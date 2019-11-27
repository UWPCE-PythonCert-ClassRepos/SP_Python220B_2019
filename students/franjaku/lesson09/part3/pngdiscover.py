"""
Lesson 09 part 3

    Make a recursive function to find the png files in a directory.
"""

import os


def find_pictures(cur_dir):
    """
    Recursive function to find pictures from the root directory
    returns a list of lists structured as follows
    """
    png_found = []
    return_list = []

    for item in os.scandir(cur_dir):
        if item.name.endswith('.png'):
            png_found.append(item.name)
        if item.is_dir():
            l2 = find_pictures(cur_dir+'\\'+item.name)
            return_list = return_list + l2
    return [cur_dir, png_found] + return_list


if __name__ == "__main__":
    final_list = find_pictures(os.getcwd())
    for item in final_list:
        print(item)
