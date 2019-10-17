"""find jpg files with recursion in given directories """
from pathlib import Path
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--file-type', help='File extension .{ext}',
                        default='.png', required=False)
    parser.add_argument('-p', '--path', help='Parent path of files.',
                        required=True)
    return parser.parse_args()


def list_files(current_path, ext='.png'):
    """
    List all files of a certain extension in a directory
    :param current_path:
    :param ext:
    :return:
    """
    current_path = Path(current_path)
    result = [str(current_path.absolute()), []]

    for path in current_path.iterdir():
        if path.is_dir():
            result.extend(list_files(path, ext))
        if path.suffix == ext:
            result[1].append(path.name)

    return result


if __name__ == '__main__':
    args = parse_args()
    file_type = args.file_type
    parent_path = args.path
    png_files = list_files(parent_path, file_type)
    print(png_files)
