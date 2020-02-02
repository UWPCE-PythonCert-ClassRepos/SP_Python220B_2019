import random
import csv
import uuid
from datetime import date

DATA_FILE = 'exercise.csv'
START_DATE_ORD = 730000
END_DATE_ORD = 737373

MY_LIST = list(range(1,1000001))

def gen_row(num):
    return [uuid.uuid4(), str(num), str(num + 1), str(num + 2), str(num + 3), gen_date(), gen_oa()]

def gen_date():
    return date.fromordinal(random.randrange(START_DATE_ORD, END_DATE_ORD)).strftime("%m/%d/%Y")

def gen_oa():
    choices = 'ao','',''
    return random.choice(choices)

with open(DATA_FILE, mode = 'w', newline = '') as f:
    w = csv.writer(f)
    for i in MY_LIST:
        w.writerow(gen_row(i))