RED = '\033[38;5;1m'
GREEN = "\033[38;5;2m"
YELLOW = '\033[38;5;3m'
BLUE = '\033[38;5;4m'
EOC = '\033[0m'

class ExSys:
	def __init__(self):
		self.facts = []
		self.rules = []

	def get_fact(self, c):
		for i in self.facts:
			if c is i.c:
				return i
	
	def print_facts(self, pos):
		for i in self.facts:
			i.print(pos)

class Fact:
	def __init__(self, c):
		self.c = c
		self.cond = 0
		self.set = 0
		self.list = []
		self.req = 0

	def switch(self):
		self.cond = 1 if self.cond is 0 else 0
		self.set = not self.set

	def print(self, l):
		print("   '" + (YELLOW if self.req else '') + self.c + EOC + "' - '", end='')
		if self.set:
			print((GREEN + "True " if self.cond else RED + "False") + EOC, end='')
		else:
			print(("True " if self.cond else "False"), end='')
		if l:
			print("' - ", end='')
			print(self.list)
		else:
			print("'")

	def __and__(self, other):
		return self.cond & other.cond
	def __or__(self, other):
		return self.cond | other.cond
	def __xor__(self, other):
		return self.cond ^ other.cond

class Op:
	def __init__(self, p, o, q):
		self.p = p
		self.o = o
		self.q = q
		self.n = 0
		self.c = 0

class Rule:
	def __init__(self):
		self.i = Fact('1')
		self.f = []
		self.o = []

	def print(self):
		l = len(self.f)
		if l is 0:
			return print('undefined rule')
		print('rule is: ' + l * '(' + self.i.c, end='')
		for i in range(0, l):
			print(self.o[i] + self.f[i].c + ')', end='')
		print()
