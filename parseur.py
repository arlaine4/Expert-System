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
	raw_content = []
	with open(file_path, "r+") as fd:
		for line in fd:
			if len(line) > 1:
				raw_content.append(line)
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
		if not self.content:
			sys.exit(print("You provided an empty file, please enter a valid input."))
		for (y, line) in enumerate(self.content):
			line_type = utils.check_line_type(line)
			if line_type == "Initial Facts":
				self.handle_initials_queries(line, self.initials)
			elif line_type == "Query":
				self.handle_initials_queries(line, self.queries)
			elif line_type == "Equation":
				if "<" in line:
					left, right = line.split("<=>")
					self.handle_equation(right, left, y)
				else:
					left, right = line.split("=>")
				self.handle_equation(left, right, y)

	def handle_initials_queries(self, line, initquer):
		"""
			:param line(string)				: content of the line we are parsing
			:param initquer(list of Fact)	: list of Facts for queries or initial facts

			Assign queries or initial facts depending on what you want to get
		"""
		line = line.replace("=", '')
		line = line.replace("?", '')
		for c in line:
			if utils.check_elem_not_in_facts(c, self.facts):
				f = Fact(c, (-1, -1))
				self.facts.append(f)
			else:
				f = self.get_fact(c)
			initquer.append(f)
		if len(initquer) == 0:
			sys.exit(print("No queries or initial facts detected, please enter a valid input."))

	def handle_equation(self, left, right, y):
		"""
			:param left(string)		: left side of the equation
			:param right(string)	: right side of the equation
			:param y(int)		    : line number, corresponds to a y position

			This method deals with equation by splitting the line in left and right parts, reversing it if needed
			and storing the facts name + dealing with left and right parts separately by calling
			Equation.parse_equation_side(side(left or rigt), lift_of_facts_names, number_of_line)
		"""
		line = utils.brackets(left + '=>' + right)
		left, right = line.split("=>")

		left = utils.recursion(0, left)
		right = utils.recursion(0, right)

		left = utils.rpn(left)
		right = utils.rpn(right)

		for (x, elem) in enumerate(left + " => " + right):
			if elem.isalpha():
				if utils.check_elem_not_in_facts(elem, self.facts):
					f = Fact(elem, (x, y))
					self.facts.append(f)
				else:
					utils.find_fact_and_append_coord(elem, self.facts, (x, y))
		self.rpn.append(left + " > " + right)

	def erase_unneeded_content(self):
		"""
			Erasing whitespaces and comments
		"""
		content = []
		for line in self.raw_content:
			tmp = line.split('#')[0]
			if tmp:
				content.append("".join(tmp.split()))
		return content

	def __repr__(self):
		return "facts:   {}\ninitials:{}\nqueries: {}"\
				.format(self.facts, self.initials, self.queries)


class Fact:
	def __init__(self, c, coord):
		"""
			cond (bool)				  : the fact's condition
			name (char)				  : name of the fact -> ex: A
			coord (tuple(x, y))		  : x, y coordinates -> x = inside line pos and y = line number
			negation (bool)			  : True or False whether the fact is set as True or False
		"""
		self.cond = None
		self.negation = False
		self.name = c
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
