"""Module jpgdiscover.py to discover all png files"""

from os.path import exists, join, abspath, isdir
from os import listdir
from pathlib import Path

def get_dir():
    """
    Get user input for the directory to use for searching directories
    for png files
    :return: Absolute path of the directory the user chooses
    """
    dir_path = input("Enter parent directory to search from\n>>>")
    while not exists(dir_path):
        dir_path = input("Not valid path, please try again\n>>>")
    full_path = abspath(dir_path)
    return full_path

def dir_recursion(path, items, stack_level=0):
    """
    Searches all directories recursively for an .png files ands them to
    a list right after their respective file path.

    :param path: current path to search
    :param items: the full_list of items to capture through a call stack
    :param stack_level: integer that determines location in the call stack
    :return: list of full paths followed by png files in that directory
    """
    full_list = items
    photo_list = list()

    subitems = listdir(path)

    for item in subitems:
        full_path = join(path, item)
        if isdir(full_path):
            stack_level += 1
            dir_recursion(full_path, full_list, stack_level)
            stack_level -= 1
            full_list.insert(0, full_path)

        else:
            if Path(item).suffix == '.png':
                print(item)
                photo_list.append(item)

    # Needed to prevent empty list inserted at the beginning
    if stack_level > 0:
        full_list.insert(0, photo_list)

    return full_list



if __name__ == '__main__':
    directory = get_dir()
    png_files = dir_recursion(directory, [])
    print(f"List of PNG's: {png_files}")
