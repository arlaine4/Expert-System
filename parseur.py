import utils
import sys
from operation import *
from constants import *
import copy
import itertools

def read_input_file(file_path):
	with open(file_path, "r+") as fd:
		raw_content = fd.read().splitlines()
	fd.close()
	if not raw_content:
		raise EOFError(file_path)
	return raw_content


class Exsys:
	def __init__(self, file_path):
		self.raw_content = read_input_file(file_path)
		self.content = self.erase_unneeded_content()
		self.rpn = []
		self.stack = []
		self.queue = []

		self.initials = []
		self.queries = []
		self.facts = []
		self.help = [Fact("True", True), Fact("False", False), Fact("None", None)]
		self.error = None

	def init_sort(self):
		if not self.rpn:
			self.error = "no valid rule detected"
			raise EOFError(self.error)
		self.facts.sort(key=lambda x: x.name)
		for initial in self.initials:
			initial.cond = True
			initial.und = False
		self.initials.sort(key=lambda x: x.name)
		if not self.queries:
			self.queries = self.facts
		self.queries.sort(key=lambda x: x.name)
		for elem in self.rpn:
			self.queue.append(elem)


	def get_help(self, cond=None):
		for elem in self.help:
			if elem.cond == cond:
				return elem
		return elem

	def get_fact(self, name):
		for elem in self.facts:
			if elem.name == name:
				return elem
		return None

	def get(self):
		remove = []
		y = 1
		for line in self.content:
			if utils.test_valid_line(line) and self.handle_equation(line):
				continue
			remove.append(line)
			if line[0] == '=':
				self.handle_initials_queries(line, y, self.initials, "initial fact(s)")
			elif line[0] == '?':
				self.handle_initials_queries(line, y, self.queries, "query/ies")
			else:
				utils.logging.warning("%d:'%s' bad input", y, line)
			y += 1
		for r in remove:
			self.content.remove(r)
		if not self.queries:
			for elem in self.facts:
				self.queries.append(elem)

	def handle_initials_queries(self, line, y, lst, msg):
		split = line.split(line[0])
		for c in split[1]:
			if c.isalpha():
				f = self.get_fact(c)
				if not f:
					f = Fact(c)
					self.facts.append(f)
				if f not in lst:
					lst.append(f)
		if len(split) > 2:
			utils.logging.warning("reading in bonus %s", msg)
			for elem in split[2:]:
				if not elem:
					utils.logging.warning("%d:'%s' bad input", y, line)
					continue
				f = self.get_fact(elem)
				if not f:
					f = Fact(elem)
					self.facts.append(f)
				if f not in lst:
					lst.append(f)

	def handle_equation(self, line):
		utils.logging.debug("line: %s", line)
		prec = utils.precedence(line)
		utils.logging.debug("prec: %s", prec)
		if not prec:
			return False
		p, q = prec.split(">")
		p = utils.rpn(0, p)
		q = utils.rpn(0, q)

		self.rpn.append(p + " > " + q)
		utils.logging.debug("rpn:  %s > %s\n", p, q)
		for elems in (p, q):
			for elem in elems.split():
				if elem.isalpha():
					f = self.get_fact(elem)
					if not f:
						f = Fact(elem)
						self.facts.append(f)
					y = len(self.rpn) - 1
					if y not in f.y:
						f.y.append(y)
		if '<' in line:
			utils.logging.debug("line: %s", line)
			utils.logging.debug("prec: %s", prec)
			utils.logging.debug("rpn:  %s > %s\n", q, p)
			self.rpn.append(q + " > " + p)
			for elems in (q, p):
				for elem in elems.split():
					if elem.isalpha():
						f = self.get_fact(elem)
						f.y.append(y + 1)
		return True

	def run(self):
		if not self.queue:
			return
		que = self.queue.pop()
		p, q = que.split(" > ")
		utils.logging.debug("%3d:None\t%s => %s", len(self.queue), p, q)
		oper = self.solve_operation(Operation(p, q, "=>"))
		if oper.p.cond is True:
			oper.cond = self.make_oper_to_be_cond(oper.q, self.rpn.index(que), True)
			if not oper.cond:
				if not self.error:
					self.error = "could not force '%s = %s', this system will crash" % (q, True)
				return
			oper.q = self.get_help(oper.p.cond)
		elif oper.q.cond is False:
			oper.cond = self.make_oper_to_be_cond(oper.p, self.rpn.index(que), False)
			if not oper.cond:
				if not self.error:
					self.error = "could not force '%s = %s', this system will crash" % (p, False)
				return
			oper.p = self.get_help(oper.q.cond)
		utils.logging.debug("%3s:%s\n", oper.o, oper)
		return self.run()

	def make_oper_to_be_cond(self, oper, y, cond):
		if oper in self.help:
			##BONUS
			return self.set_operation(oper, y, cond)
		##NO Bonus
		if oper.cond != cond:
			oper.und = False
			oper.set(cond)
			utils.logging.info("set: %s", oper)
			self.add_to_queue(oper, y)
		return True

	def add_to_queue(self, fact, y):
		for index in fact.y:
			if y != index and self.rpn[index] not in self.queue:
				self.queue.append(self.rpn[index])
				utils.logging.debug("add:%s", self.rpn[index])

	def solve_operation(self, oper):
		if oper.o != '=>':
			utils.logging.debug("%3s:%s", oper.o, oper)
			try:
				if oper.o == '+':
					oper.cond = oper.p.cond & oper.q.cond
				elif oper.o == '|':
					if oper.p.cond or oper.q.cond:
						oper.cond = True
					else:
						oper.cond = oper.p.cond | oper.q.cond
				elif oper.o == '^':
					oper.cond = oper.p.cond ^ oper.q.cond
				elif oper.q.cond is None:
					oper.cond = None
				else:
					oper.cond = not oper.q.cond
			except:
				oper.cond = None
			self.stack.append(self.get_help(oper.cond))
			utils.logging.debug("res:%s", oper)
			return oper
		oper.p = self.solve_side(oper.p)
		oper.q = self.solve_side(oper.q)
		oper.cond = (oper.q.cond or oper.p.cond == oper.q.cond)
		while self.stack:
			self.stack.pop()
		return oper

	def solve_side(self, side):
		for elem in side.split():
			if elem[0].isalpha():
				f = self.get_fact(elem)
				self.stack.append(f)
			else:
				q = self.stack.pop()
				p = self.get_help(None) if elem == '!' else self.stack.pop()
				if (self.solve_operation(Operation(p, q, elem))).cond == None:
					break
		return self.stack.pop()

	def set_operation(self, oper, y, cond):
		facts = []
		res	= []
		rpn = self.rpn[y].split(" > ")[int(cond)]
		for elem in rpn.split():
			if elem[0].isalpha():
				f = copy.deepcopy(self.get_fact(elem))
				if f.und:
					facts.append(f)
		if not facts:
			return (oper.cond == cond)
		utils.logging.debug("%3d:None\t%s = %s", y, self.get_help(cond), rpn)
		utils.logging.debug("%3d:%s\t%s", y, cond, str(facts))
		for lst in list(itertools.product([False, True], repeat=len(facts))):
			utils.logging.debug("%stes%s:%s\t%s", ORANGE, EOC, cond, [i for i in lst])
			i = 0
			for elem in rpn.split():
				if elem[0].isalpha():
					f = copy.deepcopy(self.get_fact(elem))
					if f.und:
						self.stack.append(f)
						self.stack[-1].cond = lst[i]
						i += 1
					else:
						self.stack.append(self.get_fact(elem))
				else:
					q = self.stack.pop()
					p = self.get_help(None) if elem == '!' else self.stack.pop()
					oper = self.solve_operation(Operation(p, q, elem))
			if self.stack[-1].cond is cond:
				res.append(lst)
			self.stack.pop()
		utils.logging.debug("%3d:None\t%s => %s", y, self.get_help(cond), rpn)
		if not res:
			self.error = "the system is going to fail, DO NOT proceed with this input"
			raise ValueError(self.error)
		for elem in res:
			for (r, f) in zip(elem, facts):
				f.cond = r
			utils.logging.debug("%scho%s:%s\t%s", ORANGE, EOC, self.get_help(cond), facts)
		und = len(res) - 1
		for (i, elem) in enumerate(facts):
			f = self.get_fact(elem.name)
			if f.cond != res[0][i]:
				f.und = False
				self.add_to_queue(f, y)
			f.set(res[0][i])
			utils.logging.info("set: %s", f)
		return True

	def erase_unneeded_content(self):
		content = []
		for (y, line) in enumerate(self.raw_content):
			if not line:
				continue
			tmp = line.split('#')[0]
			if not tmp:
				continue
			tmp = ''.join(tmp.split())
			if tmp == "" or tmp in content:
				utils.logging.warning("skipping:%02d:%s", y + 1, line)
				continue
			utils.logging.debug(tmp)
			content.append(tmp)
		if not content:
			raise EOFError(content)
		return content

	def __repr__(self):
		return "facts: {}\ninitials: {}\nqueries: {}"\
				.format(self.facts, self.initials, self.queries)

	def log(self, f):
		s = 10 * ' '
		f("(\033[38;5;021marlaine%s)%sexpert system%s(\033[38;5;129mmheutsch%s)", EOC, s, s, EOC)
		for (x, rule) in enumerate(self.content):
			f("rule:%02d: %s", x, rule)
		f("facts:   %s", str(self.facts))
		f("initials:%s", str(self.initials))
		f("queries: %s\n", str(self.queries))

	def result(self):
		if not self.error:
			if len(self.queries) - 1:
				utils.logging.info("Your queries are: %s", str(self.queries))
			else:
				utils.logging.info("Your query is: %s", str(self.queries))
		else:
			raise ValueError(self.error)

class Fact:
	def __init__(self, name, cond=False):
		self.cond = cond
		self.name = name
		self.y = []
		self.und = True

	def set(self, cond=True):
		if not self.cond:
			self.cond = cond
		elif cond == False:
			self.cond = "you're trying to set %s to 'False'" % (self)
			raise ValueError(self.cond)

	def __repr__(self):
		if self.cond is True:
			tmp = 2
		elif self.cond is False:
			tmp = 1
		else:
			tmp = 3
		return "\033[38;5;{}m{}{}".format(tmp, self.name, EOC)
