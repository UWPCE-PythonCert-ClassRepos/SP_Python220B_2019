'''
Module to Generate 1 million random entries formatted like the exercise.csv
'''
import csv
import random
import datetime
from  uuid import uuid4

def random_date():
    '''
    calculate the number of days between today and 01/01/2010
    and returns a random date between the two
    '''
    end = datetime.date.today()
    start = datetime.date(2010, 1, 1)
    random_day = start+(end - start) * random.random()
    return random_day.strftime('%m/%d/%Y') #MM/DD/YYYY

def random_ao():
    '''
    randomly return string: ao
    '''
    return random.choice(['ao', ''])


def random_records():
    '''
    write one million random records to csv file
    '''
    with open('data/exercise_million.csv', mode='a', newline='', encoding='utf-8-sig') as filename:
        i = 1
        for i in range(1000000):
            entry = [uuid4(), i+1, i+2, i+3, i+4, random_date(), random_ao()]
            writer = csv.writer(filename)
            writer.writerow(entry)
            i += 1

if __name__ == '__main__':
    random_records()
