'''Generates 1 million entries formatted like the exercise.csv'''

# Checklist:
# (1) Takes the data file and expands it to 10^6 entries
# (2) Generage a guid in each column

import csv
import random
from datetime import date
from  uuid import uuid4

# This is not a UUID ):
# def rand_string_generator():
#     '''Generates a random string of length using a-f and 0-9 alphanum characters'''
#     rand_string = ''.join([random.choice('abcdef' + string.digits) for i in range(8)] + ['-'] +
#                           [random.choice('abcdef' + string.digits) for i in range(4)] + ['-'] +
#                           [random.choice('abcdef' + string.digits) for i in range(4)] + ['-'] +
#                           [random.choice('abcdef' + string.digits) for i in range(4)] + ['-'] +
#                           [random.choice('abcdef' + string.digits) for i in range(12)])
#     return rand_string

def rand_date_generator():
    '''Generates a random date from the 1/01/10 to today'''
    start = date(2010, 1, 1)  # (Year, Month, Day)
    end = date.today()
    rand_date = start + (end - start) * random.random()
    return rand_date.strftime('%m/%d/%y')

def rand_ao_generator():
    '''Returns either a NULL or ao'''
    i = random.randint(0, 1)
    if i == 1:
        return 'ao'
    return ''

with open('data/exercise_million.csv', mode='a', newline='', encoding='utf-8-sig') as filename:
    NUM = 1
    for NUM in range(1000000):
        entry = [uuid4(), NUM+1, NUM+2, NUM+3, NUM+4, rand_date_generator(), rand_ao_generator()]
        writer = csv.writer(filename)
        writer.writerow(entry)
        NUM += 1
