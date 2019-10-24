#!/usr/bin/env python3

# Russell Felts
# Assignment 9 Recursion

"""
Use recursion to find all the pgn files regardless of directory depth
"""

import argparse
import os


def parse_cmd_arguments():
    """ Parse input """
    parser = argparse.ArgumentParser(description='Find png files.')
    parser.add_argument('-i', '--input', help='parent directory', required=True)

    return parser.parse_args()


# Get a list of items (files and directories) in the directory
def get_png_files(directory):
    """ Get list of png files in the current directory """
    # Main list for storing the path to the current directory and it's list of files
    final_png_list = []
    for root, current_dir, files in os.walk(directory, topdown=True):
        for temp_d in current_dir:
            # print("Directory", temp_d)
            get_png_files(temp_d)
        # List for temporarily storing the list offiles in the current directory
        temp_file_list = []
        for temp_f in files:
            # print("File ", temp_f)
            # Could verify the file extension but for the assignment currently
            # there are only png files
            temp_file_list.append(temp_f)
        # Add the path to the current directory and it's list of files to the final list
        if temp_file_list:
            final_png_list.append([root, temp_file_list])
    # print("PNG list ", png_list)
    return final_png_list


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    PNG_LIST = get_png_files(ARGS.input)
    print("PNG list ", PNG_LIST)
