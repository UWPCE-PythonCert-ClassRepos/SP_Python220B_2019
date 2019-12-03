"""list png files and paths"""
import os

def find_png(path):
    """search for png files"""
    path_list = []
    for path, directory, file_name in os.walk(path):
        file_list = []
        for file in file_name:
            if file.lower().endswith('.png'):
                file_list.append(file)
            if file_list:
                path_list.append(path)
                path_list.append(file_list)
            for dirc in directory:
                find_png(dirc)
    return path_list

if __name__ == '__main__':
    print(find_png(input("Enter file path : ")))
