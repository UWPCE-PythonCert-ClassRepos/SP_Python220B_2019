# pylint: disable=invalid-name
"""Script to find PNG files."""
import argparse
from os import listdir
from os.path import join, isfile, isdir


def parse_cmd_arguments():
    """Parse arguments from the commandline."""
    parser = argparse.ArgumentParser(description='Find PNG files.')
    parser.add_argument('-i', '--input', required=True,
                        help='directory to search')
    return parser.parse_args()


def find_png(dirpath):
    """Recurse through directory to find PNG files."""
    # use a dict for collating data
    outlist = [dirpath, []]

    # loop through files in dir
    for f in listdir(dirpath):
        # if file, check if png and append
        if isfile(join(dirpath, f)):
            if f.lower().endswith(".png"):
                outlist[1].append(f)

        # if directory, recurse
        elif isdir(join(dirpath, f)):
            newlist = find_png(f"{dirpath}/{f}")
            outlist.extend(newlist)

    return outlist


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    PNG_LIST = find_png(ARGS.input)
    print(PNG_LIST)
