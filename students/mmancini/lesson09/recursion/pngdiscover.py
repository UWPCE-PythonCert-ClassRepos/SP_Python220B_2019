
'''lesson9 recursion'''

import os

DATA_LIST = []

def png_discovery(directory):
    '''
        des: recurse specified folder create a hierarchy of contained subfolders and files
        in: folder spec to traverse from
        out: list of list format([subfoldername1/[filename1.png,filename2.png],...],[subfoldername2/[filename1.png,filename2.png,...], etc]
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
        DATA_LIST.append(os.path.join(os.getcwd(), directory))
        DATA_LIST.append(sublist)


if __name__ == '__main__':
    png_discovery(os.getcwd())
    
