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
	options = argparse.ArgumentParser()
	options.add_argument("-i", "--input", required=True, help="path to input file")
	options.add_argument("-l", "--log", type=str, default='info', help="logging level")
	args = options.parse_args()
	return args


def check_valid_path(file_path):
	try:
		fd = open(file_path, "r+")
	except FileNotFoundError:
		sys.exit(print("File does not exist, please enter a valid path."))


def	test_valid_line(line):
	if line[-1] == '>':
		return False
	elif not ((line[0].isalpha() or line[0] in lleft) and "=>" in line):
		return False
	elif line.count('>') > 1 or line.count('<') > 1 or line.count('=') > 1:
		return False
	for elem in line:
		if elem in '0123456789':
			return False
	return True


def precedence(line):
	levels = []
	depth = 0
	stack = []
	last = ''
	for elem in line:
		if elem.isalpha():
			levels.append(elem)
		elif elem in pprec:
			if elem != '!' and last in pprec[:-1]:
				return None
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
		last = elem
	if stack:
		return None
	return ''.join(levels)

def rpn(depth, line):
	if str(depth) in line:
		for p in pprec:
			elems = line.split(str(depth) + p)
			e = len(elems)
			if e == 1:
				continue
			logging.debug("%d%s%sstart%s '%s' --- %c%s",
				depth, (depth + 1) * '   ', GREEN, EOC, line, p, str(elems))
			t = []
			for elem in elems:
				t.append(rpn(depth, elem))
			line = (' '.join(t) + (e - 1) * (' ' + p)).strip()
			logging.debug("%d%s%send  %s '%s'",
				depth, (depth + 1) * '   ', RED, EOC, line)
			return line
	if not any(c.isdigit() for c in line):
		logging.debug("%s  %sstart%s '%s'", (depth + 1) * '   ', YELLOW, EOC, line)
		logging.debug("%s  %send  %s '%s'", (depth + 1) * '   ', ORANGE, EOC, line)
		return line
	logging.debug("%d%snone", depth, (depth + 1) * '   ')
	return rpn(depth + 1, line)
