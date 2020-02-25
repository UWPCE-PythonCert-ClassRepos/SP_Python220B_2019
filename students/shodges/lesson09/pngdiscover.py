'''
Module to allow for recrusive discovery of PNG images.
'''

from pathlib import Path

def png_discover(directory):
    '''
    List PNG's in directory, and recurse for child directories.

    Ultimately a list will be returned with this structure:
    ['/absolute/path', '/absolute/path/subdir', ['image1.png', 'image2.png'],
     '/absolute/path/subdir2', ['imageA.png'], 'imageZ.png']
    '''
    png_files = []
    for file in Path(directory).iterdir():
        if file.is_dir():
            dir_path = file.absolute().as_posix()
            png_files.append(dir_path)
            png_files.append(png_discover(file.absolute().as_posix()))
        elif file.name.endswith('.png'):
            png_files.append(file.name)
    return png_files

if __name__ == '__main__':
    print(png_discover('/Users/shodges/Repos/SP_Python220B_2019/students/shodges'))
