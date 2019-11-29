""" Takes a path provided on command line and returns list of png files """

import os
import sys

def get_png_files(dir_name, output_list):

    """ Find png files within a directory structure """
    file_list = []

    # scandir supports context manager to handle end of iterator
    with os.scandir(dir_name) as check_dir:
        for entry in check_dir:
            if entry.is_dir():
                get_png_files(entry.path, output_list)
            elif entry.name.endswith("png"):
                file_list.append(entry.name)
    output_list.append(dir_name)
    output_list.append(file_list)

def main():

    """ Initiates the file search and prints the findings """
    output_list = []

    # Ensure the directory exists
    try:
        dir_name = sys.argv[1]
        if not os.path.exists(dir_name):
            print("Unable to find path provided: {}".format(dir_name))
            exit()
    except IndexError:
        print("Please provide a path to a directory that exists.")
        exit()

    # Search for files
    get_png_files(dir_name, output_list)
    print(output_list)

if __name__ == '__main__':
    main()
