"""
HP Norton keeps pictures of all their furniture in png files that are stored on their file
server. They have a very crude program that starts by discovering all directories on the server
and then looking in each of those for the png files. They have discovered a problem, though:
png files are not found when they are stored in directories that are more than one level deep
from the root directory. Your job is to write a png discovery program in Python, using
recursion, that works from a parent directory called images provided on the command line. The
program will take the parent directory as input. As output, it will return a list of lists
structured like this: [“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[],
etc] The program must be called pngdiscover.py
"""

import argparse
from os import walk
# import glob


def parse_cmd_arguments():
    """parse command string arguments"""
    parser = argparse.ArgumentParser(description='get parent directory')
    parser.add_argument('-p', '--path', help='full parent directory for images', required=True)
    return parser.parse_args()


def locate_images(path):
    """locate all png files in the directory and subdirectories of input path"""
    found = []
    for (dirpath, subdirs, filenames) in walk(path):
        locating = []

        for file in filenames:
            if file.lower().endswith(".png"):
                locating.append(file)
        if locating != []:
            found.append(dirpath)
            found.append(locating)

        for directory in subdirs:
            locate_images(directory)

    return found


if __name__ == '__main__':
    ARGS = parse_cmd_arguments()
    PNG_LIST = locate_images(ARGS.path)
    print(PNG_LIST)


# def locate_images(path):
#     for filename in glob.iglob(path + '\\**/*.png', recursive=True):
#         print(filename)
