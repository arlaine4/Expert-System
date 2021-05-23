import sys
import logging
import datetime
import re
from enum import Enum
from testfunc import *
from classes import *

def log():
	if logging.getLogger().isEnabledFor(logging.DEBUG):
		logging.debug('_' * (logw - 3) + ' rule(s) ' + '_' * (logw - 3))
		for orig, rule in zip(origs, rules):
			if not rule:
				if len(orig) > logw:
					logging.debug(' ' * (logw - len(orig)) + orig[:logw - 3] + '... | solved')
				else:
					logging.debug(' ' * (logw - len(orig)) + orig + ' | solved')
			elif len(orig) > logw or len(rule) > logw:
				logging.debug(' ' * (logw - len(orig)) + orig[:logw - 3] + '... | ' + rule[:logw - 3] + '...')
			else:
				logging.debug(' ' * (logw - len(orig)) + orig + ' | ' + rule)
		logging.debug('_' * logai + ' fact(s) ' + '_' * logai + '__' + '_' * logaq + ' query(ies) ' + '_' * logaq)
		logging.debug(' ' * (logbj % 2) + ' ' * logbi + init + ' ' * logbi + ' | ' + ' ' * logbq + query)

RED = '\033[38;5;1m'
GREEN = '\033[38;5;2m'
YELLOW = '\033[38;5;11m'
BLUE = '\033[38;5;12m'
DEFAULT = '\033[39m'
EOC = '\033[0m'

loglvl = ['n','d','i','w','e','c']
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d-%b-%y %H:%M:%S', level=loglvl.index('i')*10)

argv = len(sys.argv)
if argv < 2 or argv > 3:
	logging.error("bad input")
	logging.info("usage: python3 [-diwec] main.py input.txt")
	quit()
if argv is 2:
	try:
		f = open(sys.argv[1], 'r')
	except:
		logging.error("could not open '" + sys.argv[1] + "'")
		logging.info("usage: python3 [-diwec] main.py input.txt")
		quit()
elif sys.argv[1][0] != '-' or sys.argv[1][1] not in 'diwec':
	logging.error("bad input")
	logging.info("usage: python3 [-diwec] main.py input.txt")
	quit()
else:
	logging.getLogger().setLevel(loglvl.index(sys.argv[1][1])*10)
	try:
		f = open(sys.argv[2], 'r')
	except:
		logging.error("could not open '" + sys.argv[2] + "'")
		logging.info("usage: python3 [-diwec] main.py input.txt")
		quit()

logging.debug('reading file')
lines = f.read().split('\n')
logging.debug('reading file...DONE\n')
f.close()

logging.debug('file parsing')
init = ''
query = ''
facts = []
rules = []
rulecnt = 0
for line in lines:
	if not line:
#		break
		continue
	logging.debug(line)
	if line[0] == '#':
		continue
	elif line[0] == '=':
		logging.debug("found initial fact(s)")
		init = line.split('#')[0]
		i = 1
		l = len(init)
		while i < l and init[i].isalpha():
			if not fact_exist(init[i], facts):
				facts.insert(0, Fact(init[i]))
			fact_set(init[i], 1, facts)
			i += 1
	elif line[0] == '?':
		logging.debug("found query(ies)")
		query = line.split('#')[0]
		i = 1
		l = len(query)
		while i < l and query[i].isalpha():
			if not fact_exist(query[i], facts):
				logging.error("query '" + query[i] + "' is not a fact!")
				quit()
			i += 1
	elif line[0].isupper() or "(!01".find(line[0]) != -1:
		logging.debug("found a rule")
		rulecnt += 1
		rules.insert(0, line.split('#')[0].strip())
		lc = ''
		for c in rules[0]:
			if c.isalpha():
				if not c.isupper():
					logging.error("lowercase fact name '" + c + "' detected")
					quit()
				if lc.isalpha():
					logging.error("bad fact name '" + lc + c + "' detected")
					quit()
				fact = fact_exist(c, facts)
				if not fact:
					facts.insert(0, Fact(c))
			elif c == '!':
				if lc not in " (":
					logging.error("bad condition '" + lc + c + "' detected")
					quit()
				lc = c
				continue
			elif c == '(':
				if lc == ')':
					logging.error("bad brackets '" + lc + c + "' detected")
					quit()
				lc = c
				continue
			elif c in " +|^)[]{}":
				lc = c
				continue
			elif c == '<':
				if not (lc == ' ' or lc.isalpha()):
					logging.error("bad character '" + lc + c + "' detected")
					quit()
				s = rules[0].split('<=>')
				rules[0] = s[0] + '=>' + s[1]
				rules.insert(0, (s[1] + ' => ' + s[0]).strip())
			elif c == '=':
				if not (lc == ' ' or lc == '<' or lc.isalpha()):
					logging.error("bad character '" + lc + c + "' detected")
					quit()
			elif c == '>':
				if lc != '=':
					logging.error("bad character '" + lc + c + "' detected")
					quit()
			else:
				logging.error("bad character '" + c + "' detected")
				quit()
			lc = c
	else:
		logging.error("bad line '" + line + "' detected")
		quit()
lines.clear()
if not init:
	init = "no initial facts declared"
if not query:
	query = "no queries declared"
logging.debug('file parsing..DONE\n')
rules.sort(key=lambda x: len(x))
origs = rules.copy()

logging.debug('translate rules')
for i in range(0, len(rules)):
	print(rules[i])
	temp = brackets(rules[i])
	print()
	if not temp:
		logging.error("brackets bad aligned in '" + rules[i] + "'")
		quit()
