import utils
import parseur
import sub_queries as sub_q

if __name__ == "__main__":
	options = utils.parse_args()
	utils.check_valid_path(options.input)
	exsys = parseur.Exsys(options.input)
	exsys.get()

	exsys.init_sort(options.skip)

	utils.logging.info("Exsys ----------------------------- Exsys")
	utils.logging.info(exsys)
	utils.logging.info("RPN ------------------------------- start")
	for elem in exsys.rpn:
		utils.logging.info(elem)
	utils.logging.info("RPN ------------------------------- end")

	print(exsys, end="\n\n")
	print("RPN -------------------- start")
	for elem in exsys.rpn:
		print(elem)
	print("RPN -------------------- end")

	print("Run -------------------- start")
	exsys.run()
	for elem in exsys.facts:
		print(elem.name, elem.coord)
	print("Run -------------------- end")

	print("Evaluate --------------- start")
	# How to declare the sub_queries instance and call it for one query
	exsys.rpn.sort(key=len)
	s = sub_q.Evaluate(exsys)
	sub = s.evaluate_equation(exsys.queries[1])
	print("{} for {}".format(sub, exsys.queries[1]))
	print("Evaluate --------------- end")

