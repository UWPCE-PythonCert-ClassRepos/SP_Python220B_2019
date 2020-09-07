#!/usr/bin/env python3
'''
This program will take the parent directory as input.
As output, it will return a list of lists
([“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[], etc])
with all png files
'''

import os

FILELIST = []

def getpngfiles(filepath):
    '''Uses recursion to find all png files
       and their filepaths'''
    FILELIST.append(filepath)
    FILELIST.append([])
    file_location = FILELIST.index(filepath)
    for file in os.scandir(filepath):
        if file.name.endswith('.png'):
            png_location = file_location + 1
            FILELIST[png_location].append(file.name)
        elif file.is_dir():
            getpngfiles(filepath + '/' + file.name)
    return FILELIST

if __name__ == '__main__':
    folder = os.getcwd()+'/data'
    print(folder)
    png_files = getpngfiles(folder)
    print(png_files)
