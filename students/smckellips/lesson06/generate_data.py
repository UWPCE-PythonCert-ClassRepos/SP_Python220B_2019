'''
Module for expanding data file to 1M records.

Starting data set is 2010 - 2018
Assume start 1/1/2010 and end 12/31/2018

ao appears in 3/11 of the entries.
'''
from _datetime import date, timedelta
from random import randint
from uuid import uuid4


def make_guid():
    '''Generate a guid in some form...'''
    return uuid4()


def make_date():
    '''Generate random date'''
    start = date(2010, 1, 1)
    end = date(2018, 12, 31)

    span = (end - start).days
    ran = randint(0, span)
    ran_date = (start + timedelta(days=ran)).strftime("%m/%d/%Y")
    return ran_date


def make_ao():
    '''Make ao or not ao decision.'''
    # Random from 1-100 compared to % of 3 of 11
    if randint(1, 101) < (3/11*100):
        return 'ao'
    else:
        return ''


def expand_file():
    '''Do the work'''
    filename = 'data/exercise.csv'
    with open(filename, 'a') as out_file:
        lines = 11
        while lines < (1e6 + 1):
            data_string = f'\n{make_guid()},{lines},{lines + 1},{lines +2},{lines +3},{make_date()},{make_ao()}'
            # print(data_string)
            out_file.write(data_string)
            lines +=1

if __name__ == "__main__":
    expand_file()
