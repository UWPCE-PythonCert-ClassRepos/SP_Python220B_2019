'''
-ctrl + C exits a help()
-such a thing as "entry.path.endswith('.png')""
-on line 18 png_disco(dir_list.extend(entry.path)) would make more sense but it
doesnt work
'''
import os
from pprint import pprint

folder_of_interest = ".\\data"


def png_disco(path):
    dir_list = []
    png_list = []
    for entry in os.scandir(path):
        if entry.is_dir():
            dir_list.append(entry.path)
            dir_list.extend(png_disco(entry.path))
        else:
            png_list.extend([entry.path.rsplit('\\')[-1]])
    if png_list:
        '''if the png file list isn't empty append it to the main list'''
        dir_list.append(png_list)
    return dir_list


cool = png_disco(folder_of_interest)
pprint(cool)
