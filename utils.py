import argparse
import sys
from constants import *


def parse_args():
	"""
		:return: ArgumentParser object containing every argument passed to the program

		Basic argument checker
	"""
	options = argparse.ArgumentParser()
	options.add_argument("-i", "--input", help="path to input file")
	args = options.parse_args()
	return args


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
	"""
		:param line(str): line content
		:return: string that represents the type of line that we encountered
	"""
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


def brackets(line):
	"""
		:line:		line content (equation)

		Applying a level(int) to all operators present in the current equation
		to later be able to split in the right order and respect the presedence of each operator
		Example: A+(B+C) --> A0+B1+C
	"""
	levels = []
	level = 0
	stack = []
	for elem in line:
		if elem.isalpha():
			levels.append(elem)
		elif elem in "+^|":
			levels.append(str(level) + elem)
		elif elem in left:
			level += 1
			levels.append('(')
			stack.append(elem)
		elif elem in right:
			if not stack or left[right.index(elem)] != stack[-1]:
				return ''
			level -= 1
			levels.append(')')
			stack.pop()
		elif elem == '=' and stack:
			return ''
		else:
			levels.append(elem)
	return '' if stack else ''.join(levels)


def	rpn(line):
	operators = []
	rpn = []
	for elem in line:
		if elem.isalpha():
			rpn.append(elem)
		elif elem in prec or elem == '(':
			operators.append(elem)
		elif elem == '[':
			operators.append('!')
		elif elem == ')':
			print(operators)
			tmp = operators.pop()
			while tmp != '(':
				rpn.append(tmp)
				tmp = operators.pop()
		elif elem == ']':
			tmp = ""
			while tmp != '!':
				tmp = operators.pop()
				rpn.append(tmp)
	for op in reversed(operators):
		rpn.append(op)
	return ' '.join(rpn)

"""
def recursion(lvl, line):
	if str(lvl) in line:
		if '!(' in line[:2] and line[-1] == ')':
			negation = 0
			line = line[2:]
		else:
			negation = 1
		for p in prec:
			elems = line.split(str(lvl) + p)
			if len(elems) > 1:
				tmp = []
				for elem in elems:
					tmp.append(recursion(lvl, elem))
					tmp.append(p)
				tmp.pop()
				line = '[' + ''.join(tmp) + ']' if not negation else ''.join(tmp)
				if (line[0] not in left or line[-1] not in right):
					return reval('(' + line + ')')
				return reval(line)
	if not any(c.isdigit() for c in line):
		return reval(line.replace('(', '').replace(')', ''))
	if line[0] == '(' and line[-1] == ')':
		line = line[1:]
	return recursion(lvl + 1, line)
"""

def recursion(l, s):
	print(str(l) + (l + 1) * '   ' + GREEN + "start" + EOC + " '" + s + "'")
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
				#print((l - 1) * '   ' + " found '" + str(l) + p + "'")
				#print((l + 1) * '   ' + ' ' + p + ' ', elems)
				for elem in elems:
					t.append(recursion(l, elem))
				#print((l - 1) * '   ' + ' ', end='')
				#print(t)
				#print((l + 1) * '   ' + ' ' + p + ' ', elems)
				#print((l - 1) * '   ' + ' ' + str(l) + p + ": \033[38;5;" + str(prec.index(p) + 3)  + "m wow found it " + EOC)
					##s = 'not(' + ''.join(t) + ')'
				s = ' '.join(t) + (e - 1) * (' ' + p)
				if not n:
					s += ' !'
				#print()
				print((l + 1) * '   ' + RED + " end  " + EOC + " '" + s + "'")
				#print("s: " + s)
				return s
			#print((l - 1) * '   ' + " could not find '" + str(l) + p + "'")
	if not any(c.isdigit() for c in s):
		print((l + 1) * '   ' + ORANGE + " end  " + EOC + " '" + s + "'")
		#for c in s:
			#if c.isupper():
				#print(l * '   ' + "creating op '" + ORANGE + c + "&1" + EOC + "'")
				#break
		if s[0] == '!':
			return s[1] + " !"
		return s.replace('(', '').replace(')', '')
	if s[0] == '(' and s[-1] == ')':
		s = s[1:-1]
	return recursion(l + 1, s)

"""def brackets(s):
	v = 0
	level = []
	stack = []
	print(s)
	for i in s:
		if i.isspace():
			continue
		elif i.isalpha():
			level.append(i)
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
	return ret"""


"""def reval(s):
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
	return ''.join(level)"""

"""def rpn(s):
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
	return ' '.join(rpn)"""
