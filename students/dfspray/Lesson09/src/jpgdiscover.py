"""
This program will find all the .jpg (or in my case, .png) files in the file directory system
"""

import os

def find_jpg(path):
    """This is the recursive function for discovering .jpg files"""
    path_list = []
    for root, directories, files in os.walk(path):
        file_list = []
        #In my version, all the pictures were .png not .jpg
        for file in files:
            if '.png' in file:
                file_list.append(file)
        #I added this if statement to omit paths to directories that don't have pictures
        if file_list != []:
            path_list.append(root)
            path_list.append(file_list)
        if directories:
            for directory in directories:
                find_jpg(directory)
    return path_list

if __name__ == '__main__':
    print(find_jpg(os.path.dirname(__file__)))
