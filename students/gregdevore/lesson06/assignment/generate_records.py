'''
Python script to generate 1 million records similar to those in
data/exercise.csv
'''

import random
from uuid import uuid4

def generate_day():
    '''
    Generate a random day (integer between 1 and 31)
    '''
    return random.randint(1, 31)

def generate_month():
    '''
    Generate a random month (integer between 1 and 12)
    '''
    return random.randint(1, 12)

def generate_year():
    '''
    Generate a random year (integer between 2010 and 2019)
    '''
    return random.randint(2010, 2018)

def generate_ints():
    '''
    Generate four random numbers (integers between 1 and 10)
    '''
    return [random.randint(1, 10) for _ in range(4)]

def generate_uuid():
    '''
    Generate a random uuid
    '''
    return str(uuid4())

def generate_newline():
    '''
    Generate a new line for the data source csv file
    '''
    day = generate_day()
    month = generate_month()
    year = generate_year()
    ints = generate_ints()
    uuid = generate_uuid()
    return '\n{},{},{},{},{},{}/{}/{},'.format(uuid, *ints, month, day, year)

if __name__ == "__main__":
    # Generate enough random lines to reach 1,000,000 records
    REPEAT = 999990
    CSV_FILE = 'data/exercise.csv'
    for _ in range(REPEAT):
        # Append new lines to existing csv file
        with open(CSV_FILE, 'a') as filex:
            filex.write(generate_newline())
