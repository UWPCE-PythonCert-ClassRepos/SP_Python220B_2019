#! /usr/bin/env python3
""" Generate data for our profiling """
import csv
import datetime
import random
import uuid
import numpy as np


def get_rand_row():
    """ Generate a random row for the file """
    unique_id = uuid.uuid1()
    numbers = np.random.randint(1, 1001, 4)
    startdate = datetime.date(2012, 1, 1)
    daterand = startdate + datetime.timedelta(np.random.randint(1, 366 * 10))
    ao_value = 'ao' if random.choice([True, False]) else None

    return [unique_id,
            numbers[0],
            numbers[1],
            numbers[2],
            numbers[3],
            daterand.strftime("%m/%d/%Y"),
            ao_value]


def write_file(filename, rowcount=100):
    """ Write the rows to the file """
    with open(filename, mode='w') as csv_file:
        for rowid in range(rowcount):
            print('Creating row {}'.format(rowid))
            writer = csv.writer(csv_file,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(get_rand_row())


if __name__ == "__main__":
    print(write_file('data/exercise.csv', 1_000_000))
