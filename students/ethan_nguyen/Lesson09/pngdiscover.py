'''
Given a directory, recurssively fund png files
'''
import argparse
import os


def find_png(file_dir):
    """
    function to find png file given a directory
    """
    result = []
    for dir_name, sub_dir_list, file_list in os.walk(file_dir):
        print('Found directory: %s' % dir_name)
        found_file_list = []
        for file in file_list:
            if file.endswith(".png"):
                print('\t%s' % file)
                found_file_list.append(file)
        if file_list:
            result.append(dir_name)
            result.append(found_file_list)

        for sub_dir in sub_dir_list:
            find_png(sub_dir)

    return result


def parse_cmd_arguments():
    """
    function to parse input and check for input requirements
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', '--dir', help='input parent file path',
                        required=True)

    return parser.parse_args()


if __name__ == "__main__":

    CURRENT_PATH = os.getcwd()

    # for dirName, subdirList, fileList in os.walk(ARGS.dir):
    #     print('Found directory: %s' % dirName)
    #     for fname in fileList:
    #         print('\t%s' % fname)

    print(find_png(CURRENT_PATH))
