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
