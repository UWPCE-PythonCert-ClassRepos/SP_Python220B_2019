""" Finds PNG Images from a directory"""
import os
import argparse
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def parse_cmd_arguments():
    """ Gets directory to find files """
    parser = argparse.ArgumentParser(description='Look for PNG Files')
    parser.add_argument('-d', '--directory', help='Directory to Find PNG Files', required=True)

    return parser.parse_args()


def find(path):
    """ Finds PNG Files in a Given Directory """
    png_files = []
    for root, dirs, files in os.walk(path):
        png_img = []
        for file in files:
            if file.endswith('.png'):
                png_img.append(file)
                LOGGER.info('PNG Image Found')
        if png_img:
            png_files.append(root)
            png_files.append(png_img)

        for directory in dirs:
            find(directory)

    return png_files


if __name__ == "__main__":
    LOGGER.info('Getting Directory')
    ARGS = parse_cmd_arguments()
    LOGGER.info('Looking For PNG Files...')
    print(find(ARGS.directory))
