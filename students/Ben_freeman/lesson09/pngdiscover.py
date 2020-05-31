import os


def dive(directory, big_list):
    contents = os.listdir(directory)
    picture_holder = []
    png_bool = 0
    for items in contents:
        try:
            dive(items, big_list)
        except:
            if ".png" in items:
                picture_holder.append(items)
                png_bool = 1
    if png_bool == 1:
        big_list.append(os.path.abspath(directory))
    big_list.append(picture_holder)


if __name__ == '__main__':
    big_list = []
    dive("../lesson09", big_list)
    print(big_list)
