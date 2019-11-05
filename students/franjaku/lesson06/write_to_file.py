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
            'franjaku/lesson06/data'

file = 'exercise.csv'

def add_entries(file_path, file):
    with open(file_path + '/' + file, 'r+', newline='') as fl:
        reader = csv.reader(fl)
        rand_writer = csv.writer(fl, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            last = row

        num_rows = int(last[1])
        opt = ['ao', '']

        for x in range(1000000-1-num_rows):
            # row = [uuid, row_num, row_num+1, row_num+2, row_num+3, rand date, ao]
            rand_date = random.randint(731000, 740000)
            rnd = random.randint(0, 1)
            row = [uuid.uuid4(), x+num_rows, x+num_rows+1, x+num_rows+2, x+num_rows+3,
                   datetime.date.fromordinal(rand_date).strftime('%x'), opt[rnd]]
            rand_writer.writerow(row)


if __name__ == "__main__":
    add_entries(file_path, file)
