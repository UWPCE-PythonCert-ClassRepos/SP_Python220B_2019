"""
find all the png files, recursively in a directory.
return each directory and list as key value pairs in dictionary
"""

import os
from pprint import pprint


def find_files(path, extension="png"):
    """
    find all the matching files, recursively in a directory.
    return each directory and list as key value pairs in dictionary
    :type path: str
    :type extension: str
    :return: dict
    """
    files = {path: []}
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            files.update(find_files(os.path.join(path, file)))
        elif file.endswith(f".{extension}"):
            files[path].append(file)

    return files


if __name__ == "__main__":
    PATH = "C:\\" \
            "Users\\" \
            "pants\\" \
            "PycharmProjects\\" \
            "SP_Python220B_2019\\" \
            "students\\" \
            "tim_lurvey\\" \
            "lesson09\\" \
            "assignment\\" \
            "data"
    found = find_files(path=PATH, extension="png")
    pprint(found)
