import argparse
import sys
from constants import *
import logging

def config_logging(loglevel):
	numeric_level = getattr(logging, loglevel.upper(), None)
	if not isinstance(numeric_level, int):
		raise ValueError(loglevel)
	logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',\
			datefmt='%d-%b-%y %H:%M:%S', level=numeric_level)


def parse_args():
	"""
		:return: ArgumentParser object containing every argument passed to the program

		Basic argument checker
	"""
	options = argparse.ArgumentParser()
	options.add_argument("-i", "--input", required=True, help="path to input file")
	options.add_argument("-l", "--log", type=str, default='info', help="logging level")
	options.add_argument('-s', '--skip', action='store_true', help="do not necessarily respect unused rules")
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

def	check_recursion_coord(rpn_idx, sub_queries):
	for elem in sub_queries:
		for coord in elem.coord:
			if rpn_idx[0] == coord:
				return True
	return False


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


def check_valid_path(file_path):
	"""
		:param file_path(string): file path to check

		Just checking the path validity of a file
	"""
	try:
		fd = open(file_path, "r+")
	except FileNotFoundError:
		sys.exit(print("File does not exist, please enter a valid path."))

def precedence(line):
	"""
		:line:		line content (equation)

		Applying a depth(int) to all operators present in the current equation
		to later be able to split in the right order and respect the presedence of each operator
		Example: A+(B+C) --> A0+B1+C
	"""
	levels = []
	depth = 0
	stack = []
	for elem in line:
		if elem.isalpha():
			levels.append(elem)
		elif elem in pprec:
			levels.append(str(depth) + elem)
		elif elem in lleft:
			depth += 1
			stack.append(elem)
		elif elem in rright:
			if not stack or lleft[rright.index(elem)] != stack[-1]:
				return None
			depth -= 1
			stack.pop()
		elif elem == '>':
			levels.append(elem)
		elif stack:
			return None
	return None if stack else ''.join(levels)

def rpn(depth, line):
	if str(depth) in line:
		for p in pprec:
			elems = line.split(str(depth) + p)
			e = len(elems)
			if e == 1:
				continue
			logging.debug(str(depth) + (depth + 1) * '   ' + GREEN + "start" + EOC + " '" + line\
					+ "'" + ' ' + p + str(elems))
			if p == '!':
				logging.debug((depth + 1) * '   ' + YELLOW + "  start" + EOC + " '" + elems[0] + "'")
				logging.debug((depth + 1) * '   ' + ORANGE + "  end  " + EOC + " '" + elems[0] + "'")
				return rpn(depth, elems[1]) + ' !'
			t = []
			for elem in elems:
				t.append(rpn(depth, elem))
			line = ' '.join(t) + (e - 1) * (' ' + p)
			logging.debug(str(depth) + (depth + 1) * '   ' + RED + "end  " + EOC + " '" + line + "'")
			return line
	if not any(c.isdigit() for c in line):
		logging.debug((depth + 1) * '   ' + YELLOW + "  start" + EOC + " '" + line + "'")
		logging.debug((depth + 1) * '   ' + ORANGE + "  end  " + EOC + " '" + line + "'")
		return line
	logging.debug(str(depth) + (depth + 1) * '   ' + "none")
	return rpn(depth + 1, line)
