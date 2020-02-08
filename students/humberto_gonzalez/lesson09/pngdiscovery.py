# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 08:35:36 2020

@author: uz367d
"""

import argparse
import datetime
import logging
import os

# pylint: disable = logging-format-interpolation, unused-variable, invalid-name

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + '.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

def parse_cmd_arguments():
    '''Parses the user inputs'''
    parser = argparse.ArgumentParser(description='Path to root directory')
    parser.add_argument('-p', '--path', help='path to root', required=True)
    return parser.parse_args()


def explore_folders(filepath, contents):
    """Given a root, find all PNG files within"""
    if not os.path.exists(filepath):
        logging.debug("FileNotFound")
        logging.error(f"{filepath} does not exist, please enter a valid file path")
        raise ValueError
    contents.append(filepath)
    file_list = []
    for item in os.listdir(filepath):
        if item.lower().endswith(".png"):
            file_list.append(item)
    contents.append(file_list)
    for item in os.listdir(filepath):
        if os.path.isdir(os.path.join(filepath, item)):
            contents = explore_folders(os.path.join(filepath, item), contents)
    return contents

if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    explored = explore_folders(ARGS, [])
    print(explored)
