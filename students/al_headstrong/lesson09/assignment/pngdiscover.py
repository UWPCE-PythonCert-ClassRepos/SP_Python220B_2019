""" Module to recursively search for png files."""
import os


def png_search(directory):
    """Return list of paths and pictures found."""
    pics, paths = [], []
    for content in os.listdir(directory):
        if content.endswith('png'):
            pics.append(content)
        try:
            paths.extend(png_search(os.path.join(directory, content)))
        except NotADirectoryError:
            continue
    if pics:
        paths.append(directory)
        paths.append(pics)
    return paths


if __name__ == "__main__":
    DIRECTORY = os.getcwd() + "\\images"
    for contents in png_search(DIRECTORY):
        print(contents)
