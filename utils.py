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


def check_valid_path(file_path):
    """
        :param file_path(string): file path to check

        Just checking the path validity of a file
    """
    try:
        fd = open(file_path, "r+")
    except FileNotFoundError:
        sys.exit(print("File does not exist, please enter a valid path."))
