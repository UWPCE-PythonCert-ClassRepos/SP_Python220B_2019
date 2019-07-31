'''Chapter 9, Recursion'''
import os

MY_LIST = []

def png_discovery(directory):
    '''
        takes in a directory path and appends .png files to MY_LIST
        as a list of lists like this:
        [“full/path/to/files”, [“file1.png”, “file2.png”,…],
         “another/path”,[], etc]
    '''
    sublist = []
    count = 0
    for file in os.listdir(directory):
        if file.endswith('.png'):
            count += 1
            sublist.append(file)
        elif os.path.isdir(os.path.join(directory, file)):
            png_discovery(os.path.join(directory, file))
        else:
            continue
    if count >= 1:
        MY_LIST.append(os.path.join(os.getcwd(), directory))
        MY_LIST.append(sublist)


if __name__ == '__main__':
    png_discovery(os.getcwd())
    # for x in MY_LIST:
    #     print(x)
