#!/usr/bin/env python3
"""
Module for searching through a directory for png files
"""
import argparse
import os


def parse_cmd_arguments():
    """
    Gather arguments from command line.
    """
    parser = argparse.ArgumentParser(description='List all png.')
    parser.add_argument('-i', '--input', help='input images parent directory', required=True)
    return parser.parse_args()


def png_search(directory):
    """
    Look recursively through top level directory and find all png files. Return a list of lists
    where each top list contains the path to the png and a list of the png files at that path
    """
    all_png_list = []
    for root_dir, child_dirs, files in os.walk(directory, topdown=True):
        for next_directory in child_dirs:
            png_search(next_directory)
        cur_dir_png_list = []
        for file_name in files:
            if file_name.lower().endswith('png'):
                cur_dir_png_list.append(file_name)
        if cur_dir_png_list:
            all_png_list.append([root_dir, cur_dir_png_list])
    return all_png_list


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    LIST_PNG_FILES = png_search(ARGS.input)
    print(LIST_PNG_FILES)
