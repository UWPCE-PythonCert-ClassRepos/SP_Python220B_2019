""" this utility finds all the PNG files and add to a list of lists  """

# pylint: disable=invalid-name

import logging
import os

logging.basicConfig(level=logging.INFO)

def find_png_files(directory):
    """ find png files in directory """

    list_of_lists = []

    # cur_dir=root, dirs=directories, files=files
    for cur_dir, dirs, files in os.walk(directory):
        logging.debug('Using: %s', cur_dir)
        file_list = []
        for f in files:
            if f.lower().endswith(".png"):
                file_list.append(f)
                logging.debug('Found file: %s', f)
        if len(file_list) > 0:
            logging.debug('Adding directory: %s', cur_dir)
            logging.debug('Adding file list: %s', file_list)
            list_of_lists.append(cur_dir)
            list_of_lists.append(file_list)

        if len(dirs) > 0:
            for d in dirs:
                find_png_files(d)

    return list_of_lists

if __name__ == '__main__':
    list_of_png_files = []
    current_dir = os.getcwd()
    list_of_png_files = find_png_files(current_dir)
