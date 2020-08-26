# Stella Kim
# Assignment 9: Advanced Language Constructs

"""PNG discovery command line program using recursion."""

import argparse
import os


def parse_cmd_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Search for PNG files.')
    parser.add_argument('-i', '--input', help='specify parent directory',
                        default='./', required=True)
    return parser.parse_args()


def png_search(directory, results):
    """Return a list of lists of PNG files"""
# As output, it will return a list of lists structured like this:
# [“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[], etc]
    files_list = os.listdir(directory)
    dir_list = []
    for item in files_list:
        filepath = os.path.join(directory, item)
        path_no_filename = os.path.split(filepath)
        if os.path.isdir(filepath):
            png_search(filepath, results)
        elif path_no_filename[0] in results and item.endswith('.png'):
            dir_list.append(item)
        elif not path_no_filename[0] in results and item.endswith('.png'):
            results.append(path_no_filename[0])
            dir_list.append(item)
    if dir_list:
        results.append(dir_list)
    return results


if __name__ == '__main__':
    ARGS = parse_cmd_arguments()
    RESULTS = []
    PNG_LIST = png_search(ARGS.input, RESULTS)
    print(RESULTS)
