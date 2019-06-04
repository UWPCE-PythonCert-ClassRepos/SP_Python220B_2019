"""list jpg files and their paths"""
import os


def find_jpg(path):
    """search for jpg files"""
    path_list = []
    for root, direcs, files in os.walk(path):
        file_list = []
        for file in files:
            if '.png' in file:
                file_list.append(file)
        if file_list:
            path_list.append(root)
            path_list.append(file_list)
        for direc in direcs:
            find_jpg(direc)
    return path_list


if __name__ == '__main__':
    JPG_LIST = find_jpg(os.getcwd())
    print(JPG_LIST)
    print(len(JPG_LIST))
