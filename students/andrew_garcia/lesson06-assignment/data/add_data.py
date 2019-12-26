""" Adding New Data into CSV File"""

import uuid
import csv
import random
from datetime import date


def random_date():
    ''' Picks a random date '''
    start = date(2000, 1, 1)
    end = date(2019, 1, 1)
    new_date = start + ((end - start) * random.random())
    return new_date


with open('exercise.csv', 'w', newline='') as file:
    WRITER = csv.writer(file)
    for i in range(1000000):
        number = random.randint(1, 97)
        WRITER.writerow([str(uuid.uuid4()), number, number + 1, number + 2, number + 3,
                         random_date().strftime('%m/%d/%Y'), random.choice(['ao', ''])])
