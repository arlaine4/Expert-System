import utils
import parseur
import itertools

if __name__ == "__main__":
	options = utils.parse_args()
	utils.config_logging(options.log)
	utils.check_valid_path(options.input)
	exsys = parseur.Exsys(options.input)
	exsys.get()
	exsys.init_sort()
	exsys.log(utils.logging.info)

	exsys.run()
	exsys.result()
