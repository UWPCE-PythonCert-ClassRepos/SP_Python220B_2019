"""Extend exercise.csv file to one million lines."""

import csv
import uuid
import random
from datetime import datetime, timedelta

def generate_date():
    """Generate a random date in the years 2013-2017."""

    start = datetime(2013, 1, 1)
    end = start + timedelta(days=365 * 5 + 1)
    rand_date = start + (end - start) * random.random()

    return rand_date.strftime("%m/%d/%Y")


def add_ao():
    """Determines when to add 'ao'"""

    if random.randint(0, 2) == 2:
        return 'ao'
    return ''


def extend_csv():
    """Generate a csv file with 1000000 rows"""

    with open('exercise.csv', 'w') as file:
        csv_writer = csv.writer(file, lineterminator='\n')
        for i in range(1, 1000001):
            csv_writer.writerow([uuid.uuid4(), i, i + 1, i + 2, i + 3,
                                 generate_date(), add_ao()])


if __name__ == '__main__':
    extend_csv()
