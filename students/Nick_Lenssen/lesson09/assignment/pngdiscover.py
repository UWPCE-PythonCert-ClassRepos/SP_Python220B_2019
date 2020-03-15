"""
Module for locating all *.png files starting in a parent directory to
the final root directory.
"""
#pylint: disable=len-as-condition
#pylint: disable=W0102, E0602

import os

def png_locator(directory, png_name=None):
    """A recursive function to find jpg files within folders"""
    out = [directory, []]

    if png_name is None:
        png_name = []

    for file in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, file)):
            png_locator(os.path.join(directory, file), png_name)

        elif file.endswith('.png'):
            out[1].append(file)

    if out[1]:
        png_name.extend(out)

    return png_name

def parse_cmd_arguments():
    """separate argument line commands and their uses in the program"""
    parser = argparse.ArgumentParser(description='Import parent directory')
    parser.add_argument('-i', '--input', help='input file path', required=True)

    return parser.parse_args()

if __name__ == "__main__":
    #DIRECTORY_PATH = parse_cmd_arguments()
    DIRECTORY_PATH = os.getcwd()
    LIST_PNG_FILES = png_locator(DIRECTORY_PATH)
    print(LIST_PNG_FILES)
