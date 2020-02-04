"""Module for png discovery program"""

import csv
import os


def discover_png(path):
    """Discover all directories then look in each directories for png files
    
    Args:
        directory_name: parent directory file path
    Returns:
        None
    """
    result = []
    for root, folders, files in os.walk(path):
        png_files = [] #Collects png_files in a list
        for file in files:
            if file.lower().endswith(".png"):  # Only png files
                png_files.append(file) #Adds png file to list
        if png_files:
            result.append(root)
            result.append(files)
        
        # Figure out by run cmd
        for folder in folders:
            discover_png(folder)  # Recursion
            
        return result
    
if __name__ == "__main__":
    pass
