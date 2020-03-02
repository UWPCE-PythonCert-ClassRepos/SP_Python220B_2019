""" Recursive PNG directory search """
# pylint: disable=unused-variable

import os
import argparse

from pathlib import Path


def parse_cmd_arguments():
    """ Parse Command Line Arguments

    Parses the provided commnad line argument
    -d --directory Directory to search
    """
    parser = argparse.ArgumentParser(description="Input the search directory")
    parser.add_argument(
        "-d", "--directory", help="Directory to search", required=True, type=str
    )

    return parser.parse_args()


def search_for_png(directory):
    """
    Search Directory for PNG
    Args:
        directory: Top level directory to search from
    Returns:
        list: list of lists of locations of png files
    """
    top_dir = Path(directory)
    path_list = []
    file_list = []
    for (dir_path, dir_names, file_names) in os.walk(top_dir):
        for file in file_names:
            if file.lower().endswith(".png"):
                file_list.append(file)
        if file_list:
            path_list.append(str(top_dir))
            path_list.extend([file_names])
        for names in dir_names:
            lower_path = search_for_png(top_dir / names)
            if lower_path:
                path_list.extend(lower_path)
        break
    return path_list


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    search_for_png(ARGS.directory)
