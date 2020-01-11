""" This module returns a list of names of .png files in a directory """

import os

def what_files(folder_to_search):
    for root, dirs, files in os.walk(folder_to_search):
        for file in files:
            if file.endswith('.png'):
                print(os.path.join(root, file))

if __name__ == '__main__':
    folder = 'search_directory'
    what_files(folder)