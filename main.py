import utils
import parseur
import sub_queries as sub_q
import itertools

if __name__ == "__main__":
	options = utils.parse_args()
	utils.config_logging(options.log)
	utils.check_valid_path(options.input)
	exsys = parseur.Exsys(options.input)
	exsys.get()
	exsys.init_sort(options.skip)
	exsys.log(utils.logging.info)

	exsys.run()
	for elem in exsys.facts:
		if elem.und:
			elem.set(None)
	exsys.result()
