"""
pngdiscover.py

Find all PNG files in a directory tree starting with a root directory.

Usage::

    >>> python pngdiscover.py root

where ``root`` is the root directory to search in.
"""


import os
import sys


def find_png(directory: str):
    """Find .png files located in the directory.

    Returns
    -------
    list of lists
        List of lists of the format::
            [path_to_directory, [png1, png2, ... ], another_path, [png1, png2, ...]]
    """

    directory = os.path.realpath(directory)
    output = [directory, []]

    for entry in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, entry)):  # Is a directory
            output.extend(find_png(os.path.join(directory, entry)))
        elif entry.endswith(".png"):
            output[1].append(entry)

    if not output[1]:
        output.pop(0)
        output.pop(0)

    return output


if __name__ == "__main__":
    print(find_png(sys.argv[1]))
