#!/usr/bin/env python3

"""
This is a script to create more sample data for the lesson 6 assignment
"""

# pylint: disable= C0301, C0103

import csv
import uuid
from datetime import datetime
from random import randint, choice


def add_data(path, quantity):
    """
    This script will add new rows to a csv based on the input quantity.
    :param path: Path to the CSV
    :param quantity: How many rows of data to be created
    :return:
    """
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        for x in range(quantity):
            day, month, year = randint(1, 28), randint(1, 12), randint(2013, 2018)
            d = str(year) + str(month) + str(day)
            date = datetime.strptime(d, '%Y%m%d').strftime('%m/%d/%Y')
            ao = ['ao', '']
            row = (['{}'.format(uuid.uuid4()), x + 1, x + 2, x + 3, x + 4, date, choice(ao)])
            writer.writerow(row)


if __name__ == '__main__':
    csv_path = "data/exercise.csv"
    add_data(csv_path, 1000000)
