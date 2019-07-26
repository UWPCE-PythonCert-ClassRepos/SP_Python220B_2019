""" Data generation"""

import uuid
import random
from datetime import date


def random_uuid():
    """Random UUID"""
    return uuid.uuid4()


def random_gene():
    """Generate a random number"""
    for i in range(10):
        return random.randint(1, 21)


def random_date():
    """Generate a Random date"""
    start_dt = date.today().replace(day=1, month=1, year=2013).toordinal()
    end_dt = date.today().toordinal()
    random_day = date.fromordinal(random.randint(start_dt, end_dt)).strftime('%m/%d/%Y')
    return random_day


END = ["ao", ""]

FILE = open('exercise.csv', 'w')

for j in range(1000000):
    uid = random_uuid()
    first = random_gene()
    second = random_gene()
    third = random_gene()
    fourth = random_gene()
    ran_date = random_date()
    end_ch = random.choice(END)
    FILE.write(f'{uid},{first},{second},{third},{fourth},{ran_date},{end_ch}\n')
FILE.close()
