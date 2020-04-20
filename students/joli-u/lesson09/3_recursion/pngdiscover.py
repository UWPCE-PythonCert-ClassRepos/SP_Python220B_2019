"""
pngdiscover.py
Assignment 9
Joli Umetsu
PY220
"""
import argparse
from pathlib import Path

def parse_cmd_arg():
    """
    Parses user input
    """
    parser = argparse.ArgumentParser(description="Find png files.")
    parser.add_argument('-p', '--path', help='input directory path', required=False, \
                        default=Path.cwd())

    return parser.parse_args()


def find_png(parent):
    """
    Recursively finds .png files in parent directory
    """
    png_files = []
    for child in parent.iterdir():
        if child.suffix == ".png":
            if str(parent) in png_files:
                png_files[png_files.index(str(parent))+1].append(child.name)
            else:
                png_files.append(str(parent))
                png_files.append([child.name])

        elif child.is_dir():
            png_files.extend(find_png(child))

    return png_files


if __name__ == "__main__":
    ARG = parse_cmd_arg()
    print(find_png(ARG.path))
