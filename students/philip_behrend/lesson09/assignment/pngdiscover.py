""" This module discovers image directories with PNG files """

import argparse
import os

def parse_args():
    """ Gathers user cmd input """
    parser = argparse.ArgumentParser(description="Processes user input")
    parser.add_argument('-i', '--input', help="Input directory", required=True)
    return parser.parse_args()

def find_png(parent_dir, output_list):
    """ Find all PNG files within parent directory and return list of file names """
    os.chdir(parent_dir)
    png_list = []
    for item in os.listdir(parent_dir):
        print(f"ITEM: {item}")
        print(os.listdir(parent_dir))
        if item.endswith('.png'):
            print(f'PNG:{item}')
            png_list.append(item)
        elif os.path.isdir(os.path.abspath(item)):
            subdir = os.path.abspath(item)
            print(f"DIR: {subdir}")
            find_png(subdir, output_list)

        if png_list:
            output_list.append(os.getcwd())
            output_list.append(png_list)
        
    print(f"OUTPUT: {output_list}")
    return output_list
        



""" ### This function uses os.walk, which is the automated way to use recursion
def find_png(parent_dir, png_list):
     Find all PNG files within parent directory and return list of file names 

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
"""

if __name__ == '__main__':
    ARGS = parse_args()
    all_pngs = find_png(ARGS.input, [])
    print(all_pngs)
