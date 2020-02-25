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
    png_this_dir = []
    png_files = []
    for file in Path(directory).iterdir():
        if file.is_dir():
            child_files = png_discover(file.absolute().as_posix())
            if len(child_files) > 0:
                #If anything was found in child directories, add its dirname followed by the list
                #of files
                png_files.append(child_files[0])
                png_files.append(child_files[1])
        elif file.name.endswith('.png'):
            png_this_dir.append(file.name)
    if len(png_this_dir) > 0:
        #If we found anything in this dir (excluding subdir's), append it and the dir name to
        #png_files
        png_files.insert(0, directory)
        png_files.insert(1, png_this_dir)
    return png_files

if __name__ == '__main__':
    print(png_discover('/Users/shodges/Repos/SP_Python220B_2019/students/shodges'))
