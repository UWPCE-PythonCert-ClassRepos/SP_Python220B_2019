"""Recursively search a directory for PNG files."""
import os


def find_png(path):
    """Recursively search a directory for PNG files."""
    contents = os.listdir(path)
    master_list = list()
    found = list()
    for item in contents:
        if item.endswith('.png'):
            found.append(item)
        elif os.path.isdir(os.path.join(path, item)):
            master_list.extend(find_png(path + '/' + item))
    master_list.append(path)
    master_list.append(found)
    return master_list


if __name__ == "__main__":
    RESULTS = find_png(os.getcwd() + '/png_data')
    for entry in RESULTS:
        print(entry)
