"""
Recursively search the directory and subdirectories
for .png files
"""
import argparse
import os
from pathlib import Path


def parse_cmd_arguments():
    """ Process command line options """
    parser = argparse.ArgumentParser(description='PNG File Discover')
    parser.add_argument('-dir', '--directory', help='directory to search', required=True)

    return parser.parse_args()


def scan_directory(path):
    """ Generator to scan the directory and the sub-directories recursively """
    for entry in os.scandir(path):
        if entry.is_file() and entry.name.endswith('.png'):
            yield entry.path
        if entry.is_dir():
            yield from scan_directory(entry.path)


def png_discover(path):
    """ Create the PNG discover list """
    png_dic = {}
    for file in scan_directory(path):
        png_file_path = Path(file)
        parent_directory = png_file_path.parent
        file_name = png_file_path.name
        if parent_directory not in png_dic:
            png_dic[parent_directory] = []
            png_dic[parent_directory].append(file_name)
        else:
            png_dic[parent_directory].append(file_name)

    png_list = []
    for key in png_dic:
        png_list.append(str(key))
        png_list.append(png_dic[key])

    return png_list


if __name__ == "__main__":
    arguments = parse_cmd_arguments()
    search_path = Path.cwd() / arguments.directory
    print(png_discover(search_path))
