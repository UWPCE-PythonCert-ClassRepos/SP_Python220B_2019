'''Module to find files in subdirectories'''
# Advanced Programming in Python -- Lesson 9 Assignment 1
# Jason Virtue
# Start Date 3/06/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name,too-few-public-methods,wrong-import-order,singleton-comparison,too-many-arguments,logging-format-interpolation,too-many-locals,no-else-return,unused-variable,redefined-outer-name

import argparse
import logging
import os

def parse_cmd_arguments():
    """Reads parameters from command line
       Command line   python -m pngdiscover --dir ./images
       -d = directory
    """
    parser = argparse.ArgumentParser(description='Process data')
    parser.add_argument('-d', '--dir', help='directory path of images', required=True)
    logging.info("End to parsing arguments from command line")
    return parser.parse_args()

def get_filepaths(directory):
    """
    Read file directory to find files and list directory and file names
    """
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root)
            file_paths.append(filepath)
            for filename in files:
                filepath = os.path.join(filename)
                file_paths.append(filepath)
    return file_paths

def main():
    """Main function to execute commands"""
    ARGS = parse_cmd_arguments()
    full_file_paths = ARGS.dir
    print(get_filepaths(full_file_paths))

if __name__ == "__main__":
    main()
