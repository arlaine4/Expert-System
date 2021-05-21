import utils
import parseur
import numpy


if __name__ == "__main__":
    options = utils.parse_args()
    utils.check_valid_path(options.input)
    parsing = parseur.Parsing(options.input)
    parsing.parsing_loop()
    #bonsoir
    #bonsoir
    #for elem in parsing.raw_content: print(elem, end='')
