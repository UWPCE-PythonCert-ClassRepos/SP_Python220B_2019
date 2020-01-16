""" This module returns a list of names of .png files in a directory """
import os

def what_png(folder_to_search):
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
            what_png(subdirectory)

    return local_list

if __name__ == '__main__':
    FOLDER = 'search_directory'
    PNG_LIST = what_png(FOLDER)
    print(PNG_LIST)
