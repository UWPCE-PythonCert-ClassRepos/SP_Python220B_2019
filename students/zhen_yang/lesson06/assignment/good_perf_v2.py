# good_perf.py
""" This module defines functions for generating 1 million of records and
    analyzing the generated data.
"""
import string
import random
import sys
import logging
import time
import datetime
#import csv
import cProfile
import pstats
from itertools import islice

# set logging configuration
LOG_FORMAT = "%(levelname)s %(filename)s %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def number_generator(record_num):
    """ This function generate four digits starting from the record_num  """
    element = []
    for i in range(record_num, record_num + 4):
        element.append(str(i))
    return element

def random_date_generator(start, end, proportion):
    """ This function randomly generate a date between start and end time """
    # mktime() convert the time to the seconds passed since epoch in local time
    # localtime() convert the seconds passed since epoch to local time
    # propotion is a random percentage of the elaspsed time
    # between start and end time.
    #format = '%m/%d/%Y'
    start_time = time.mktime(time.strptime(start, '%m/%d/%Y'))
    end_time = time.mktime(time.strptime(end, '%m/%d/%Y'))

    the_elapse_time = start_time + proportion * (end_time - start_time)

    return time.strftime('%m/%d/%Y', time.localtime(the_elapse_time))


def unique_identity_generator(size=1, combine=1):
    """ This function randomly generate a unique identity """
    if combine == 1:
        return ''.join(random.choices(string.digits, k=size))
    if combine == 2:
        return ''.join(random.choices(string.ascii_lowercase +
                                      string.digits, k=size))
    LOGGER.info('Uknown flag for combine:{combine}i!')
    sys.exit()

def record_generator(record_num):
    """ This function randomly generate one record """
    LOGGER.debug('--- Start randomly generate one record ---')
    record = []
    # 1. randomly generate the unique identity
    element = []
    element.append(unique_identity_generator(8, combine=2))
    element.append(unique_identity_generator(4, combine=2))
    element.append(unique_identity_generator(4, combine=2))
    element.append(unique_identity_generator(4, combine=2))
    element.append(unique_identity_generator(12, combine=2))
    # concantonate the five parts of the unique identity
    record.append('-'.join(element))
    record.append(',')

    # 2. randomly generate five single digits.
    record.append(','.join(number_generator(record_num)))
    record.append(',')
    # randomly generate dates.
    r_date = random_date_generator('01/01/2000', '01/01/2020', random.random())
    record.append(r_date)
    record.append(',')

    # 3. randomly generate 'ao' field.
    if random.random() >= 0.5:
        record.append('ao')
    #LOGGER.info(f'Record:{"".join(record)}')
    LOGGER.debug('--- End randomly generate one record ---')
    return ''.join(record)

def generate_data_file(filename):
    """ This function generate random records and write to a .csv file """
    with open(filename, 'w') as file:
        for i in range(1000000):
            the_record = record_generator(i + 1)
            file.write(the_record + '\n')


def analyze(filename):
    """ This function analyzes the date in a .csv file """

    start = datetime.datetime.now()
    # count the number of year: 2013, 2014 ,2015, 2016, 2017, 2018
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    found = 0
    with open(filename, 'r') as file:
        #lines = csv.reader(file, delimiter=',')
        for rows in islice(file, 0, None):
            line = list(rows.strip('\n').split(','))
        #for line in lines:
            if line[5][6:] == '2013':
                year_count['2013'] += 1
            if line[5][6:] == '2014':
                year_count['2014'] += 1
            if line[5][6:] == '2015':
                year_count['2015'] += 1
            if line[5][6:] == '2016':
                year_count['2016'] += 1
            if line[5][6:] == '2017':
                year_count['2017'] += 1
            if line[5][6:] == '2018':
                year_count['2018'] += 1
            if line[6] == 'ao':
                found += 1

    end = datetime.datetime.now()
    # print(f'start time:{start}')
    # print(f'end time:{end}')
    # print(f'year_count:{year_count}')
    # print(f'found "ao":{found}')
    return (start, end, year_count, found)


def main():
    """ This is the main() function """
    # generate one million of records.
    #generate_data_file("data/exercise_new.csv")',
    #filename = "data/exercise_new.csv"

    # set up profiling
    cProfile.run('analyze("data/exercise_new.csv")', 'analyze_good.res')
    #with open('cumulative_good.res', 'w') as file:
    with open('time_good_v2.res', 'w') as file:
        q = pstats.Stats('analyze_good.res', stream=file)

        # find what algorithms are taking time. Only print top 10
        #q.strip_dirs().sort_stats('cumulative').print_stats(10)

        # find what functions were looping a lot and taking a lot of time.
        q.strip_dirs().sort_stats('time').print_stats(10)


if __name__ == "__main__":
    main()
