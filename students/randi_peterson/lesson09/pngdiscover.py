"""Finds the location of PNG files"""

import os


def find_pics(path):
    """Search for PNG files in given path"""
    result = []
    for root, dirs, files in os.walk(path):
        png_list = []
        for each_file in files:
            if each_file.lower().endswith('.png'):
                png_list.append(each_file)
        if len(png_list) > 0:
            #   Returns the location and files found
            result.append(root)
            result.append(png_list)

        for directory in dirs:
            find_pics(directory)

    return result


if __name__ == '__main__':
    PNG_FILES = find_pics(input("Where should I look?"))
    print(PNG_FILES)
