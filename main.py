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

	if options.und:
		for elem in exsys.facts:
			if elem.cond is None:
				elem.cond = False
				utils.logging.debug("set:%s", elem)
	exsys.log(utils.logging.debug)

	exsys.result()
