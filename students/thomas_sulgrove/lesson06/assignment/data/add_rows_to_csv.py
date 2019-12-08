from random import randrange, randint
from datetime import datetime, timedelta
import uuid
import csv

def random_string():
    if randint(0, 10) <=3:
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

date_start = datetime.strptime('01/01/2010', '%m/%d/%Y')
date_end = datetime.strptime('01/01/2019', '%m/%d/%Y')

with open('students/thomas_sulgrove/lesson06/assignment/data/exercise.csv', 'r+') as file:
    row_num = sum(1 for line in csv.reader(file))
    while row_num <= 1000000:
        new_row = ('\n{},{},{},{},{},{},{}'.format(str(uuid.uuid4()), row_num + 1, row_num + 2, row_num + 3,
                                                   row_num + 4, str(random_date(date_start, date_end)), random_string()))
        file.write(new_row)
        row_num += 1
