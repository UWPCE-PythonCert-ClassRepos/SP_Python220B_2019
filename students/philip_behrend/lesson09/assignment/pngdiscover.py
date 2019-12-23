""" This module discovers image directories with PNG files """

import argparse
import os

def parse_args():
    """ Gathers user cmd input """
    parser = argparse.ArgumentParser(description="Processes user input")
    parser.add_argument('-i', '--input', help="Input directory", required=True)
    return parser.parse_args()

def find_png(parent_dir, png_list):
    """ Find all PNG files within parent directory and return list of file names """

    for root, _, file_list in os.walk(parent_dir):

        #print(f"root: {root}")
        #print(f"subs: {sub}")
        #print(f"files: {file_list}")

        cur_pngs = []
        for item in file_list:
            if item.endswith('.png'):
                cur_pngs.append(item)
        
        if cur_pngs:
            png_list.append(root)
            png_list.append(cur_pngs)
    
    return png_list

if __name__ == '__main__':
    ARGS = parse_args()
    all_pngs = find_png(ARGS.input, png_list=[])
    print(all_pngs)
