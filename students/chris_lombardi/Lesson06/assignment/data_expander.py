"""A script to generate a *.csv file with random entries to support
   expansion of data for Lesson06"""

import uuid
import csv
import os
import datetime
import random

PATH = ('C:\\users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\students'
        '\\chris_lombardi\\Lesson06\\assignment\\data')
YEARS = [year for year in range(2005, 2019)]
LAST_COL = ['ao', '']

def gen_rand_date(year):
    """Generates a random date"""
    try:
        month = random.randint(1,13)
        day = random.randint(1,31)
        rand_date = datetime.date(year, month, day)
        return rand_date.strftime('%m/%d/%Y')
    except ValueError:
        return gen_rand_date(year)

def find_last_row(filename, directory=PATH):
    """Return the last row number in a file"""
    # Check to see if file exists
    file_path = os.path.join(directory, filename)
    count = 0
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            # Iterate through rows in file and return final count of rows.
            while True:
                try:
                    next(reader)
                    count += 1
                except StopIteration:
                    return count
    # Return '0' indicating no rows in a file that doesn't exist.
    except FileNotFoundError:
        return 0

def expand_data(filename, start_num, end_num, directory=PATH):
    """Expands the data in the *.csv file to match the existing format."""
    file_path = os.path.join(directory, filename)
    # Determine whether or not to append or write to the file based on if it exists.
    if os.path.exists(file_path):
        editor = 'a'
    else:
        editor = 'w'
    # The starting row number for data.
    row_num = start_num
    with open(file_path, mode=editor, newline='', encoding='utf-8-sig') as file:
        data_writer = csv.writer(file)
        while row_num <= end_num:
            row = [uuid.uuid4(), row_num, row_num+1, row_num+2, row_num+3,
                   gen_rand_date(random.choice(YEARS)), random.choice(LAST_COL)]
            data_writer.writerow(row)
            row_num += 1

if __name__ == '__main__':
    DATAFILE = 'exercise.csv'
    NUM_ENTRIES = find_last_row(DATAFILE)
    expand_data(filename=DATAFILE, start_num=NUM_ENTRIES+1, end_num=1000000, directory=PATH)
