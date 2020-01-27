# Advanced Programming In Python - Lesson 9 Assignment 1.3: Recursion
# RedMine Issue - SchoolOps-15
# Code Poet: Anthony McKeever
# Start Date: 01/24/2019
# End Date: 01/25/2019

"""
Recursively crawls a folder structure looking for PNG files.
"""

import argparse
import os
import pathlib

from argparse import RawTextHelpFormatter

PARSER = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
PARSER.description = str("Recursively searches for PNG files in a " +
                         "given directory tree")
PARSER.add_argument("-search-dir",
                    help="The top directory of the tree to search",
                    required=True)
PARSER.epilog = str("Return format is a list containing the directory name " +
                    "followed by a list of PNG files found within it." +
                    "\nExample:" +
                    "\n\t[\"./images/\", []," +
                    " \"./images/couches\", [img1.png, img2.png]]]")


def crawl_folder(current_dir, list_files):
    """
    Recursively crawl a folder structure and return the list of folders
    and files in the following format.

    Return Value Example:
        ["./images/", [], "./images/couches/", ["img1.png", "img2.png"]...]

    :current_directory:     The directory to crawl.
    :list_files:            The list to store values to.
    """
    all_files = os.listdir(current_dir)
    list_pngs = []
    list_dirs = []

    for file_name in all_files:
        if pathlib.Path(file_name).suffix == ".png":
            list_pngs.append(file_name)

        else:
            potential_dir = os.path.join(current_dir, file_name)
            if os.path.isdir(potential_dir):
                # Ensure the directories get returned in alphabetical order by
                # reversing the order of them here to later be inserted in
                # reverse when appending to the final list of files and
                # directories.
                list_dirs.insert(0, potential_dir)

    if len(list_dirs) > 0:
        for directory in list_dirs:
            crawl_folder(directory, list_files)

    list_files.insert(0, list_pngs)
    list_files.insert(0, current_dir)

    return list_files


def main(args):
    """
    The main method of the application.
    """
    return crawl_folder(args.search_dir, [])


if __name__ == "__main__":
    ARGS = PARSER.parse_args()
    print(main(ARGS))
