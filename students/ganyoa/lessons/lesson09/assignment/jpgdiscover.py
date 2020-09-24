'''
Advanced Programming in Python Lesson 9
Advance Language Constructs; resursion

pylint disabled warnings:
'''
import argparse
import os


def parse_cmd_arguments():
    '''
    Parse command line arguments
    :param input: requires Parent directory for PNG images
    '''

    parser = argparse.ArgumentParser(description='PNG file finder.')
    parser.add_argument('-d', '--directory', metavar='', help='Parent directory for PNG files', \
        required=True)
    return parser.parse_args()


def find_pngs(png_path):
    '''resursive function working through directory for png files'''
    png_list = []
    for root, dirs, files in os.walk(png_path):
        for file in files:
            if file.endswith('.png'):
                png_list.append(file)
        for current_dir in dirs:
            find_pngs(current_dir)
    return png_list


if __name__ == '__main__':
    ARG = parse_cmd_arguments()
    find_pngs(ARG.directory)
