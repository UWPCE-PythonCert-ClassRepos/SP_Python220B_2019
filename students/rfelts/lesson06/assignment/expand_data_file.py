#!/usr/bin/env python3

# Russell Felts
# Assignment 6

""" Expand data in csv file to one million records """

import csv
import uuid
import random
from datetime import datetime, timedelta


def random_date():
    """
    Generate a random datetime in format dd - mm - yyyy
    :return: A date string in the format of month, day, and four digit year
    """
    start = datetime(1969, 1, 1)
    max_year = datetime.now().year
    years = max_year - 1969
    end = start + timedelta(days=365 * years)
    temp_date = start + (end - start) * random.random()
    return temp_date.strftime("%m/%d/%Y")


def main():
    """
    Append 999,990 rows to a csv file.
    """
    with open('data/exercise.csv', 'a') as data_file:
        # Move to the next line before appending new row to the file
        data_file.write("\n")
        data_writer = csv.writer(data_file)
        for i in range(11, 1000000):
            data_writer.writerow([uuid.uuid4(), i, i+1, i+2, i+3,
                                  random_date(), random.choice(['ao', '', '', ''])])


if __name__ == '__main__':
    main()
