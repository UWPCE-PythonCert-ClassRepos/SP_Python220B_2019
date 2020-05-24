# pngdiscover.py
""" This module defines functions that discover all the .png files
    under the sepcific parent directory.
"""
import os
import logging


output_list = []

# set logging configuration
LOG_FORMAT = "%(levelname)s %(filename)s %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def discover_file(directory):
    for cur_path, cur_dir, files in os.walk(directory):
        LOGGER.debug(f'cur_subdir:{cur_dir}, cur_files:{files}')
        for file in files:
            if file.endswith('.png'):
                if cur_path not in output_list:
                    output_list.append(cur_path)
                    files_list = []
                    output_list.append(files_list)
                files_list.append(file)
                LOGGER.debug(f'adding file:{file} to dir:{cur_path}')

        if cur_dir:
            for the_dir in cur_dir:
                # recursively calling discover_file() to find .png files under
                # sub-directory.
                LOGGER.debug('\n----------------')
                LOGGER.debug(f'-- Start to dig in dir:{the_dir} -- ')
                new_dir = os.path.join(cur_path, the_dir)
                discover_file(new_dir)
                LOGGER.debug(f'-- End of dig in dir:{the_dir} --')
        # if the current directory doesn't have any sub-directory
        # then terminate the recursion.
        else:
            LOGGER.debug(f'Return from dir:{directory} due to no sub-dir')
        break
