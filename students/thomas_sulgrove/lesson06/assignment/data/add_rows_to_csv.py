"""Generate csvs for the project"""

from random import randrange, randint
from datetime import datetime, timedelta
import uuid
import csv

def random_string():
    """Return ao"""
    if randint(0, 10) <= 3:
        return 'ao'
    return ''

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    date_time = start + timedelta(seconds=random_second)
    return date_time.date().strftime('%m/%d/%Y')

DATE_START = datetime.strptime('01/01/2010', '%m/%d/%Y')
DATA_END = datetime.strptime('01/01/2019', '%m/%d/%Y')

with open('students/thomas_sulgrove/lesson06/assignment/data/exercise.csv', 'r+') as file:
    ROW_NUM = sum(1 for line in csv.reader(file))
    while ROW_NUM <= 1000000:
        NEW_ROW = ('\n{},{},{},{},{},{},{}'.format(str(uuid.uuid4()),
                                                   ROW_NUM + 1, ROW_NUM + 2, ROW_NUM + 3,
                                                   ROW_NUM + 4,
                                                   str(random_date(DATE_START, DATA_END)),
                                                   random_string()))
        file.write(NEW_ROW)
        ROW_NUM += 1
