"""
Find the png files and show them in a list recursively.
"""

import os

def search_png(path):
    """search for png files"""
    result = []
    for root, folders, files in os.walk(path):
        png_files = []
        for file in files:
            if file.lower().endswith('.png'):
                png_files.append(file)
        if png_files:
            result.append(root)
            result.append(png_files)
        for folder in folders:
            search_png(folder)
    return result


if __name__ == '__main__':
    PNG_FOLDER = input("File path >: ")
    # PNG_FOLDER = os.path.join(os.getcwd(), 'data', 'furniture', 'chair')
    PNG_FILES = search_png(PNG_FOLDER)
    print(PNG_FILES)
