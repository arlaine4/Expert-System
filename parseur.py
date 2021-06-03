import utils
import sys
from equation import *
from constants import *
import copy
import itertools

def add_coord_to_class(instance, new_coord):
	"""
		:param instance (class)			: class instance we want the coordinates to be updated
		:param new_coord (int, int)		: the coordinates to add the instance coordinates list
				-> new_coord correspond to the x (inside line related) and y(wich line) coordinates
				   of the new element to add to the class

		:return: update coordinates list

		Update Fact and Comment classes coordinates
	"""
	instance.coord.append(new_coord)
	return instance.coord

def read_input_file(file_path):
	"""
		:param file_path(string) : path to the file that we are going to read information from

		Reading input file to store every line into a list
	"""
	with open(file_path, "r+") as fd:
		raw_content = fd.read().splitlines()
	fd.close()
	if not raw_content:
		raise EOFError(file_path)
	return raw_content


class Exsys:
	def __init__(self, file_path):
		"""
			:param file_path(string)				: Path to the input file

			raw_content(list of class instances)	: all the raw file content
			queries(list of chars)				    : all the queries inside the file
			rpn (list of strings)					: all the equations in reverse polish notation
			facts (list of Fact instances)			: all the facts available for this file
			content(list)							: content without comments
		"""
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

	def init_sort(self, skip):
		"""
			Sorting facts, initials and queries by alphabetical order
			assigning initial facts with the corresponding condition aswell
		"""
		if not self.rpn:
			self.error = "no valid rule detected"
			raise EOFError(self.error)
		self.facts.sort(key=lambda x: x.name)
		self.initials.sort(key=lambda x: x.name)
		for initial in self.initials:
			initial.cond = True
		self.queries.sort(key=lambda x: x.name)
		for elem in self.rpn:
			self.queue.append(elem)


	def get_help(self, cond=None):
		"""
			:param cond(string) : cond of the fact we want to acces
			:return: fact 'True'/'False'/'None'
		"""
		for elem in self.help:
			if elem.cond == cond:
				return elem
		return elem

	def get_fact(self, name):
		"""
			:param name(string) : name of the fact we want to acces
			:return: the elem when its found inside the facts or None
		"""
		for elem in self.facts:
			if elem.name == name:
				return elem
		return None

	def get(self):
		"""
			Main parsing loop
		"""
		remove = []
		r = 0
		for (y, line) in enumerate(self.content):
			if utils.test_valid_line(line):
				r = self.handle_equation(line, y, r)
			else:
				remove.append(line)
				r += 1
				if line[0] == '=':
					self.handle_initials_queries(line, y, self.initials, "initial fact(s)")
				elif line[0] == '?':
					self.handle_initials_queries(line, y, self.queries, "query/ies")
				else:
					utils.logging.warning("%d:'%s' bad input", y, line)
		for r in remove:
			self.content.remove(r)
		if not self.queries:
			for elem in self.facts:
				self.queries.append(elem)

	def handle_initials_queries(self, line, y, lst, msg):
		"""
			:param line(string)				: content of the line we are parsing
			:param lst(list of Fact)		: list of Facts for queries or initial facts

			Assign queries or initial facts depending on what you want to get
		"""
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

	def handle_equation(self, line, y, r):
		"""
			:param line(string)		: content of the equation
			:param y(int)		    : line number, corresponds to a y position

			This method deals with equation by splitting the line in 'p' and 'q' parts, reversing it if needed
			and storing the facts name
		"""
		utils.logging.debug("line: %s", line)
		prec = utils.precedence(line)
		utils.logging.debug("prec: %s", prec)
		if not prec:
			utils.logging.warning("%d:'%s' bad input", y, line)
			return r + 1
		p, q = prec.split(">")
		p = utils.rpn(0, p)
		q = utils.rpn(0, q)

		self.rpn.append(p + " > " + q)
		utils.logging.debug("rpn:  %s > %s\n", p, q)
		x = sum([p.count(e) for e in pprec[:-1]])
		for elems in (p, q):
			for elem in elems.split():
				if elem.isalpha():
					f = self.get_fact(elem)
					if not f:
						f = Fact(elem)
						self.facts.append(f)
					if (y - r, x) not in f.coord:
						add_coord_to_class(f, (y - r, x))
		if '<' in line:
			utils.logging.debug("line: %s", line)
			utils.logging.debug("prec: %s", prec)
			utils.logging.debug("rpn:  %s > %s\n", q, p)
			y += (1 - r)
			self.rpn.append(q + " > " + p)
			for elems in (q, p):
				for elem in elems.split():
					if elem.isalpha():
						f = self.get_fact(elem)
						add_coord_to_class(f, (y, x))
			return r - 1
		return r

	def run(self):
		if not self.queue:
			return
		p, q = self.queue.pop().split(" > ")
		utils.logging.debug("%3d:None\t%s => %s", len(self.queue), p, q)
		oper = self.solve_operation(Operation(p, q, "=>"))
		if oper.p.cond is True:
			oper.cond = self.make_oper_to_be_cond(oper.q, self.rpn.index(p + " > " + q), True)
			if not oper.cond:
				return
			oper.q = self.get_help(oper.p.cond)
		elif oper.q.cond is False:
			oper.cond = self.make_oper_to_be_cond(oper.q, self.rpn.index(p + " > " + q), False)
			if not oper.cond:
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
			oper.set(cond)
