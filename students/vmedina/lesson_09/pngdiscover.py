"""
Victor Medina
Assignment 9: Recursive PNG read
"""
import glob
import os
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

png_list = []


def find_png(path):
    """search for png files"""

    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            find_png(os.path.join(path, file))
        elif file.endswith('png'):
            png_list.append(file)
    return png_list


if __name__ == '__main__':
    print(find_png(os.getcwd()))
