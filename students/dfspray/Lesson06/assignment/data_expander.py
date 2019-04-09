"""
This is a one-off program to create one million records to test the efficiency of poor_perf.py
"""

import csv
import logging
import random
import uuid
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
        for record in range(0, 1000000):
            unique_id = uuid.uuid4()
            something1 = record + 1
            something2 = record + 2
            something3 = record + 3
            something4 = record + 4
            random_ao = random.choice(['ao', None])
            rand_date = random_date()
            perf_data = [unique_id, something1, something2, something3,
                         something4, rand_date, random_ao]
            writer = csv.writer(data, lineterminator='\n')
            writer.writerow(perf_data)
    LOGGER.debug("Write successful!")

def random_date():
    """This method creates a random date between 2010 and 2018"""
    start = date(2010, 1, 1)
    years = 9
    end = timedelta(years*365)
    rand_date = start + end * random.random()
    return rand_date.strftime("%m/%d/%Y")


if __name__ == '__main__':
    write_csv()
