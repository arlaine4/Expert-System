import argparse
import sys


def parse_args():
    options = argparse.ArgumentParser()
    options.add_argument("-i", "--input", help="path to input file")
    args = options.parse_args()
    return args


def check_valid_path(file_path):
    try:
        fd = open(file_path, "r+")
    except FileNotFoundError:
        sys.exit(print("File does not exist, please enter a valid path."))
