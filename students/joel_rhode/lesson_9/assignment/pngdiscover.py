"""Module for listing all .png files in specified directory and subdirectories."""
from os import listdir, getcwd
from os.path import isdir, join
import argparse


def parse_cmd_arguments():
    """Define command line input arguments"""
    parser = argparse.ArgumentParser(description='Search for .pngs within directory')
    parser.add_argument('-d', '--directory', help='Root directory to search in',
                        default=getcwd())
    return parser.parse_args()


def discover_png(directory):
    """Returns list of all .png files within parent directory"""
    file_list = []
    file_list.append(directory)
    png_list = [file for file in listdir(directory) if file.endswith('.png')]
    file_list.append(png_list)
    for path in listdir(directory):
        path = join(directory, path)
        if isdir(path):
            file_list.append(discover_png(path))
    return file_list


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    print(discover_png(ARGS.directory))
