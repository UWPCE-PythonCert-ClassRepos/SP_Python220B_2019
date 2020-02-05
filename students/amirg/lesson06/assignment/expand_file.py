'''
This file expands the exercise csv file from 10
to 1,000,000 records
'''
#pylint: disable=redefined-builtin
import csv
import uuid
import logging
import random
import time

#format for the log
LOG_FORMAT = "%(asctime)s %(filename)s: %(lineno)-3d %(levelname)s %(message)s"

#setup for formatter and log file
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = 'db.log'

#setup for file hanlder at error level
FILE_HANDLER = logging.FileHandler(LOG_FILE, mode='w')
FILE_HANDLER.setLevel(30)
FILE_HANDLER.setFormatter(FORMATTER)

#setup for console handler at debug level
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(10)
CONSOLE_HANDLER.setFormatter(FORMATTER)

#setup for logging set at debug level
LOGGER = logging.getLogger()
LOGGER.setLevel(10)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

#dict to convert debug input to log level
LOG_LEVEL = {'0': 51, '1': 40, '2': 30, '3': 10}

def expand_data(directory_name, input_file):
    '''
    This module expands the data in the csv file
    '''
    #logging.debug('Attempting to open %s', input_file)
    try:
        with open(directory_name + "/" + input_file, 'a', newline='') as file:
            expanded_writer = csv.writer(file, delimiter=',',
                                         quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #logging.debug('Successfully opened file %s', input_file)
            for i in range(11, 1000001, 1):
                new_list = []
                rand_uuid = str(uuid.uuid4())
                logging.debug('Generated random uuid')
                rand_date = random_date('1/1/2010', '12/31/2020', random.random())
                logging.debug('Generated random date')
                rand_string = random.choice(['', 'ao'])
                logging.debug('Generated random string')
                new_list = [rand_uuid, i, i+1, i+2, i+3, rand_date, rand_string]
                expanded_writer.writerow(new_list)
            logging.debug('Successfully expanded data')

    except FileNotFoundError:
        logging.error('Could not open file')



def str_time_prop(start, end, format, prop):
    '''
    Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    '''

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    '''
    Generates a random date
    '''
    return str_time_prop(start, end, '%m/%d/%Y', prop)

if __name__ == "__main__":
    expand_data(r'C:/Users/Amir G/SP_Python220B_2019/students/amirg/lesson06/assignment/data',
                'exercise.csv')
