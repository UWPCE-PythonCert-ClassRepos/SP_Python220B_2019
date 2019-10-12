#! /usr/bin/env python3

"""
HP Norton keeps pictures of all their furniture in png files that are stored on
their file server. They have a very crude program that starts by discovering
all directories on the server and then looking in each of those for the png
files. They have discovered a problem, though:
png files are not found when they are stored in directories that are more than
one level deep from the root directory.
Your job is to write a png discovery program in Python, using
recursion, that works from a parent directory called images provided on the
command line.
The program will take the parent directory as input. As output,
it will return a list of lists structured like this:
[“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[], etc]
"""
import os as path

def gather_files(root_directory, file_type='png'):
    """
    Search from the root directory for all png files
    """
    print("Searching root: %s for %s file type" %(root_directory, file_type))
    files = path.listdir(root_directory)
    files_filtered = [i for i in files if i.endswith(file_type)]

    for file_item in files_filtered:
        print(":: %s" %(file_item))

    gathered_files = [root_directory, files_filtered]

    return gathered_files



if __name__ == "__main__":
    gather_files(path.getcwd())
