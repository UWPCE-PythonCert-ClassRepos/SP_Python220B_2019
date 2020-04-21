'''Creates data for csv file'''

import csv
import random
from datetime import date
from uuid import uuid4

def random_date():
    '''Creates a random date'''
    start_date = date(2000, 1, 1)
    end_date = date(2019, 1, 1)
    return start_date + (end_date - start_date) * random.random()

with open('exercise.csv', 'w', newline='') as csv_file:
    CSV_WRITTER = csv.writer(csv_file)
    for i in range(1000000):
        CSV_WRITTER.writerow([str(uuid4()), i, i + 1, i + 2, i + 3,
                              random_date().strftime('%m/%d/%Y'),
                              random.choice(['ao', '', ''])])
