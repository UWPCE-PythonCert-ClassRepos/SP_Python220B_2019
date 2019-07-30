
import uuid
import csv
import logging
from datetime import date, timedelta
from random import randint, choice, random


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def random_date():
    start_date = date(2000, 1, 1)
    years = 19
    end_date = timedelta(years*365)
    random_date = (start_date + end_date * random()).strftime('%m/%d/%Y')
    return random_date


def write_file():
    with open('exercise.csv', 'w') as filename:
        for i in range(1000000):
            l = []
            l.append(uuid.uuid4())
            l.append(i+1)
            l.append(i+2)
            l.append(i+3)
            l.append(i+4)
            l.append(random_date())
            l.append(choice(['ao', None]))
            writer = csv.writer(filename, lineterminator='\n')
            writer.writerow(l)
        logger.info('finished writing file')


if __name__ == '__main__':
    write_file()
