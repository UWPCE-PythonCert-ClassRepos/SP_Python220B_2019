"""
This is a one-off program to create the product_data, customer_data, and rentals_data csv files
in a folder named 'csvs'. This program is otherwise useless once the data is created. I only made
this because I couldn't find any pre-generated csv files or formats were given.
"""

import os
import csv
import logging
import random
from datetime import date, timedelta

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'test.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

def write_csv():
    """This method writes the million entry csv files to import for testing"""

    LOGGER.debug("Writing to .csv files")
    with open('data/exercise.csv', 'w') as data:
        for record in range(0,100):
            something1 = record + 1
            something2 = record + 2
            something3 = record + 3
            something4 = record + 4
            date = random_date()
            perf_data = [something1, something2, something3, something4, date, date, something1]
            writer = csv.writer(data, lineterminator='\n')
            writer.writerow(perf_data)
    LOGGER.debug("Write successful!")

def random_date():
    min_year = 2010
    max_year = 2018
    years = 9
    start = date(2010, 1, 1)
    end = timedelta(years*365)
    return start + end * random.random()
    

if __name__ == '__main__':
    write_csv()
