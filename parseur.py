import utils
import sys
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

		self.initials = []
		self.queries = []
		self.facts = []
		self.error = None

	def init_sort(self):
		"""
			Sorting facts, initials and queries by alphabetical order
			assigning initial facts with the corresponding condition aswell
		"""
		self.facts.sort(key=lambda x: x.name)
		self.initials.sort(key=lambda x: x.name)
		self.queries.sort(key=lambda x: x.name)
		for elem in self.initials:
			elem.cond = True

	def get_fact(self, name):
		"""
			:param name(string) : name of the fact we want to acces
			:return: the elem when its found inside the facts or None
		"""
		for elem in self.facts:
			if elem.name == name:
				return elem
		return None

	def parsing(self):
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

		self.rpn.append(p + " > " + q)
		utils.logging.debug(self.rpn[-1])
		x = 0
		for elems in (p.split(), q.split()):
			for elem in elems:
				if elem.isalpha():
					f = self.get_fact(elem)
					if not f:
						f = Fact(elem, (x, y))
						self.facts.append(f)
		if '<' in line:
			self.rpn.append(q + " > " + p)

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
		return "facts:   {}\ninitials:{}\nqueries: {}"\
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
		self.negation = False
		self.name = name
		self.coord = []
		self.coord = add_coord_to_class(self, coord)

	def __repr__(self):
		if self.cond is True:
			tmp = 2
		elif self.cond is False:
			tmp = 1
		else:
			tmp = 3
		return "\033[38;5;{}m{}{}".format(tmp, self.name, EOC)
