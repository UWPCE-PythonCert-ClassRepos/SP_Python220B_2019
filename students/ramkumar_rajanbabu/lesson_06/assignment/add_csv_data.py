"""Module for add data to given csv file"""

import csv
import random
from uuid import uuid4
from datetime import date


def rand_date():
    """Generate random date from 1/01/2010 to today"""
    start_date = date(2010, 1, 1)  # Year, month, day
    end_date = date.today()  # Today's date
    random_date = start_date + ((end_date - start_date) * random.random())
    return random_date.strftime('%m/%d/%Y')  # Format MM/DD/YYYY


with open('data/exercise.csv', mode="w", newline='') as file_name:
    WRITER = csv.writer(file_name)
    NUM = 1
    for NUM in range(1000000):  # Million records max range
        uu_id = str(uuid4())
        ao = random.choice(['ao', None])
        row_entry = [uu_id, NUM+1, NUM+2, NUM+3, NUM+4, rand_date(), ao]
        WRITER.writerow(row_entry)
