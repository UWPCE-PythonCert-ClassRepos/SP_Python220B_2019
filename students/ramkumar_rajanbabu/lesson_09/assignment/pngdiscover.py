"""Module for png discovery program"""

import csv
from os import path


def png_discover(directory_name):
    """Discover all directories then look in each directories for png files
    
    Args:
        directory_name: parent directory file path
    Returns:
        None
    """
    