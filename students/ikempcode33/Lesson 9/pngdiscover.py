
import os

def locate_png(search_folder):
    """find files within folders"""
    loc_list = []
    for root, dir_names, file_names in os.walk(search_folder):
        pic_list = []
        for file in file_names:
            if file.endswith('.png'):
                pic_list.append(file)
        if pic_list:
            loc_list.append(root)
            loc_list.append(pic_list)
        for subdir in dir_names:
            locate_png(subdir)
    
    return loc_list

if __name__ == '__main__':
    #folder = os.getcwd()
    folder = 'pictures'
    png_files = locate_png(folder)
    print(png_files)
