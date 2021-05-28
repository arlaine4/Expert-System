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
		self.help = []
		self.help.append(Fact("True", (-1,-1)))
		self.help[-1].cond = True
		self.help.append(Fact("False", (-1,-1)))
		self.help[-1].cond = False
		self.help.append(Fact("None", (-1,-1)))
		self.error = None

	def init_sort(self, skip):
		"""
			Sorting facts, initials and queries by alphabetical order
			assigning initial facts with the corresponding condition aswell
		"""
		self.facts.sort(key=lambda x: x.name)
		for fact in self.facts:
			fact.coord.sort(key=lambda x: x[0])
		self.initials.sort(key=lambda x: x.name)
		for initial in self.initials:
			initial.cond = True
		self.queries.sort(key=lambda x: x.name)
		for query in (self.queries if skip else self.facts):
			self.queue.append(query)


	def get_help(self, cond):
		"""
			:param cond(string) : cond of the fact we want to acces
			:return: fact 'True'/'False'/'None'
		"""
		for elem in self.help:
			if elem.cond == cond:
				return elem
		return None

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
		for (y, line) in enumerate(self.content):
			if line[0] == '=':
				self.handle_initials_queries(line, y, self.initials, "initial fact(s)")
			elif line[0] == '?':
				self.handle_initials_queries(line, y, self.queries, "query/ies")
			elif (line[0].isalpha() or line[0] in lleft) and "=>" in line:
				self.handle_equation(line, y)
			else:
				utils.logging.warning("%d:'%s' bad input" % (y, line))
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
					f = Fact(c, (-1, -1))
					self.facts.append(f)
				lst.append(f)
		if len(split) > 2:
			utils.logging.warning("reading in bonus %s" % (msg))
			for elem in split[2:]:
				if not elem:
					utils.logging.warning("%d:'%s' bad input" % (y, line))
					continue
				f = self.get_fact(elem)
				if not f:
					f = Fact(elem, (-1,-1))
					self.facts.append(f)
				lst.append(f)

	def handle_equation(self, line, y):
		"""
			:param line(string)		: content of the equation
			:param y(int)		    : line number, corresponds to a y position

			This method deals with equation by splitting the line in 'p' and 'q' parts, reversing it if needed
			and storing the facts name
		"""
		utils.logging.debug("-------------------------------------------")
		utils.logging.debug(line)
		prec = utils.precedence(line)
		utils.logging.debug(prec)
		if not prec:
			utils.logging.warning("%d:'%s' bad input" % (y, line))
			return
		p, q = prec.split(">")
		p = utils.rpn(0, p)
		q = utils.rpn(0, q)

		if p + " > " + q in self.rpn:
			return
		self.rpn.append(p + " > " + q)
		utils.logging.debug("rpn " + p + " > " + q)
		x = len(p) + len(q)
		for elems in (p, q):
			for elem in elems.split():
				if elem.isalpha():
					f = self.get_fact(elem)
					if not f:
						f = Fact(elem, (x, y))
						self.facts.append(f)
					if (x, y) not in f.coord:
						add_coord_to_class(f, (x, y))
		if '<' in line:
			self.rpn.append(q + " > " + p)

	def run(self):
		i = len(self.queue) - 1
		while i >= 0:
			utils.logging.debug("que:%s %d" % (self.queue, i))
			if self.queue[i].cond != None:
				utils.logging.debug("query %s is %s" % (self.queue[i], self.queue[i].cond))
				self.queue.remove(self.queue[i])
				i = len(self.queue) - 1
				continue
			utils.logging.debug("%snew%s query is %s" % (ORANGE, EOC, self.queue[i]))
			for y in self.queue[i].coord:
				utils.logging.debug("-------------------------------------------")
				p, q = self.rpn[y[1]].split(" > ")
				self.solve(Operation(p, q, "=>"))
				q = self.stack.pop()
				p = self.stack.pop()
				utils.logging.debug("%s => %s" % (p, q))
				if p.cond == True:
					#force q to be true
					continue
				if p.cond == None and p not in self.queue:
					self.queue.append(p)
					i = len(self.queue)
					break
				if q.cond == None and q not in self.queue:
					self.queue.append(q)
					i = len(self.queue)
					break
			i -= 1

	def make(self, oper, cond):
		return

	def solve(self, oper):
		utils.logging.debug("%3s:%s" % (oper.o, oper))
		if oper.o != '=>':
			try:
				if oper.o == '+':
					oper.cond = oper.p.cond & oper.q.cond
				elif oper.o == '|':
					oper.cond = oper.p.cond | oper.q.cond
				elif oper.o == '^':
					oper.cond = oper.p.cond ^ oper.q.cond
				elif oper.q.cond == None:
					oper.cond = None
				else:
					oper.cond = not oper.q.cond
			except:
				if oper.p.cond == None and oper.p not in self.queue:
					self.queue.append(oper.p)
				if oper.q.cond == None and oper.q not in self.queue:
					self.queue.append(oper.q)
				oper.cond = None
			self.stack.append(self.get_help(oper.cond))
			utils.logging.debug("res:%s" % (oper))
			return
		for elems in (oper.p, oper.q):
			for elem in elems.split():
				if elem[0].isalpha():
					f = self.get_fact(elem)
					self.stack.append(f)
				else:
					q = self.stack.pop()
					p = None if elem == '!' else self.stack.pop()
					o = Operation(p, q, elem)
					self.solve(o)

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
			content.append(''.join(tmp.split()))
		if not content:
			raise EOFError(content)
		return content

	def __repr__(self):
		return "facts:   {}\n\t\t\tinitials:{}\n\t\t\tqueries: {}"\
				.format(self.facts, self.initials, self.queries)

class Fact:
	def __init__(self, name, coord):
		"""
			cond (bool)				  : the fact's condition
			name (char)				  : name of the fact -> ex: A
			coord (tuple(x, y))		  : x, y coordinates -> x = inside line pos and y = line number
			negation (bool)			  : True or False whether the fact is set as True or False
		"""
		self.cond = None
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
