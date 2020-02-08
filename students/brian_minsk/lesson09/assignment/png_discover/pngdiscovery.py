""" Code for lesson09 assignment, part 3, png discovery

Note: This could be accomplished for the most part by os.walk but since one of the subjects of this
lesson is recursion a implementation that shows recursion is assumed. :)
"""
# pylint: disable=unused-argument, dangerous-default-value
import os
import logging
from pprint import pformat

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def file_directory_tree(parent_directory=".", filter_ext="png"):
    """ Return a list of lists of a recursive directory search of the form (example for file
    extension "png"): [“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[], etc]

    Keyword arguments:
    parent_directory - the directory to start the search in
    filter_ext - limit the search to files with this extension only
    """
    directory_tree = full_directory_tree()
    return convert_to_output_form(directory_tree)


# pylint: disable=redefined-outer-name
def full_directory_tree(directories=[], tree={}, current_directory=".", filter_ext="png"):
    """ Return a full recursive directory tree dictionary of all files of the form
    {dir0.0: [file0.0.1, file0.0.2, ...], dir1.0: [file1.0.0, file1.0.1, ...],
     dir1.1: [file1.1.0, file1.1.1, ...], dir2.0: [file2.0.0, file2.0.1, ...], ...}
     using depth-first search.

    Keyword arguments:
    directories - a list of visited directories (pass in an empty list only to start)
    tree - will be appended to on each recursive call (pass in an empty dictionary only to start)
    current_directory - the directory currently being investigated (pass in the parent directory
        only to start)
    filter_ext - if a string only add files with an extention equal to filter_ext
    """
    directories += current_directory

    for item in os.scandir(path=current_directory):
        # assume everything is a proper file or directory (e.g. not a symbolic link)
        if item.is_file() and isinstance(filter_ext, str) and item.name.endswith(filter_ext):
            if current_directory in tree:
                tree[current_directory] += [item.path]
            else:
                tree[current_directory] = [item.path]
        elif item.is_dir():
            full_directory_tree(directories=directories, tree=tree, current_directory=item.path,
                                filter_ext=filter_ext)

    return tree


def convert_to_output_form(directory_tree, output=[]):
    """ Convert a directory tree to the form specified as the return value for lesson09 part 3 e.g.
    [“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[], etc]

    Note: Just for fun, make this one recursive too.

    Keyword arguments:
    directory_tree - a directory tree of the form:
        {dir0.0: [file0.0.1, file0.0.2, ...], dir1.0: [file1.0.0, file1.0.1, ...],
        dir1.1: [file1.1.0, file1.1.1, ...], dir2.0: [file2.0.0, file2.0.1, ...], ...}
    output - initial call output must be an empty list
    """
    while directory_tree:
        first_directory = next(iter(directory_tree))
        output.extend([first_directory, directory_tree.pop(first_directory)])
        convert_to_output_form(directory_tree, output)

    return output


if __name__ == '__main__':
    TREE = file_directory_tree()
    LOGGER.info(pformat(TREE))
