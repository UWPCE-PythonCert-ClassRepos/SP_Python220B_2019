"""Module for png discovery program"""

import os


def search_png(path):
    """Discover all directories then look in each directories for png files"""
    result = []
    for root, folders, files in os.walk(path):
        png_files = []  # Collects png_files in a list
        for file in files:
            if file.lower().endswith(".png"):  # Only png files
                png_files.append(file)  # Adds png file to list
        if png_files:
            result.append(root)
            result.append(files)
        for folder in folders:
            search_png(folder)

    return result


if __name__ == "__main__":
    PNG_PATH = input("Enter file path:")
    PNG_FILES = search_png(PNG_PATH)
    print(PNG_FILES)
