"""The program will take the parent directory as input.
As output, it will return a list of lists structured like this:
 [“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[], etc]"""
import os
import argparse


def parse_cmd_arguments():
    """Defining command line input args"""
    parser = argparse.ArgumentParser(description='Getting parent directory as input')
    parser.add_argument('-i', '--input', help='input path', required=True)

    return parser.parse_args()


def locate_png(path):
    """
    locate png files recursively and put it into a list of lists
    """
    result = []
    for root, dirs, files in os.walk(path):
        filenames = []
        for file in files:
            if file.endswith('.png'):
                filenames.append(file)
        if filenames:
            result.append(root)
            result.append(filenames)
        elif dirs:
            for dir in dirs:
                locate_png(dir)
        elif root:
            for r in root:
                locate_png(r)
    return result


if __name__ == '__main__':
    args = parse_cmd_arguments()
    png_files = locate_png(args.input)
    print(png_files)

# python  pngdiscover.py -i /Users/Tian/Documents/PythonClass/Tianx/SP_Python220B_2019/students/Tianx/Lesson9/data