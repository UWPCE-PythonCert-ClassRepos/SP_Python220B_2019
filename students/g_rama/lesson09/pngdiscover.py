"""Recursion exercise to go to the bottom of th folders"""
import os
import sys

#png_root_dir = sys.argv[1]

# print('png_root_dir = ' + png_root_dir)
#
#
# print('png_root_dir (absolute) = ' + os.path.abspath(png_root_dir))

# for dir_name, sub_dirs, files in os.walk(PNG_ROOT_DIR):
#     sub_dirs = [n for n in sub_dirs]
#     images = sub_dirs + files
#     images.sort()
#     for image in images:
#         print(image)


def image_recursion(root_dir):
    dirs = os.listdir(root_dir)
    print(dirs)
    images = []
    for file in dirs:
        images.append(file)
        if os.path.isdir(os.path.join(file)) is True:
            image_recursion(file)
            print(images)


if __name__ == '__main__':
    png_root_dir = sys.argv[1]
    image_recursion(png_root_dir)
