# -*- coding: utf-8 -*-
"""
Created on Tue May 21 20:47:09 2019

@author: Laura.Fiorentino
"""

"""list jpg files and their paths"""
import os


def find_jpg(path):
    """search for jpg files"""
    path_list = []
    for root, dirs, files in os.walk(path):
        file_list = []
        for file in files:
            if '.png' in file:
                file_list.append(file)
        if file_list:
            path_list.append(root)
            path_list.append(file_list)

    return path_list


if __name__ == '__main__':
    JPG_LIST = find_jpg(os.getcwd())
    print(JPG_LIST)
    print(len(JPG_LIST))
