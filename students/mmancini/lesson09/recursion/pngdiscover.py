
'''lesson9 recursion'''

import os

DATA_LIST = []

def png_discovery(directory):
    '''
        des: recurse specified folder create a hierarchy of contained subfolders and files
        in: folder spec to traverse from
        out: list of list format([subfoldername1/[filename1.png,filename2.png],...],[subfoldername2/[filename1.png,filename2.png,...], etc]
    '''
    pass


if __name__ == '__main__':
    png_discovery(os.getcwd())
    
