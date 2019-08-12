import os
import sys

png_root_dir = sys.argv[1]

print('png_root_dir = ' + png_root_dir)


print('png_root_dir (absolute) = ' + os.path.abspath(png_root_dir))

for dir_name, sub_dirs, files in os.walk(png_root_dir):
    sub_dirs = [n for n in sub_dirs]
    images = sub_dirs + files
    images.sort()
    for image in images:
        print(image)

