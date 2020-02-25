'''
Module to allow for recrusive discovery of PNG images.
'''

from pathlib import Path

def png_discover(directory):
    '''
    List PNG's in directory, and recurse for child directories.
    '''
    print(directory)
    for file in Path(directory).iterdir():
        if file.is_dir():
            png_discover(file.absolute().as_posix())
        else:
            print(file.name)

if __name__ == '__main__':
    png_discover('../../')
