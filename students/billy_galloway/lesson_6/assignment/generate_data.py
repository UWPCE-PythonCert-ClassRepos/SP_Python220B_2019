'''
Generate a million entries
'''
import datetime
from datetime import timedelta
from random import randrange
import random
import csv
import uuid

def random_date():
    ''' generates a random date '''
    start = datetime.datetime.strptime("1/01/2013", '%m/%d/%Y')
    end = datetime.datetime.strptime("12/31/2018", '%m/%d/%Y')
    delta = end - start
    output = start + timedelta(days=randrange(delta.days))

    return output.strftime('%m/%d/%Y')

def write_csv(filename):
    ''' writes a csv file with a million lines of data '''
    num_list = [11, 7]
    with open(filename, 'w') as file:
        file.write(f'guid,count_0,count_1,count_2,count_3,date,ao\n')
        for i in range(1000000):
            number = random.choice(num_list)
            if i % number == 0:
                file.write(f'{str(uuid.uuid1())},{i+1},{i+2},{i+3},{i+4},{random_date()},ao\n')
            else:
                file.write(f'{str(uuid.uuid1())},{i+1},{i+2},{i+3},{i+4},{random_date()}\n')
