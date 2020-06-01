""" This module returns a list of names of .png files in a directory """

import os

def find_png(folder_to_search):
    """ This function adds .png files to a list and calls again if there are sub directories """
    local_list = []
    for root, dirs, files in os.walk(folder_to_search):
        file_list = []
        for file in files:
            if file.lower().endswith('.png'):
                file_list.append(file)
        if file_list:
            local_list.append(root)
            local_list.append(file_list)
        for subdirectory in dirs:
            find_png(subdirectory)

    return local_list

if __name__ == '__main__':
    FOLDER = 'images'
    PING_LIST = find_png(FOLDER)
    print(PING_LIST)
