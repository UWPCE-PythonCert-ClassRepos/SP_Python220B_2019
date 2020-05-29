""" Add lines to the data file """

import csv
import uuid
from datetime import date
import random

START_DATE = date(2000, 1, 1).toordinal()
END_DATE = date(2020, 1, 1).toordinal()

with open(r'customers.csv', 'w', newline='') as f:
    WRITER = csv.writer(f)
    for row in range (1,1000):
        WRITER.writerow(['user'+str(row), 'name'+str(row), 'address'+str(row), 'phone_num'+str(row), 'email'+str(row)])

with open(r'products.csv', 'w', newline='') as f:
    WRITER = csv.writer(f)
    for row in range (1,1000):
        WRITER.writerow(['product'+str(row), 'item'+str(row), 'room'+str(row), random.randint(1,10)])

with open(r'rentals.csv', 'w', newline='') as f:
    WRITER = csv.writer(f)
    for row in range (1,1000):
        WRITER.writerow(['product'+str(row), 'user'+str(row), date.fromordinal(random.randint(START_DATE, END_DATE)),
                         date.fromordinal(random.randint(START_DATE, END_DATE)), random.randint(1,10)])
