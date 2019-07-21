"""
Module for locating all *.png files starting in a parent directory to
the final root directory.
"""
#pylint: disable=len-as-condition

import os

def png_locator(path):
    """Locate all of the *.png files in a given directory"""

    list_output = []

    for dir_path, dir_names, file_names in os.walk(path):
        if dir_names:
            for directory in dir_names:
                png_locator(directory)
        for file in file_names:
            png_files = []
            png_files = [file for file in file_names if '.png' in file]

            # Checks for *.png files in the directory before adding to output.
            if len(png_files) > 0:
                list_output.append(dir_path)
                list_output.append(png_files)

    return list_output

if __name__ == '__main__':
    DIRECTORY_PATH = os.getcwd()
    LIST_PNG_FILES = png_locator(DIRECTORY_PATH)
    print(LIST_PNG_FILES)
