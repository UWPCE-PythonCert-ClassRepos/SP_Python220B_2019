#!/usr/bin/env python3
"""Command line script to create a list of png files in a given parent directory
and all sub-folders then displays the list on the screen"""

import argparse
import os


def parse_cmd_arguments():
    """Command line input argument parser"""
    parser = argparse.ArgumentParser(description="find PNG Files")
    parser.add_argument("-d", "--directory", help="input parent directory path", required=True)
    return parser.parse_args()


def png_file_finder(parent_directory):
    """Searches a provided directory and all sub folders for .png files to
    return a dictionary object with the path and filename"""
    for entry in os.listdir(parent_directory):
        current_path = os.path.join(parent_directory, entry)
        if os.path.isfile(current_path) and entry.endswith(".png"):
            if parent_directory in PNG_DICT.keys():
                PNG_DICT[parent_directory].append(entry)
            else:
                PNG_DICT[parent_directory] = [entry]
        elif os.path.isdir(current_path):
            png_file_finder(current_path)
    return PNG_DICT


def convert_to_list(dictionary):
    """takes a dictionary object, converts it to a list """
    list_from_dictionary = []
    for key, val in dictionary.items():
        list_from_dictionary.append(key)
        list_from_dictionary.append(val)
    return list_from_dictionary


if __name__ == "__main__":
    PNG_DICT = {}
    ARGS = parse_cmd_arguments()
    DATA = png_file_finder(ARGS.directory)
    print(convert_to_list(DATA))
