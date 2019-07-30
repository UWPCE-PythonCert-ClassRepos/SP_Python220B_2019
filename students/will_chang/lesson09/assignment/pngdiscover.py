"""
Return a list of lists through a recursive search of files
with a given extension
"""

import os

def find_files(parent_dir, ext):
    """List files in each directory that match the provided extension"""
    for entry in os.listdir(parent_dir):
        entry_path = os.path.join(parent_dir, entry)
        if os.path.isfile(entry_path) and entry.endswith(ext):
            if parent_dir in ENTRY_DICT.keys():
                ENTRY_DICT[parent_dir].append(entry)
            else:
                ENTRY_DICT[parent_dir] = [entry]
        elif os.path.isdir(entry_path):
            find_files(entry_path, ext)
    return ENTRY_DICT


def dict_to_list(a_dict):
    """
    Convert dictionary to list
    """
    new_list = []
    for key, val in a_dict.items():
        new_list.append(key)
        new_list.append(val)
    return new_list

if __name__ == "__main__":
    ENTRY_DICT = {}
    PARENT_DIRECTORY = os.getcwd()+"\images"
    NEW_DICT = find_files(PARENT_DIRECTORY, '.png')
    print(dict_to_list(NEW_DICT))
