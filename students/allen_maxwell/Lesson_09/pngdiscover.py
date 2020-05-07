'''Searches for png files'''
import os
import argparse

def parse_cmd_arguments():
    '''Gets the path to search for png files'''
    parser = argparse.ArgumentParser(description='Find png files')
    parser.add_argument('-i', '--input', help='Parent directory to search for png files',
                        default='./', required=False)
    return parser.parse_args()

def find_png(directory):
    '''Searches for png files within the parent directory'''
    results = []
    for root, folders, files in os.walk(directory):
        png_files = []
        for item in files:
            if item.endswith('.png'):
                png_files.append(item)
        if png_files:
            results.append(root)
            results.append(png_files)
        for folder in folders:
            find_png(folder)
    return results

if __name__ == '__main__':
    ARGS = parse_cmd_arguments()
    PNG_LIST = find_png(ARGS.input)
    print(PNG_LIST)
