'''
file to expand exercise to 1 million entries
'''

import csv
import uuid
import random
from datetime import date

def gen_random_date():
    '''generates a random date between today and 2010'''
    start = date(2010, 1, 1)
    end = date.today()
    random_date = start + (end-start) * random.random()
    return random_date.strftime('%m/%d/%Y')

def ao_func():
    '''randomly returns either blank or "ao" '''
    k = random.randint(0, 1)
    if k == 1:
        return 'ao'
    return ''

with open('data/exercise.csv', 'a') as csvfile:
    NUM = 11
    for i in range(1000000):
        new_entry = [uuid.uuid4(), NUM, NUM + 1, NUM + 2, NUM + 3, gen_random_date(), ao_func()]
        writer = csv.writer(csvfile)
        writer.writerow(new_entry)
        num += 1