#	n = temp.find(' ')
#	m = temp.rfind(' ')
#	rules[i] = temp[n + 1:m]
	rules[i] = temp
	i += 1

opers = []
i = 0
for rule in rules:
	impl = rule.split('=>')
#	rule = recursion(2, impl[0])
	print(rule)
#	temp = recursion(int(impl[0][:n + 1]), impl[0][n + 1:]) + ''.join('=>' + recursion(int(impl[1][m + 1:]), impl[1][:m]))
	temp = recursion(0, impl[0]) + ''.join('=>' + recursion(0, impl[1]))
	print()
#	temp = rule + ''.join('=>' + recursion(2, impl[1]))
	for c in range(0, len(temp)):
		if not temp[c].isupper():
			continue
		fact = fact_exist(temp[c], facts)
		fact.list.append([i, c])
#	for c in temp:
#		if not c.isupper():
#			continue
#		fact = fact_exist(c, facts)
#		fact.list.append([i, temp.index(c)])
	rules[i] = temp
	i += 1

if logging.getLogger().isEnabledFor(logging.DEBUG):
	logw = 35
	i = len(init)
	if logw < i:
		logw = i
	q = len(query)
	if logw < q:
		logw = q 
	logai = int((logw - 8) / 2)
	logaq = int((logw - 11) / 2)
	logbj = int(logw - len(init))
	logbi = int(logbj / 2)
	logbq = int((logw - len(query)) / 2)

log()
logging.debug('translate rules..DONE\n')

a = Fact('A')
b = Fact('B')
a.print(0)
b.print(0)
print(a | b)
b.cond = 1
a.print(0)
b.print(0)
print(a | b)

tests = [Rule(), Rule(), Rule()]
tests[0].f.append(a)
tests[0].o.append('&')
tests[0].f.append(b)
tests[0].o.append('|')
tests[1].f.append(b)
tests[1].o.append('^')
tests[1].f.append(a)
tests[1].o.append('|')
for test in tests:
	test.print()

exsys = ExSys()
exsys.facts.append(Fact('B'))
exsys.facts.append(Fact('G'))
exsys.facts.append(Fact('A'))
exsys.facts.append(Fact('Y'))
exsys.facts.append(Fact('L'))
exsys.print_facts(0)
moll = exsys.get_fact('A')
moll.print(1)
moll.cond = 1
ok = exsys.get_fact('A')
ok.print(1)

oper = Op(None, None, None)
oper.c = exsys.get_fact(ok.c).cond
print(str(oper.c))
ok.cond = 0
print(str(oper.c))


quit()


#------------------------------------------------------------------------------------------------

logging.debug('applying initial fact(s)')
for c in init[1:]:
	fact = fact_exist(c, facts)
	if not fact:
		continue
	fact.req = 1
	for e in fact.list:
		rules[e[0]] = rules[e[0]][:e[1]] + '1' + rules[e[0]][e[1] + 1:]

log()
logging.debug('applying initial fact(s)..DONE\n')

results = []
helpers = []
facts.sort(key=lambda x: (x.set, len(x.list), x.c))
while (1):
	if not facts:
		break
	fact = facts.pop()
	if not fact.cond:
		break
	results.insert(0, fact)

cd = len(facts)
while(1):
	for e in fact.list:
		s = rules[e[0]].split("=>")
		try:
			f = 0
			el = eval(s[0])
			if el:
				for c in s[1]:
					if c.isupper():
						f += 1
				if f == 1:
					break
			else:
				for k in fact.list:
					if k[0] is e[0]:
						logging.debug("removing fact '" + fact.c + "' occurance from rule >" + rules[e[0]] + "<")
						fact.list.remove(k)
				logging.debug("marking rule >" + rules[e[0]] + "< as uesless")
				rules[e[0]] = 'useless'
		except:
			continue
	if f == 1:
		if e[1] > 0 and rules[e[0]][e[1] - 1] == ' ':
			logging.debug("setting single fact '" + fact.c + "' to be false >" + rules[e[0]] + "<")
			fact.cond = 0
		else:
			logging.debug("setting single fact '" + fact.c + "' to be true >" + rules[e[0]] + "<")
			fact.cond = 1
		fact.set = 1
		logging.debug("marking rule >" + origs[e[0]] + "< as solved")
		rules[e[0]] = 'solved'
		fact.list.remove(e)
		for e in fact.list:
			rules[e[0]] = rules[e[0]][:e[1]] + str(fact.cond) + rules[e[0]][e[1] + 1:]
		fact.list = []
		results.insert(0, fact)
		cd = len(facts)
		logging.debug("minimum turns left are " + str(cd) + '\n')
	elif f == 2:
		logging.debug("HERE it all starts... '" + fact.c + "'")
		facts.insert(0, fact)
		cd -= 1
		logging.debug("minimum tries left are " + str(cd) + '\n')
	else:
		logging.debug("CAN'T do anything about fact '" + fact.c + "' for the moment")
		facts.insert(0, fact)
		cd -= 1
		logging.debug("minimum tries left are " + str(cd) + '\n')


	if cd:
		print('Fact(s)')
		for fact in facts:
			fact.print(1)
		fact = facts.pop()
	else:
		break
	log()


facts.sort(key=lambda x: x.c)
print('UNdetermined Fact(s)')
for fact in facts:
	fact.print(0)

results.sort(key=lambda x: x.c)
print('determined Fact(s)')
for result in results:
	result.print(0)


print("\n" + brackets("(!(A + (X | V))) => R"))
print("\n" + brackets("C | D => !(X | V) + C"))
