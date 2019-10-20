#! /usr/bin/env python3

"""
HP Norton keeps pictures of all their furniture in png files that are stored on
their file server. They have a very crude program that starts by discovering
all directories on the server and then looking in each of those for the png
files. They have discovered a problem, though:
png files are not found when they are stored in directories that are more than
one level deep from the root directory.
Your job is to write a png discovery program in Python, using
recursion, that works from a parent directory called images provided on the
command line.
The program will take the parent directory as input. As output,
it will return a list of lists structured like this:
[“full/path/to/files”, [“file1.png”, “file2.png”,…], “another/path”,[], etc]
shouldn't this ^ be a dictionary?
"""
import argparse
import datetime
import logging
import os

LOGGER = logging.getLogger()


def setup_logging(_log_level=None):
    """
        Accepts None (no -d sent in) and 1 - 3.
        All other values are invalid including 0
        None: No debug messages or log file.
        1: Only error messages.
        2: Error messages and warnings.
        3: Error messages, warnings and debug messages.
        *  No debug message to logfile
    """
    log_level = logging.INFO
    if _log_level is None:
        print('No debug logging')
        LOGGER.addHandler(logging.NullHandler())
    elif int(_log_level) == 1:
        print('Error message logging')
        log_level = logging.ERROR
    elif int(_log_level) == 2:
        print('Error and Warning messages logging')
        log_level = logging.WARNING
    elif int(_log_level) == 3:
        print('Error, Warning and Debug message logging')
        log_level = logging.DEBUG
    else:
        print("Invalid log_level. Expected values 1 - 3. "
              "This argument is optional.")
        exit(1)

    if _log_level:
        log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d " \
                     "%(levelname)s %(message)s"
        formatter = logging.Formatter(log_format)
        file_handler = logging.FileHandler(log_file, mode='w')

        # We don't want to log DEBUG messages to the log file
        if log_level == logging.DEBUG:
            file_handler.setLevel(logging.WARNING)
        else:
            file_handler.setLevel(log_level)

        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        LOGGER.setLevel(log_level)
        LOGGER.addHandler(console_handler)
        LOGGER.addHandler(file_handler)


def parse_cmd_arguments():
    """ this function parses the command line arguments """
    parser = argparse.ArgumentParser(description='Find some files.')
    parser.add_argument('-r',
                        '--root_directory',
                        help='The root directory to start searching',
                        required=True)
    parser.add_argument('-f',
                        '--file_type',
                        help='The file type to search for',
                        required=True)

    parser.add_argument('-d',
                        '--debug',
                        help='set the log output level (1-3)',
                        required=False)

    return parser.parse_args()


def gather_files(root_directory, file_type, gathered_files):
    """
    Search from the root directory for all png files
    """
    LOGGER.info("Searching root:  %s for %s file type",
                root_directory, file_type)

    # find all subfolders in the directory
    subfolders = [f.path for f in os.scandir(root_directory) if f.is_dir()]

    # get all the files matching the file_type
    files_full = os.listdir(root_directory)
    files_filtered = [i for i in files_full if i.endswith(file_type)]

    # add the files to the gathered files collection
    gathered_files.append([root_directory, files_filtered])

    # for each directory call the function recursively
    for directory in subfolders:
        gather_files(directory, file_type, gathered_files)

    return gathered_files


if __name__ == "__main__":
    ARGS = parse_cmd_arguments()
    setup_logging(ARGS.debug)
    files = gather_files(ARGS.root_directory, ARGS.file_type, [])
    LOGGER.debug(files)