#			utils.logging.info("set: %s %s", oper, str(oper.coord))
			utils.logging.info("set: %s", oper)
			self.add_to_queue(oper, y)
		return True

	def add_to_queue(self, fact, y):
		for coord in fact.coord:
			if y != coord[0] and self.rpn[coord[0]] not in self.queue:
				self.queue.append(self.rpn[coord[0]])
				utils.logging.debug("add:%s", self.rpn[coord[0]])

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
		oper.cond = (oper.p == oper.q)
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
				facts.append(self.get_fact(elem))
		utils.logging.debug("%3d:None\t%s => %s", y, self.get_help(cond), rpn)
		utils.logging.debug("%3d:%s\t%s", y, cond, str(facts))
		for lst in list(itertools.product([True, False], repeat=len(facts))):
			utils.logging.debug("tes:%s", str(lst))
#			self.stack.append(self.get_help(cond))
			i = 0
			for elem in rpn.split():
				if elem[0].isalpha():
					self.stack.append(copy.deepcopy(self.get_fact(elem)))
					self.stack[-1].cond = lst[i]
					i += 1
				else:
					q = self.stack.pop()
					p = self.get_help(None) if elem == '!' else self.stack.pop()
					oper = self.solve_operation(Operation(p, q, elem))
			if self.stack[-1].cond is cond:
				res.append(lst)
			self.stack.pop()
		utils.logging.debug("%s", str(res))
		for (i, elem) in enumerate(facts):
			if elem.cond != cond:
				elem.set(res[0][i])
#				utils.logging.info("set: %s %s", elem, elem.coord)
				utils.logging.info("set: %s", elem)
				self.add_to_queue(elem, y)
		return True
		utils.logging.error("You're trying to do bonus that is not implemented")
		self.error = "If you stick with this input noone knows what will happen"
		return False

	def erase_unneeded_content(self):
		"""
			Erasing whitespaces and comments and skipping empty lines
		"""
		content = []
		for line in self.raw_content:
			if not line:
				continue
			tmp = line.split('#')[0]
			if not tmp:
				continue
			tmp = ''.join(tmp.split())
			if tmp == "" or tmp in content:
				utils.logging.warning("skipping %s", line)
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
			utils.logging.error(self.error)

class Fact:
	def __init__(self, name, cond=False):
		"""
			cond (bool)				  : the fact's condition
			name (char)				  : name of the fact -> ex: A
			coord (tuple(y, x))		  : (rpn[y], cnt(rpn[y].p.op))
			negation (bool)			  : True or False whether the fact is set as True or False
		"""
		self.cond = cond
		self.name = name
		self.coord = []

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
