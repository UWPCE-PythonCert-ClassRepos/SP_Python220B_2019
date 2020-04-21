"""Return a list of pngs in each folder within a parent directory."""

import os
import argparse

pngs = [] # pylint: disable=invalid-name

def parse_cmd_arguments():
    """
    Command line interface.

    Required argument: -d (directory)
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory',
                        help='dir to search for pngs', required=True)

    return parser.parse_args()


def find_pngs(path):
    """Find pngs in each folder within a parent directory."""
    for root, dirs, files in os.walk(path):
        png_files = []
        for file in files:
            if file.endswith('.png'):
                png_files.append(file)
        if png_files:
            pngs.append(root)
            pngs.append(png_files)
        for directory in dirs:
            find_pngs(directory)
    return pngs


if __name__ == "__main__":
    args = parse_cmd_arguments() # pylint: disable=invalid-name
    find_pngs(args.directory)
