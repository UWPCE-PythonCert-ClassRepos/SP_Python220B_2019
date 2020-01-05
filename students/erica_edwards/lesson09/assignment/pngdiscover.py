"""Find .png files and print file path"""
import os
import argparse

#pylint: disable=redefined-outer-name
#pylint: disable=invalid-name
#pylint: disable=expression-not-assigned

def parse_cmd_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Find .png files.')
    parser.add_argument('-i', '--input', help='specify parent directory',
                        default="./data", required=True)
    return parser.parse_args()

def find_files(path, png_list):
    """Recursive method to find .png files"""
    files = [f.name for f in os.scandir(path) if f.is_file() and f.name.endswith(".png")]
    if files:
        png_list.append(path)
        png_list.append(files)
    folders = [f.path for f in os.scandir(path) if f.is_dir()]
    [find_files(folder, png_list) for folder in folders]


if __name__ == "__main__":
    args = parse_cmd_arguments()
    png_list = []
    find_files(args.input, png_list)
    print()
    print(png_list)
