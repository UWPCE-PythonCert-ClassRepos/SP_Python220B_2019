# Stella Kim
# Assignment 6: Finding Bottlenecks

"""
Create CSV file with one million data records following
format for given initial 10 records (exercise file).
"""

import random
import datetime
import csv
import uuid
from timeit import timeit as timer


def create_random_date():
    """Generate random date between 2010 and today using specific format"""
    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date.today()
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime('%m/%d/%Y')


def generate_data(default=1000000):
    """Generate rows of data following exercise file formatting"""
    with open('./data/data.csv', 'w', newline='') as file:
        data_file = csv.writer(file, quoting=csv.QUOTE_NONE)
        choices = ['ao', '']
        for i in range(default):
            row = uuid.uuid4(), i + 1, i + 2, i + 3, i + 4,\
                  create_random_date(), random.choice(choices)
            data_file.writerow(row)


def _code_timer():
    """Measure time it takes to run code"""
    print(timer('generate_data()', globals=globals(), number=1))


if __name__ == "__main__":
    generate_data(10)
    # _code_timer()
