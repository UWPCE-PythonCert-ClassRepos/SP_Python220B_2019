#!/usr/bin/env python
"""
L09 recursion:

HP Norton keeps pictures of all their furniture in png files that are stored on their file server.
They have a very crude program that starts by discovering all directories on the server and then
looking in each of those for the png files. They have discovered a problem, though: png files are
not found when they are stored in directories that are more than one level deep from the root
directory. Your job is to write a png discovery program in Python, using recursion, that works from
a parent directory called images provided on the command line. The program will take the parent
directory as input. As output, it will return a list of lists structured like this:
[“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[], etc]
The program must be called pngdiscover.py
"""

# import logging
import os
from os.path import isdir as isdir
from os.path import isfile as isfile

IMAGE_PATH = os.getcwd() + '/' + 'images/'
ALL_SEARCH_PATHS = [IMAGE_PATH]
FINAL_LIST = []

# logging.basicConfig(level=logging.INFO)
# LOGGER = logging.getLogger(__name__)
# LOGGER.info('Logger initialized')


def read_directory(search_path):
    """
    Read the directory and handle the resulting subfolders and files appropriately.
    """
    # LOGGER.info(f'search_path is {search_path}')
    global FINAL_LIST
    global ALL_SEARCH_PATHS
    local_image_sequence = []

    there_is_png = False
    for thing in os.listdir(search_path):
        # LOGGER.info(f'thing is {thing}')
        # LOGGER.info(f'full path is {search_path + thing}')
        if isfile(search_path + thing) and thing[-4:] == '.png':
            # LOGGER.info(f'its a png: {thing}')
            there_is_png = True
            local_image_sequence.append(thing)
            # LOGGER.info(f'local_image_sequence: {local_image_sequence}')
        if isdir(search_path + thing):
            # LOGGER.info(f'its a dir: {thing}')
            ALL_SEARCH_PATHS.append(search_path + thing + '/')
    ALL_SEARCH_PATHS.pop(0)
    # LOGGER.info(f'ALL_DIRECTORIES after pop(0): {ALL_SEARCH_PATHS}')
    if there_is_png is True:
        FINAL_LIST.append(search_path)
        FINAL_LIST.append(local_image_sequence)
        # LOGGER.info(f'FINAL_LIST: {FINAL_LIST}')
    if ALL_SEARCH_PATHS != []:
        handle_recursive_calls(ALL_SEARCH_PATHS)
    else:
        print(FINAL_LIST)


def handle_recursive_calls(search_paths):
    """
    Cycle through the sequence of directories to search, and send each directory to the
    read_directory function.
    """
    # LOGGER.info(f'in handle_recursive_calls')
    for search_path in search_paths:
        # LOGGER.info(f'directory is {directory}')
        read_directory(search_path)
    return FINAL_LIST


if __name__ == '__main__':
    handle_recursive_calls(ALL_SEARCH_PATHS)
