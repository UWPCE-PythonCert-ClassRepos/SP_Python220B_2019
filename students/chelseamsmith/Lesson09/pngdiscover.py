"""list png files and paths"""
import os

def find_png(path):
    """search for png files"""
    output = []
    for dirpath, direc, file_names in os.walk(path):
        files = []
        for file in file_names:
            if file.lower().endswith('.png'):
                files.append(file)
            if files:
                output.append(dirpath)
                output.append(files)
            for directory in direc:
                find_png(directory)
    return output

if __name__ == '__main__':
    PNGS = find_png(input("Enter file path to be searched: "))
    print(PNGS)
