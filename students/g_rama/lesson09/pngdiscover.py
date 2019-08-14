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
    print("rmakanth")
    print(dirs)
    #return dirs
    images = []
    for file in dirs:
        print(file)
        images.append(file)
        if os.path.isdir(os.path.join(root_dir, file)):
            path_in = os.path.join(root_dir, file)
            print(path_in)
            dirs_in  = os.listdir(path_in)
            images.append(dirs_in)
            images_in = []
            for file_in in dirs_in:
                images_in.append(file)
                #images.append(images_in)
                if os.path.isdir(os.path.join(path_in, file_in)):
                    print(os.path.join(path_in, file_in))
                    inside_image = image_recursion(os.path.join(path_in, file_in))
                    print(inside_image)
                    images_in.append(inside_image)

    return images




           # image_recursion(os.path.join(root_dir, file))


        # images.append(file)
        # if os.path.isdir(file):
        #     path = os.path.join(file, "")
        #     print(path)
        #     image_recursion(path)
        #     print(images)


if __name__ == '__main__':
    png_root_dir = sys.argv[1]
    direc = image_recursion(png_root_dir)
    print(direc)
