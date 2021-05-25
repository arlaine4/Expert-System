import utils
from utils import *
import sys

RED = '\033[38;5;1m'
GREEN = "\033[38;5;2m"
YELLOW = '\033[38;5;3m'
BLUE = '\033[38;5;4m'
EOC = '\033[0m'


def unpack_facts_to_list(facts):
	"""
		:param facts: string to decompose into a list of chars
		:return: list of chars

		Unpacking a string into a list of chars, used for initial facts
		and queries
	"""
	lst_facts = []
	for c in facts:
		if c == '#':
			break
		elif c.isspace() or c == "=" or c == "?":
			continue
		lst_facts.append(c)
	return lst_facts


def update_initial_fact(line):
	pass


def check_initial_facts_cond(fact, initial):
	"""
		:param fact: string
		:return: Bool whether the string fact is inside the global initial or not

		returns True if the fact name is inside initial list or False if it isn't
	"""
	return True if fact in initial else False


def add_coord_to_class(instance, new_coord):
	"""
		:param instance (class): class instance we want the coordinates to be updated
		:param new_coord (int, int): the coordinates to add the instance coordinates list
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
			# Skipping empty lines
			if len(line) > 1:
				raw_content.append(line)
	return raw_content


class Exsys:
	def __init__(self, file_path):
		"""
			:param file_path(string)				: Path to the input file

			raw_content(list of class instances)	: all the raw file content
			queries(list of chars)				    : all the queries inside the file
			comments(list of Comment() instances)   : all the comments encountered inside the file
			equations(list of Equation() instances) : all the equation encountered inside the file
		"""
		self.raw_content = read_input_file(file_path)
		self.content = self.erase_unneeded_content()
		self.rpn = []

		self.initials = []
		self.queries = []
		self.comments = []
		self.equations = []
		self.facts = []

	def get_fact(self, name):
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

	def handle_comment(self, line, y):
		self.comments.append(Comment((0, y), line, 0))

	def handle_equation(self, left, right, y):
		#this is not true anymore
		"""
			:param line(string)	 	: line content
			:param y(int)		    : line number, corresponds to a y position

			This method deals with equation by splitting the line in left and right parts, reversing it if needed
			and storing the facts name + dealing with left and right parts separately by calling
			Equation.parse_equation_side(side(left or rigt), lift_of_facts_names, number_of_line)
		"""
		eq = Equation()
		line = brackets(left + '=>' + right)
		left, right = line.split("=>")
		left = recursion(0, left)
		right = recursion(0, right)
		left = rpn(left)
		right = rpn(right)

		for (x, elem) in enumerate(left + " => " + right):
			if elem.isalpha():
				if utils.check_elem_not_in_facts(elem, self.facts):
					f = Fact(elem, (x, y))
					self.facts.append(f)
				else:
					f = self.get_fact(elem)
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


class Comment:
	def __init__(self, coord, line, start_pos):
		"""
			:param coord(tuple(x, y)) : x, y position of the comment
			:param line(string)	   : full line content
			:param start_pos(int)	 : x position where we start getting the comment content
		"""
		self.coord = []
		self.coord = add_coord_to_class(self, coord)
		self.content = line[start_pos:]


class Query:
	def __init__(self, compact_queries):
		"""
			:param compact_queries(string) : queries glued to each other inside a string

			queries (list of chars)		: list of all the queries
		"""
		self.queries = []
		self.queries = unpack_facts_to_list(compact_queries)


class Equation:
	def __init__(self):
		"""
			operator (list of char)					 : operator on the right side of the fact, related to the next fact
			left (list of class instances)	  : left side of the equation, list of facts
			right (list of class instances)	 : right side of the equation, list of facts
		"""
		self.op = []
		self.fact = []


class Fact:
	def __init__(self, c, coord):
		"""
			cond (bool)				  : the fact's condition
			name (char)				  : name of the fact -> ex: A
			coord (tuple(x, y))		: x, y coordinates -> x = inside line pos and y = line number
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
