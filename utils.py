import argparse
import sys


def parse_args():
    """
        :return: ArgumentParser object containing every argument passed to the program

        Basic argument checker
    """
    options = argparse.ArgumentParser()
    options.add_argument("-i", "--input", help="path to input file")
    args = options.parse_args()
    return args


def find_fact_and_append_coord(name, fact_names, new_coord):
    """
        :param name(string)                 : name of the fact we want the coordinates to be updated
        :param fact_names(list of strings)  : list of facts already encountered
        :param new_coord(tuple(x, y))       : the new coordinates to add to a already existing fact

        :return: updates fact_names with the new coordinates
    """
    index = [elem.name for elem in fact_names].index(name)
    fact_names[index].coord.append(new_coord)
    return fact_names


def check_elem_not_in_fact_names(elem, fact_names):
    """
        :param elem(string)                 : name of fact we want to find or not inside the fact_names
        :param fact_names(list of strings)   : list of facts already encountered

        :return(bool): False if the elem is already inside fact_names or True if it's not
    """
    try:
        _ = [elem.name for elem in fact_names].index(elem)
    except ValueError:
        return True
    return False


def check_valid_path(file_path):
    """
        :param file_path(string): file path to check

        Just checking the path validity of a file
    """
    try:
        fd = open(file_path, "r+")
    except FileNotFoundError:
        sys.exit(print("File does not exist, please enter a valid path."))


def check_line_type(line):
    if line[0] == '#':
        return "Comment"
    elif line[0] == '?':
        return "Query"
    elif line[0] == "=":
        return "Initial Facts"
    elif line[0].isupper():
        return "Equation"
    else:
        return "Error"
