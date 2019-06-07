"""This program uses recursion in order to find jpg files within a folder."""
import os
import logging
# pylint: disable=W1203,C0103

logging.basicConfig(format="%(asctime)s %(filename)s:%(lineno)-3d"
                    "%(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def recursion(directory, jpg_name=None):
    """A recursive function to find jpg files within folders"""
    out = [directory, []]

    if jpg_name is None:
        jpg_name = []

    for file in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, file)):
            logger.info(f'Going deeper - {os.path.join(directory, file)}')
            recursion(os.path.join(directory, file), jpg_name)

        elif file.endswith('.jpg'):
            logger.info(f'{file} found')
            out[1].append(file)
            logger.info(f'Appended {file} file to output list')

    if out[1]:
        jpg_name.extend(out)

    return jpg_name

if __name__ == "__main__":
    print(recursion(os.getcwd()))
