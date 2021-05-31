import utils
import sys
from equation import *
from constants import *


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
		self.help = [Fact("None"), Fact("True", True), Fact("False", False)]
		self.error = None

	def init_sort(self, skip):
		"""
			Sorting facts, initials and queries by alphabetical order
			assigning initial facts with the corresponding condition aswell
		"""
		for fact in self.facts:
			fact.coord.sort(key=lambda x: x[1])
		self.initials.sort(key=lambda x: x.name)
		for initial in self.initials:
			initial.cond = True
		self.queries.sort(key=lambda x: x.name)
		for query in (self.queries if skip else self.facts):
#			if not query.cond:
#				self.queue.append(query)
			self.queue.append(query)


	def get_help(self, cond=None):
		"""
			:param cond(string) : cond of the fact we want to acces
			:return: fact 'True'/'False'/'None'
		"""
		for elem in self.help:
			if elem.cond == cond:
				return elem
		raise ValueError("helper fact not found")

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
					utils.logging.debug("-------------------------------------------")
					utils.logging.warning("%d:'%s' bad input", y, line)
		for r in remove:
			self.content.remove(r)
		utils.logging.debug("-------------------------------------------")
		if not self.initials:
			self.error = "NO initial fact(s) detected"
		elif not self.queries:
			self.error = "NO query/ies detected"
		if self.error:
			raise SyntaxError(self.error)

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
				lst.append(f)

	def handle_equation(self, line, y, r):
		"""
			:param line(string)		: content of the equation
			:param y(int)		    : line number, corresponds to a y position

			This method deals with equation by splitting the line in 'p' and 'q' parts, reversing it if needed
			and storing the facts name
		"""
		utils.logging.debug("-------------------------------------------")
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
		utils.logging.debug("rpn:  %s > %s", p, q)
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
						utils.logging.debug("%s: (%d, %d)", f, y - r, x)
		if '<' in line:
			utils.logging.debug("line: %s", line)
			utils.logging.debug("prec: %s", prec)
			utils.logging.debug("rpn:  %s > %s", q, p)
			y += (1 - r)
			self.rpn.append(q + " > " + p)
			for elems in (q, p):
				for elem in elems.split():
					if elem.isalpha():
						f = self.get_fact(elem)
						if (y, x) not in f.coord:
							add_coord_to_class(f, (y, x))
							utils.logging.debug("%s: (%d, %d)", f, y, x)
			return r - 1
		return r


	def run(self):
		utils.logging.debug("hel:%s", self.help)
		i = len(self.queue) - 1
		while i >= 0:
			utils.logging.debug("que:%s %d", self.queue, i)
			utils.logging.debug("-------------------------------------------")
