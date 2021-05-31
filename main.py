import utils
import parseur
import sub_queries as sub_q

if __name__ == "__main__":
	options = utils.parse_args()
	utils.config_logging(options.log)
	utils.check_valid_path(options.input)
	exsys = parseur.Exsys(options.input)
	exsys.get()
	exsys.init_sort(options.skip)
	exsys.log(utils.logging.info)

	utils.logging.info("Run -------------------- start")
	exsys.run()
	utils.logging.info("Run -------------------- end")

	## IGNORE EVERYTHING ABOVE -----------------------------------------
	#utils.logging.info(exsys)
	#utils.logging.info("Evaluate --------------- start")
	## How to declare the sub_queries instance and call it for one query
	#exsys.rpn.sort(key=len)
	#for elem in exsys.rpn:
	#	utils.logging.info(elem)
	#s = sub_q.Evaluate(exsys)
	#for query in exsys.queries:
	#	sub = s.evaluate_equation(query)
	#	utils.logging.info("{} for {}".format(sub, query))
	#utils.logging.info("Evaluate --------------- end")
	exsys.result()
