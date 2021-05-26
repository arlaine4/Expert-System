import argparse
import sys

RED = '\033[38;5;1m'
GREEN = '\033[38;5;2m'
YELLOW = '\033[38;5;3m'
ORANGE = '\033[38;5;208m'
BLUE = '\033[38;5;4m'
MAGENTA = '\033[38;5;5m'
DEFAULT = '\033[39m'
EOC = '\033[0m'


def parse_args():
	"""
		:return: ArgumentParser object containing every argument passed to the program

		Basic argument checker
	"""
	options = argparse.ArgumentParser()
	options.add_argument("-i", "--input", help="path to input file")
	args = options.parse_args()
	return args


def	unpack_facts_operators(inst_eval, eq):
	operators = []
	facts = []
	for elem in eq:
		if elem.isalpha():
			facts.append(inst_eval.get_fact(elem))
		elif elem == '>':
			break
		elif not elem.isspace():
			operators.append(elem)
	return facts, operators


def	locate_query_inside_rpns(obj_query, rpns):
	indexes = []
	for (y, rpn) in enumerate(rpns):
		for (x, elem) in enumerate(rpn):
			if obj_query == elem and x > rpn.index('>'):
				indexes.append((y, x))
	return indexes


def find_fact_and_append_coord(name, facts, new_coord):
	"""
		:param name(string)				 : name of the fact we want the coordinates to be updated
		:param facts(list of strings)  : list of facts already encountered
		:param new_coord(tuple(x, y))	   : the new coordinates to add to a already existing fact

		:return: updates facts with the new coordinates
	"""
	index = [elem.name for elem in facts].index(name)
	facts[index].coord.append(new_coord)
	return facts


def check_elem_not_in_facts(elem, facts):
	"""
		:param elem(string)				 : name of fact we want to find or not inside the facts
		:param facts(list of strings)    : list of facts already encountered

		:return(bool): False if the elem is already inside facts or True if it's not
	"""
	try:
		_ = [elem.name for elem in facts].index(elem)
	except ValueError:
		return True
	return False


def check_parenthesis_inside_equation(line):
	"""
		:param line(string): the line content that we are parsing
		:return: a list of integers corresponding to the facts levels according to the parenthesis
		-> like for (A+B)-C we get -> A1+B1-C0
	"""
	levels = []
	level = 0
	# Add a condition if all levels are the same and above 1 > remove all parenthesis
	for elem in line:
		if elem.isalpha():
			levels.append(level)
			continue
		elif elem == '(':
			level += 1
		elif elem == ')':
			level -= 1
	if level != 0:
		# Call an error function with some kind of x, y and return the specific line that was wrong
		sys.exit(print("Miss matching parenthesis, please enter a valid input"))
	return levels


def update_facts_with_levels(facts, levels):
	"""
		:param facts(list) : list of Fact class instances
		:param levels(list): list of ints corresponding to levels according to parenthesis
		:return: every fact.name + level at the end like : A -> A1

	"""
	for (i, level) in enumerate(levels):
		facts[i].name += str(level)
	return facts


def check_valid_path(file_path):
	"""
		:param file_path(string): file path to check

		Just checking the path validity of a file
	"""
	try:
		fd = open(file_path, "r+")
	except FileNotFoundError:
		sys.exit(print("File does not exist, please enter a valid path."))


def check_line_type(line):
	if line[0] == '#':
		return "Comment"
	elif line[0] == '?':
		return "Query"
	elif line[0] == "=":
		return "Initial Facts"
	elif line[0].isupper() or line[0] == "(":
		return "Equation"
	elif line[0] == ")":
		return "Error found a closing parenthesis at the beginning of an equation"


left = ["(","{","["]
right = [")","}","]"]

def brackets(s):
	v = 0
	level = []
	stack = []
	for i in s:
		if i.isspace():
			continue
		elif i.isalpha():
			level.append(i)
		#elif i == '+':
			#level.append(str(v) + '&')
		elif i in "+^|":
			level.append(str(v) + i)
		elif i in left:
			v += 1
			level.append('(')
			stack.append(i)
		elif i in right:
			if not stack or left[right.index(i)] != stack[-1]:
				return ''
			v -= 1
			level.append(')')
			stack.pop()
		elif i == '=' and stack:
			return ''
		elif i == '>':
			level.append(i)
		else:
			level.append(i)
	if stack:
		return ''
	ret = ''.join(level)
	return ret

def reval(s):
	level = []
	n = 0
	for i in s:
		if i == '(':
			level.append(i)
		elif i == ')':
			level.append(i)
		elif i == '!':
			n = 1
			#level.append('(not ')
			level.append('[')
		elif not i.isnumeric() or i == '1':
			#not sure if 'i == '1'' does something
			level.append(i)
	if n:
		#return ''.join(level) + ')'
		return ''.join(level) + ']'
	return ''.join(level)

prec = ['^', '|', '+']

def recursion(l, s):
	#print(str(l) + (l + 1) * '   ' + GREEN + "start" + EOC + " '" + s + "'")
	if str(l) in s:
		if '!(' in s[0:2] and s[-1] == ')':
			n = 0
			s = s[2:-1]
		else:
			n = 1
		for p in prec:
			elems = s.split(str(l) + p)
			e = len(elems)
			if e > 1:
				t = []
				##print((l - 1) * '   ' + " found '" + str(l) + p + "'")
				#print((l + 1) * '   ' + ' ', end='')
				#print(elems)
				for elem in elems:
					#print("bra: " + brackets(elem.))
					t.append(recursion(l, elem))
					t.append(p)
				t.pop()
				##print((l - 1) * '   ' + ' ', end='')
				##print(t)
				#print((l - 1) * '   ' + ' ' + p + ' ', end='')
				#print(elems)
				##print((l - 1) * '   ' + ' ' + str(l) + p + ": \033[38;5;" + str(prec.index(p) + 3)  + "m wow found it " + EOC)
				if not n:
					##s = 'not(' + ''.join(t) + ')'
					s = '[' + ''.join(t) + ']'
				else:
					s = ''.join(t)
				##print()
				#print((l + 1) * '   ' + RED + " end  " + EOC + " '" + s + "'")
				##print("s: " + s)
				return reval('(' + s + ')') if l and (s[0] not in left or s[-1] not in right) else reval(s)
			##print((l - 1) * '   ' + " could not find '" + str(l) + p + "'")
	if not any(c.isdigit() for c in s):
		#print((l + 1) * '   ' + ORANGE + " end  " + EOC + " '" + s + "'")
		##for c in s:
			##if c.isupper():
				##print(l * '   ' + "creating op '" + ORANGE + c + "&1" + EOC + "'")
				##break
		return reval(s.replace('(', '').replace(')', ''))
	if s[0] == '(' and s[-1] == ')':
		s = s[1:-1]
	return recursion(l + 1, s)

def rpn(s):
	op = []
	rpn = []
	for c in s:
		if c.isalpha():
			rpn.append(c)
		elif c in prec:
			op.append(c)
		elif c == '[':
			op.append('!')
		elif c == ')':
			tmp = op.pop()
			rpn.append(tmp)
		elif c == ']':
			tmp = ""
			while tmp != '!':
				tmp = op.pop()
				rpn.append(tmp)
	while op:
		tmp = op.pop()
		rpn.append(tmp)
	return ' '.join(rpn)
