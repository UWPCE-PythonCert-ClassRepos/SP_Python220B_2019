'''
module find png files in a given directory
'''

import os
import os.path

def png_discovery(path):
    '''function that makes a list of all pngs in a given directory and
    subdirectories (without recursion)'''
    output = []
    for dirpath, filenames in os.walk(path):
        png_files = []
        for file in filenames:
            if file.lower().endswith('.png'):
                png_files.append(file)
        if png_files:
            output.append(dirpath)
            output.append(png_files)
    return output

#os.walk() doesn't require recursion to complete assignment
#use another method

PNG_DICT = {}

def png_disc_recursive(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and item.lower().endswith('.png'):
            if path in PNG_DICT.keys():
                PNG_DICT[path].append(item)
            else:
                PNG_DICT[path] = [item]
        elif os.path.isdir(item_path):
            png_disc_recursive(item_path)
    png_list = PNG_DICT.items()
    return png_list

if __name__ == '__main__':
    SOL = png_disc_recursive(input('directory:'))
    print(SOL)