#			if self.queue[i].cond != None:
#				utils.logging.debug("query %s is %s", self.queue[i], self.queue[i].cond)
#				self.queue.remove(self.queue[i])
#				i = len(self.queue) - 1
#				utils.logging.debug("-------------------------------------------")
#				continue
			utils.logging.debug("%squery%s is %s (rpn[y], cnt(p.op))", ORANGE, EOC, self.queue[i])
			utils.logging.debug("%s", str(self.queue[i].coord))
			for y in self.queue[i].coord:
				utils.logging.debug("-------------------------------------------")
				utils.logging.debug("rpn:%-3d\t%s", y[0], self.rpn[y[0]])
				n, u = self.rpn[y[0]].split(" > ")
				oper = Operation(n, u, "=>")
				self.solve_operation(oper)
				q = self.stack.pop()
				p = self.stack.pop()
				while self.stack:
					self.stack.pop()
				if p.cond is True:
					if q.cond is True:
						continue
					if not self.make_oper_to_be_cond(q, u, True):
						oper.cond = False
						self.error = "bad:%s" % (oper)
						return
					oper.cond = True
					utils.logging.info("res: %s", oper)
					continue
				elif q.cond is False:
					if p.cond is False:
						continue
					if not self.make_oper_to_be_cond(p, n, False):
						oper.cond = False
						self.error = "bad:%s" % (oper)
						return
					oper.cond = True
					utils.logging.info("res: %s", oper)
					continue
				else:
					utils.logging.debug("res:%s", oper)
				if p not in self.help and p.cond is None and p not in self.queue:
					utils.logging.debug("add:%s", p)
					self.queue.append(p)
					i = len(self.queue)
					break
				if q not in self.help and q.cond is None and q not in self.queue:
					utils.logging.debug("add:%s", q)
					self.queue.append(q)
					i = len(self.queue)
					break
			i -= 1
		utils.logging.debug("que:%s", self.queue)

	def make_oper_to_be_cond(self, oper, rpn, cond):
		if oper.cond == (not cond):
			return False
		if oper.name != "None":
			oper.cond = cond
			utils.logging.info("set: %s", oper)
			return True
		self.stack.append(self.get_help(cond))
		return self.set_operation(rpn)

	def set_operation(self, rpn):
		npr = rpn[::-1]
		utils.logging.debug("npr:%s", npr)
		o = ''
		for elem in npr.split():
			utils.logging.debug("ehm:%s", self.stack)
			utils.logging.debug("%1s %s", o, elem)
			if elem == '!':
				o = '!'
				#	p	|	q	|  !q
				#-------|-------|-------
				#		|	T	|	F
				#		|	F	|	T
				q = self.stack.pop()
				self.stack.append(self.get_help(not q.cond))
			elif not elem[0].isalpha():
				o = elem
			elif o == '+':
				#	p	|	q	| p + q
				#-------|-------|-------
				#	T	|	T	|	T
				#	T	|	F	|	F
				#	F	|	T	|	F
				#	F	|	F	|	F
				p = self.stack.pop()
				q = self.get_fact(elem)
				if q.cond == (not p.cond):
					#falsch
					return False
				if p.cond:
					if q.cond != p.cond:
						q.cond = p.cond
						utils.logging.info("set: %s", q)
				else:
					utils.logging.debug("und:%s", q)
				oper = Operation(p, q, o)
				self.solve_operation(oper)
				o = ''
			elif o == '|':
				#	p	|	q	| p | q
				#-------|-------|-------
				#	T	|	T	|	T
				#	T	|	F	|	T
				#	F	|	T	|	T
				#	F	|	F	|	F
				p = self.stack.pop()
				q = self.get_fact(elem)
				if p.cond is True:
					return p.cond
				if q.cond is True:
					return False
				q.cond = p.cond
				utils.logging.info("set: %s", q)
				oper = Operation(p, q, o)
				self.solve_operation(oper)
				o = ''
			elif o == '^':
				#	p	|	q	| p ^ q
				#-------|-------|-------
				#	T	|	T	|	F
				#	T	|	F	|	T
				#	F	|	T	|	T
				#	F	|	F	|	F
				q = self.get_fact(elem)
			else:
				q = self.get_fact(elem)
				q.cond = self.stack[-1].cond
				utils.logging.info("set: %s", q)

		self.stack.pop()
		return True

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
				if oper.p.cond is None and oper.p not in self.help and oper.p not in self.queue:
					utils.logging.debug("add:%s", oper.p)
					self.queue.append(oper.p)
				if oper.q.cond is None and oper.q not in self.help and oper.q not in self.queue:
					utils.logging.debug("add:%s", oper.q)
					self.queue.append(oper.q)
				oper.cond = None
			utils.logging.debug(oper.cond)
			self.stack.append(self.get_help(oper.cond))
			utils.logging.debug("res:%s", oper)
			return oper.cond
		for elems in (oper.p, oper.q):
			for elem in elems.split():
				if elem[0].isalpha():
					f = self.get_fact(elem)
					self.stack.append(f)
				else:
					q = self.stack.pop()
					p = self.get_help() if elem == '!' else self.stack.pop()
					o = Operation(p, q, elem)
					if self.solve_operation(o) is None:
						break
		return oper.cond

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
			if tmp in content:
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
		for (x, rule) in enumerate(self.content):
			f("rule:%02d: %s", x, rule)
		f("facts:   %s", str(self.facts))
		f("initials:%s", str(self.initials))
		f("queries: %s", str(self.queries))

	def result(self):
		if not self.error:
			if len(self.queries) - 1:
				utils.logging.info("Your queries are: %s", str(self.queries))
			else:
				utils.logging.info("Your query is: %s", str(self.queries))
		else:
			utils.logging.error(self.error)

class Fact:
	def __init__(self, name, cond=None):
		"""
			cond (bool)				  : the fact's condition
			name (char)				  : name of the fact -> ex: A
			coord (tuple(y, x))		  : (rpn[y], cnt(rpn[y].p.op))
			negation (bool)			  : True or False whether the fact is set as True or False
		"""
		self.cond = cond
		self.name = name
		self.coord = []

	def __repr__(self):
		if self.cond is True:
			tmp = 2
		elif self.cond is False:
			tmp = 1
		else:
			tmp = 3
		return "\033[38;5;{}m{}{}".format(tmp, self.name, EOC)
