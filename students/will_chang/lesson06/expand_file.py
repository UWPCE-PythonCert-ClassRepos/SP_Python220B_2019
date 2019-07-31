"""
Expands exercise.csv file to one million lines
"""

import csv
import uuid
import random
from datetime import datetime, timedelta

def random_date():
    """
    Generate a random date in the years 2010-2018
    """
    start = datetime(2010, 1, 1)
    end = start + timedelta(days=365 * 9)
    rand_date = start + (end - start) * random.random()
    return rand_date.strftime("%m/%d/%Y")


def determine_ao():
    """
    Randomly generate 'ao' or ''
    """
    if random.randint(0, 1):
        return 'ao'
    return ''

def csv_write():
    """
    Generate a csv file with 1000000 rows
    """
    with open('exercise.csv', 'w') as file:
        csv_writer = csv.writer(file, lineterminator='\n')
        for i in range(1, 1000001):
            col_1 = uuid.uuid4()
            col_2 = i
            col_3 = i + 1
            col_4 = i + 2
            col_5 = i + 3
            col_6 = random_date()
            col_7 = determine_ao()
            csv_writer.writerow([col_1, col_2, col_3, col_4, col_5,
                                 col_6, col_7])


if __name__ == '__main__':
    csv_write()
