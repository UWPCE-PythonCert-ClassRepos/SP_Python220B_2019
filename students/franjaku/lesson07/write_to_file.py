"""
    Populate the data file to contain a million entries.

"""

import logging
import csv
import uuid
import datetime
import random

# Setup logging
FILE_LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"

# Console logging setup
CONSOLE_LOG_FORMAT = "%(filename)s:%(lineno)-4d %(message)s"
CONSOLE_FORMATTER = logging.Formatter(CONSOLE_LOG_FORMAT)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(CONSOLE_FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)

# Open file
file_path = 'C:/Users/USer/Documents/UW_Python_Certificate/Course_2/SP_Python220B_2019/students/' \
            'franjaku/lesson07'

file = 'rental_data.csv'


def add_entries(file_path, file):
    """Add rentals to file."""
    with open(file_path + '/' + file, 'r+', newline='') as fl:
        reader = csv.reader(fl)
        rand_writer = csv.writer(fl, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            last = row

        rental_num = int(last[1])
        rental_num += 1
        for x in range(10000-1-rental_num):
            rental_num += 1
            row = [rental_num, random.randint(1, 10), random.randint(1, 10)]
            rand_writer.writerow(row)


if __name__ == "__main__":
    add_entries(file_path, file)
