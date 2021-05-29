import utils
import parseur


if __name__ == "__main__":
	options = utils.parse_args()
	utils.config_logging(options.log)
	utils.check_valid_path(options.input)
	exsys = parseur.Exsys(options.input)
	exsys.parsing()

	exsys.init_sort()

	utils.logging.info("Exsys ----------------------------- Exsys")
	utils.logging.info(exsys)
	utils.logging.info("RPN ------------------------------- start")
	for elem in exsys.rpn:
		utils.logging.info(elem)
	utils.logging.info("RPN ------------------------------- end")
