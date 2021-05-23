RED = '\033[38;5;1m'
ORANGE = '\033[38;5;208m'
GREEN = '\033[38;5;2m'
YELLOW = '\033[38;5;3m'
BLUE = '\033[38;5;4m'
MAGENTA = '\033[38;5;5m'
DEFAULT = '\033[39m'
EOC = '\033[0m'

def fact_exist(c, facts):
	for fact in facts:
		if c == fact.c:
			return fact

def fact_set(c, cond, facts):
	for fact in facts:
		if c == fact.c and not fact.set:
			fact.cond = cond
			fact.set = 1
			break

def fact_index(s):
	n = 0
	for c in s:
		if c.isupper():
			r = s.index(c)
			n += 1
	return r if n == 1 else -1

left = ["(","{","["] 
right = [")","}","]"]

def brackets(s):
	v = 0
	level = []
	stack = []
	m = v
	for i in s:
		if i.isspace():
			continue
		elif i.isalpha():
			level.append(i)
		elif i is '+':
			level.append(str(v) + '&')
		elif i in "^|":
			level.append(str(v) + i)
		elif i in left:
			v += 1
			m = v
			level.append('(')
			stack.append(i)
		elif i in right:
			if not stack or left[right.index(i)] is not stack[-1]: 
				return ''
			v -= 1
			level.append(')')
			stack.pop()
		elif i is '=' and stack:
			return ''
		elif i is '>':
#			level.insert(0, str(v) + ' ')
			level.append(i)
		else:
			level.append(i)
	if stack:
		return ''
#	level.append(' ' + str(v))
	ret = ''.join(level)
	print(ret)
	return ret

def reval(s):
	level = []
	n = 0
	for i in s:
		if i is '(':
			level.append(i)
		elif i is ')':
			level.append(i)
		elif i is '!':
			n = 1
			level.append('(not ')
		elif not i.isnumeric() or i is '1':
			level.append(i)
	if n:
		return ''.join(level) + ')'
	return ''.join(level)

prec = ['&', '|', '^']

def recursion(l, s):
	print(str(l) + (l + 1) * '   ' + GREEN + "start" + EOC + " '" + s + "'")
	if str(l) in s:
		if '!(' in s[0:2] and s[-1] is ')':
			n = 0
			s = s[2:-1]
		else:
			n = 1
		for p in prec:
			elems = s.split(str(l) + p)
			e = len(elems)
			if e > 1:
				t = []
#				print((l - 1) * '   ' + " found '" + str(l) + p + "'")
				print((l + 1) * '   ' + ' ', end='')
				print(elems)
				for elem in elems:
#					print("bra: " + brackets(elem.))
					t.append(recursion(l, elem))
					t.append(p)
				t.pop()
#				print((l - 1) * '   ' + ' ', end='')
#				print(t)
				print((l - 1) * '   ' + ' ' + p + ' ', end='')
				print(elems)
#				print((l - 1) * '   ' + ' ' + str(l) + p + ": \033[38;5;" + str(prec.index(p) + 3)  + "m wow found it " + EOC)
				if not n:
					s = 'not(' + ''.join(t) + ')'
				else:
					s = ''.join(t)
#				print()
				print((l + 1) * '   ' + RED + " end  " + EOC + " '" + s + "'")
#				print("s: " + s)
				return reval('(' + s + ')')
#			print((l - 1) * '   ' + " could not find '" + str(l) + p + "'")
	if not any(c.isdigit() for c in s):
		print((l + 1) * '   ' + ORANGE + " end  " + EOC + " '" + s + "'")
#		for c in s:
#			if c.isupper():
#				print(l * '   ' + "creating op '" + ORANGE + c + "&1" + EOC + "'")
#				break
		return reval(s)
	if s[0] is '(' and s[-1] is ')':
		s = s[1:-1]
	return recursion(l + 1, s)

#def recursion(l, p, i, s):
#	if str(l) not in s:
#		print((l - 1) * '   ' + RED + "end recursion for" + EOC + " '" + s + "'")
#		if l is 2:
#			print("['" + s + "']")
#			print("0" + prec[p] + ": " + BLUE + "wow found it " + EOC)
#			print()
#		return
#	print((l - 1) * '   ' + str(l) + prec[p] + ': ' + s)
#	elems = s.split(str(l) + prec[p])
#	if len(elems) > 1:
#		print((l - 1) * '   ' + "found '" + str(l) + prec[p] + "'")
#		print((l - 1) * '   ', end='')
#		print(elems)
#		for elem in elems:
#			recursion(l + 1, 0, i, elem)
#		print((l - 1) * '   ', end='')
#		print(elems)
#		print((l - 1) * '   ' + str(l) + prec[p] + ": " + BLUE + "wow found it " + EOC)
#		print()
##		return
##	if p is 2:
##		return
#	else:
#		print((l - 1) * '   ' + "could not find '" + str(l) + prec[p] + "'")
#	elems = s.split(str(l) + prec[p + 1])
#	if len(elems) > 1:
#		print((l - 1) * '   ' + "found '" + str(l) + prec[p + 1] + "'")
#		print((l - 1) * '   ', end='')
#		print(elems)
#		i += 1
#		for elem in elems:
#			recursion(l + i, 0, i, elem)
#		print((l - 1) * '   ', end='')
#		print(elems)
#		print((l - 1) * '   ' + str(l) + prec[p + 1] + ": " + YELLOW + "wow found it " + EOC)
#		print()
##		return
##	if p is 1:
##		return
#	else:
#		print((l - 1) * '   ' + "could not find '" + str(l) + prec[p + 1] + "'")
#	elems = s.split(str(l) + prec[p + 2])
#	if len(elems) > 1:
#		print((l - 1) * '   ' + "found '" + str(l) + prec[p + 2] + "'")
#		print((l - 1) * '   ', end='')
#		print(elems)
#		i += 1
#		for elem in elems:
#			recursion(l + i, 0, i, elem)
#		print((l - 1) * '   ', end='')
#		print(elems)
#		print((l - 1) * '   ' + str(l) + prec[p + 2] + ": " + GREEN + "wow found it " + EOC)
#		print()
##		return 
##	if l is 1:
##		return
#	else:
#		print((l - 1) * '   ' + "could not find '" + str(l) + prec[p + 2] + "'")
#	recursion(l - 2, 0, 0, s)


#	for e in x:
#	for e in x:
#		recursion(l + 1, '^', e)
#	for e in o:
#		recursion(l + 1, '|', e)
