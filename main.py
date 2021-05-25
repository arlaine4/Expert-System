import utils
import parseur


if __name__ == "__main__":
	options = utils.parse_args()
	utils.check_valid_path(options.input)
	exsys = parseur.Exsys(options.input)
	exsys.parsing()

	exsys.facts.sort(key=lambda x: x.name)
	exsys.initials.sort(key=lambda x: x.name)
	exsys.queries.sort(key=lambda x: x.name)
	for elem in exsys.initials:
		elem.cond = True

	print(exsys, end="\n\n")
	print("RPN -------------------- start")
	for elem in exsys.rpn:
		print(elem)
	print("RPN -------------------- end")

	"""
	----------------------------------------------------
	RPNs are now correct
	Under hear I suppose, that you try to think about how do we want to
	solve stuff form here. I mean basically it "should" be straight forward like
	any other 'rpn' is solved. Only difference is that we don't have numbers
	but facts ('True'/'False') and the '!' operator is a bit special.

	The '!' works like this (in my brain):	#the test file 'mhm.txt' has some '!'operators inside
	input:		A + C => A + !G
	initials:	=AC
	queries:	?G

	left:		True + True		gives		True
	right:		True + !G		MUST be		True
				True + !False	=			True
			------->	G = False

	input:		A + C => A + !G
	rpn:		A C +  > A G ! +

	rpn:		A C +  > A G !   =			#the '!' takes ONLY 1 parameter, the 1 right before
	rpn:		____.  > A __. + =			#any other operator takes 2 param, the 2 right before
	rpn:		       > ______. =


	for example like this...
	.------------
	|
	|
	v
	"""
	print("Evaluate --------------- start")
	for elem in exsys.rpn:
		print(elem)
		exsys.evaluate(elem)
		print()
