"""Write a recursive program that works froma parent directory
as an input it takes a parent directory and as an output the path to the files
[“full/path/to/files”, [“file1.png”, “file2.png”,…]
"""
from os import listdir, getcwd


def png_finder(path, file_list):
    """recursive function to go through all the directories
    and find all the png files"""
    directories = []
    files = []
    for obj in listdir(path):
        if '.png' in obj:
            files.append(obj)
        else:
            directories.append(obj)
        if files:
            file_list.append([path, files])
    for directory in directories:
        new_directory = path + '\\' + directory
        png_finder(new_directory, file_list)
    return file_list


if __name__ == '__main__':
    for thing in png_finder(getcwd() + '\\data', []):
        print(thing)
