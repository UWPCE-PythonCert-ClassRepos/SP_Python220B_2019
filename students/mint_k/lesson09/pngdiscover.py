"""to find all png files using recursive function"""
#pylint: disable=W0102

import os


def find_files(files, dirs=['./'], extensions=['.png']):
    """recursive function that will call itself to dig deeper into directory"""
    new_dirs = []
    for my_dir in dirs:
        try:
            new_dirs += [os.path.join(my_dir, f) for f in os.listdir(my_dir)]
        except OSError:
            if os.path.splitext(my_dir)[1] in extensions:
                files.append(my_dir)
    if new_dirs:
        find_files(files, new_dirs, extensions)
    else:
        return


if __name__ == "__main__":
    MY_PATH = "./"
    MY_EXT = '.png'
    MY_FILES = []
    find_files(MY_FILES, [MY_PATH], [MY_EXT])
    for f in MY_FILES:
        print(f)
        