import utils
from utils import *

class Operation:
	def __init__(self, p=None, q=None, o=None):
		self.p = p
		self.q = q
		self.o = o
		self.cond = None

	def __repr__(self):
		if self.cond is True:
			tmp = 2
		elif self.cond is False:
			tmp = 1
		else:
			tmp = 3
		return "\033[38;5;{}m{}{}\t{} {} {}".format(tmp, self.cond, EOC, self.p, self.o, self.q)

	def solve(self, pq, get_fact):
		stack = []
		for elem in pq.split():
			utils.logging.warning(elem)
			utils.logging.warning(stack)
			if elem[0].isalpha():
				f = get_fact(elem)
				stack.append(f)
			else:
				q = stack.pop()
				p = None if elem == '!' else stack.pop()
				o = Operation(p, q, elem)
		utils.logging.debug(stack)
