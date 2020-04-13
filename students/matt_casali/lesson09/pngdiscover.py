#!/usr/bin/env python3

"""
Find all .png files
"""

# pylint: disable= C0103

import os
import argparse


def get_path():
    """
    Function to get path for input path directory
    """
    parser = argparse.ArgumentParser(description="Directory to search for png files")
    parser.add_argument("-i", "--input", required=True, type=str)

    return parser.parse_args()


def get_files(path, png_list):
    """
    Searches for file paths and png files using recursion, appends to list.
    """
    temp_list = []
    with os.scandir(path) as scanner:
        for file_path in scanner:
            if file_path.is_dir():
                get_files(file_path.path, png_list)
            elif file_path.name.endswith(".png"):
                temp_list.append(file_path.name)
    png_list.append(path)
    png_list.append(temp_list)


if __name__ == "__main__":
    args = get_path()
    png_files = []
    get_files(args.input, png_files)
    print(png_files)
