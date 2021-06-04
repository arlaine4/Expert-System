from constants import *

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
