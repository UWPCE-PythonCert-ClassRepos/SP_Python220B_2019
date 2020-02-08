'''
This file searches returns all png files
in a specified directory and their file paths
'''

import os

FILE_LIST = []

def get_png_files(file_path):
    '''Method to use recursion to find all png files
       and their associated filepaths'''
    FILE_LIST.append(file_path)
    FILE_LIST.append([])
    file_location = FILE_LIST.index(file_path)
    for file in os.scandir(file_path):
        if file.name.endswith('.png'):
            png_location = file_location + 1
            FILE_LIST[png_location].append(file.name)
        elif file.is_dir():
            get_png_files(file_path + '/' + file.name)
    return FILE_LIST
