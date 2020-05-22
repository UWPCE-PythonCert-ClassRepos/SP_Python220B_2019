"""Module to search nest folders using recusion to fing png files"""
import os


def search():
    """function using closure to hide the mylist"""
    mylist = []

    def find_png(start_directory):
        """Recursive function """
        nonlocal mylist
        for root, dirs, files in os.walk(start_directory):
            list_of_files = []
            for one_file in files:
                if one_file.lower().endswith(".png"):
                    list_of_files.append(one_file)
            mylist.append([root, list_of_files])
            for one_dir in dirs:
                find_png(one_dir)
        return mylist
    return find_png


if __name__ == "__main__":
    directory = input("Enter the starting directory: ")
    myfind_png = search()
    results = myfind_png(directory)
    print(results)
