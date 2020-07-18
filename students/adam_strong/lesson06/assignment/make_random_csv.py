''' make_random_csv.py

This will generate a x ROWS 7 column random data set with
IIUD, ordinal IDs, random dates, numbers and categoricals
'''

import csv
import random
import datetime
import uuid

START_DATE = datetime.date(2010, 1, 1)
END_DATE = datetime.date(2020, 7, 1)
TIME_BETWEEN = END_DATE - START_DATE
DAYS_BETWEEN = TIME_BETWEEN.days


ROWS = 1000000

def make_random_csv(rows):
    '''This makes x ROWS of randomly generated csv data over 7 columns'''
    with open('random_million_rows.csv', 'w', newline='') as csvfile:
        random_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in range(rows):
            row1_id = uuid.uuid4() #random UUID from uuid library
            row2_num = row + 1 #Unique ordinal identifying integer
            row3_num = random.randrange(1, 12)
            row4_num = random.randrange(1, 12)
            row5_num = random.randrange(1, 12)
            random_days = random.randrange(DAYS_BETWEEN)
            row6_date_temp = START_DATE + datetime.timedelta(days=random_days)
            row6_date = row6_date_temp.strftime("%m/%d/%Y")
            ao_seed = random.randrange(1, 3)
            if ao_seed == 1:
                row7_ao = 'ao'
            else:
                row7_ao = ''
            random_writer.writerow([(row1_id), (row2_num), (row3_num), (row4_num),
                                    (row5_num), (row6_date), (row7_ao)])

if __name__ == '__main__':
    make_random_csv(ROWS)
