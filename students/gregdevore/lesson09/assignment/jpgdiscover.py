'''
Module for discovering all picture files (png default) within a root directory.
Recursively searches all subdirectories.
'''
import os
import argparse

def parse_cmd_arguments():
    '''
    Define command line argument structure
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='target directory', required=True)
    return parser.parse_args()

def find_pictures(current_path, filetype='png'):
    '''
    Starting at provided directory, recursively search all subdirectories
    for image files. Populates a list of lists with each directory and all
    images found within.

    Args:
        current_path (str):
            Current path to search for pictures
        filetype (str):
            Type of image to search for (default is png)
    '''
    # Get contents of current directory
    contents = os.listdir(current_path)
    # List of pictures to populate
    pictures = []
    for item in contents:
        # Get full path to item
        full_path_to_item = os.path.abspath(os.path.join(current_path, item))
        # If current item is a picture file with the appropriate extension, add
        # to list of pictures
        if os.path.isfile(full_path_to_item) and full_path_to_item.endswith('.' + filetype):
            pictures.append(item)
        # If current item is a directory, recursively call function
        elif os.path.isdir(full_path_to_item):
            find_pictures(full_path_to_item)
    # Add current directory and any pictures found to output
    output.append(os.path.abspath(current_path))
    output.append(pictures)

if __name__ == '__main__':
    # Parse command line arguments
    args = parse_cmd_arguments()
    output = []
    # Call find_pictures, which will populate 'output'
    find_pictures(args.directory)
    # Print results
    print(output)
