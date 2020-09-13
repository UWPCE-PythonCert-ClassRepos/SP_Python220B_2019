"""
Find all pngs in a directory
"""
import os


def find_png(dir_name, result=[]):
    """
    Does a recursive search of a directory and returns a list of pngs discovered

    :param dir_name: The path of the directory to search
    :param result: List to append results to
    """
    all_files = [os.path.join(dir_name, x) for x in os.listdir(dir_name)]
    files = filter(os.path.isfile, all_files)
    pngs = []
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.png':
            pngs.append(os.path.basename(file))
    if pngs:
        result.append(os.path.abspath(dir_name))
        result.append(pngs)

    dirs = filter(os.path.isdir, all_files)
    for directory in dirs:
        find_png(directory, result)
    return result


if __name__ == "__main__":
    png_list = find_png('./data')
    print(png_list)
