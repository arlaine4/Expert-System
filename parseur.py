import utils
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
		:return: Bool wheter the string fact is inside the global initial or not

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
			print(y, line)
			line_type = utils.check_line_type(line)
			if line_type == "Initial Facts":
				self.handle_initials_queries(line, self.initials)
			elif line_type == "Query":
				self.handle_initials_queries(line, self.queries)
			elif line_type == "Equation":
				self.handle_equation(line, y)

	def handle_initials_queries(self, line, initquer):
		"""
			:param line(string): content of the line we are parsing
			:param initquer(list of Fact): list of Facts for queries or initial facts

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
			initquer.insert(0, f)
		if len(initquer) == 0:
			sys.exit(print("No queries or initial facts detected, please enter a valid input."))

	def handle_comment(self, line, y):
		self.comments.append(Comment((0, y), line, 0))

	def handle_equation(self, line, y):
		"""
			:param line(string)	 : line content
			:param y(int)		   : line number, corresponds to a y position

			This method deals with equation by splitting the line in left and right parts, reversing it if needed
			and storing the facts name + dealing with left and right parts separately by calling
			Equation.parse_equation_side(side(left or rigt), lift_of_facts_names, number_of_line)
		"""
		eq = Equation()
		split_line = line.split('#')

		if "<=>" in split_line[0]:
			bi = Equation()
			eq.operator = "<=>"
			left, right = split_line[0].split('<=>')
			self.facts, bi.right = bi.parse_equation_side(left, self.facts, y)
			self.facts, bi.left = bi.parse_equation_side(right, self.facts, y)
			self.equations.append(bi)
		else:
			left, right = split_line[0].split('=>')

		self.facts, eq.left = eq.parse_equation_side(left, self.facts, y)
		self.facts, eq.right = eq.parse_equation_side(right, self.facts, y)

		self.equations.append(eq)

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
			neg_bool (tuple(bool, bool))		: if the left/right part of the equation has a negation operator '!'
			operator (char)					 : operator on the right side of the fact, related to the next fact
			left (list of class instances)	  : left side of the equation, list of facts
			right (list of class instances)	 : right side of the equation, list of facts
		"""
		self.neg_bool = (False, False)
		self.operator = ''
		self.left = []
		self.right = []

	def parse_equation_side(self, side, facts, y):
		"""
			:param side(string): string that cointains a side, left or right
			:param facts(list): list of fact names already encountered
			:param y(int): line number
			:return: facts(list) updated, new_side(list) which corresponds to left or right side as
				a list of Fact instances
		"""
		# Error parsing needs to be done

		prev = None
		tmp_negation = False
		new_side = []
		for (x, elem) in enumerate(side):
			if elem.isalpha():
				new_side.append(Fact(elem, (x, y)))
				new_side[-1].previous = prev
				if utils.check_elem_not_in_facts(elem, facts):
					facts.append(Fact(elem, (x, y)))
				else:
					utils.find_fact_and_append_coord(elem, facts, (x, y))
				prev = elem
				if tmp_negation:
					new_side[-1].negation = True
					tmp_negation = False
			else:
				if elem == '!' and len(new_side) == 0:
					tmp_negation = True
					continue
				elif elem == "(" or elem == ")":
					continue
				new_side[-1].operator = elem
		levels = utils.check_parenthesis_inside_equation(side)
		new_side = utils.update_facts_with_levels(new_side, levels)
		#print(facts)
		return facts, new_side


class Fact:
	def __init__(self, c, coord):
		"""
			cond (bool)				  : If the fact is true or not regarding to the initial_facts
			operator (char)			  : Operator (after the fact) associated with a fact
			name (char)				  : name of the fact -> ex: A
			relative_coord (tuple(x, y)) : x, y coordinates -> x = inside line pos and y = line number
			previous (class instance)	: left connected element to the current fact
		"""
		self.cond = False
		self.operator = None
		self.negation = False
		self.name = c
		self.coord = []
		self.sides = []
		self.coord = add_coord_to_class(self, coord)
		self.previous = None

	def __repr__(self):
		return "{} {}{}{}{}"\
				.format((self.previous if self.previous else ' '), (GREEN if self.cond else RED), self.name, EOC, (self.operator if self.operator else ' '))
