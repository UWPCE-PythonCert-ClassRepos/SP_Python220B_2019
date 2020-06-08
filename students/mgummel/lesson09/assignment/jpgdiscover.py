from pathlib import Path
from os import listdir

file_list = list()

def get_dir(default_path="./data"):
    directory_path = input("Enter parent directory to search from\n>>>")
    if directory_path:
        return directory_path
    return default_path

def get_pictures(working_directory):
    test = listdir(working_directory)
    print(test)

    """d = '.'
    e = [os.path.join(d, o) for o in os.listdir(d)
     if os.path.isdir(os.path.join(d, o))]"""



if __name__ == '__main__':
    path = get_dir()
    #list_recursively([2,23,33,2,23,40])
    get_pictures(path)