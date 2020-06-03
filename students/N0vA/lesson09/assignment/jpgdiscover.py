"""
Module to find all PNG files on HP Norton Server.
"""

import argparse
import os

def parse_cmd_arguments():
    """ Gets directory to find files """
    parser = argparse.ArgumentParser(description='Look for PNG Files')
    parser.add_argument('-d', '--directory', help='Directory to Find PNG Files', required=True)

    return parser.parse_args()

def find_png(path):
    """Locate all of the png files in a given directory"""

    output = []

    for root, dir_names, file_names in os.walk(path):

        png_files = []

        # Use recursion to go through parent director and any sub-directories.
        if dir_names:
            for directory in dir_names:
                find_png(directory)

        # Append list with any png files in the directory
        for file in file_names:
            if file.endswith('.png'):
                png_files.append(file)

        # Adds any pngs to output list
        if len(png_files) > 0:
            output.append(root)
            #output.append([root, png_files])
            output.append(png_files)

    return output

if __name__ == "__main__":

    ARGS = parse_cmd_arguments()
    print(find_png(ARGS.directory))
