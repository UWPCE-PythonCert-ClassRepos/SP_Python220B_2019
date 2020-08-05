#!/usr/bin/env python

'''
Lesson 9 Assignment: pngdiscover.py -
   - Recurses through a folder system and finds all of the .png files
     and returns them in a list of lists format
   - Command line argument (-f/-folder) will crawl through passed in folder name
'''

import os
import sys
import argparse

FILE_DICT = {}

def parse_command_arguments():
    '''Process the folder name that will be recursively searched through'''
    parser = argparse.ArgumentParser(description='Enter the folder name to search')
    parser.add_argument('-folder', '-f', type=str, default='', required=True,
                        help='Enter the folder name to crawl')
    try:
        return parser.parse_args()
    except TypeError:
        sys.exit()

def find_pngs(working_path):
    '''Searches a directory for subdirectories and .png files'''
    for item in os.listdir(working_path):
        full_path = working_path + '/' + item
        if item[-4:] == '.png':
            try:
                FILE_DICT[working_path].append(item)
            except KeyError:
                FILE_DICT[working_path] = [item]
        elif os.path.isdir(full_path):
            find_pngs(full_path) # Keep recurring this in all paths


def listify(dict_to_list):
    '''Turns the dictionary into a list of this format:
    [“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[], etc]'''
    file_collection = []
    for key, value in dict_to_list.items():
        file_collection.append(key)
        file_collection.append(value)
    return file_collection



if __name__ == '__main__':
    args = parse_command_arguments()
    start_path = './' + args.folder
    find_pngs(start_path)
    output_list = listify(FILE_DICT)
    print(f'Here is the list of lists of .pngs in {start_path}:\n')
    print(output_list)
