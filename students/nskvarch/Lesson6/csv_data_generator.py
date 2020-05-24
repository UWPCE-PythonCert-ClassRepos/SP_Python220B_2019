#!usr/bin/env python 3
"""
.csv data file expander for the lesson 6 exercise in profiling and performance
re-writes the contents of the .csv file to include one million lines of randomized data
"""
# Created by Niels Skvarch

import csv
import random
from datetime import datetime, timedelta
import uuid


def random_date():
    """Creates a random date during the years of 2010 and 2018"""
    start_date = datetime(2010, 1, 1)
    end_date = start_date + timedelta(days=365 * 9)
    rand_date = start_date + (end_date - start_date) * random.random()
    return rand_date.strftime("%m/%d/%Y")


def random_ao_tag():
    """Adds an "ao" tag to the csv line at random"""
    if random.randint(0, 1):
        return "ao"
    return ""


def main():
    """Write one million lines of data to the .csv file"""
    with open(r"data\exercise.csv", "w") as file:
        file_write = csv.writer(file, lineterminator='\n')
        for i in range(1, 1000001):
            col_1 = uuid.uuid4()
            col_2 = i
            col_3 = i + 1
            col_4 = i + 2
            col_5 = i + 3
            col_6 = random_date()
            col_7 = random_ao_tag()
            file_write.writerow([col_1, col_2, col_3, col_4, col_5, col_6, col_7])


# main program namespace
if __name__ == "__main__":
    main()
