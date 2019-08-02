"""
Victor Medina
Assignment 9: Recursive PNG read
"""

"""list png files and their paths"""
import glob
import os
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def find_png(path):
    """search for png files"""

    files = [f for f in glob.glob(path + "**/*.png", recursive=True)]
    LOGGER.info(files)
    for file in files:
        print(file)
    return files


if __name__ == '__main__':
    find_png(os.getcwd())
