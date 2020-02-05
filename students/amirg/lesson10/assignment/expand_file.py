'''
This file expands the exercise csv file from 10
to 1,000,000 records
'''
#pylint: disable=redefined-builtin
import csv
import logging
import random
import time


def expand_customers(directory_name, input_file):
    '''
    This module expands the data in the csv file
    '''
    #logging.debug('Attempting to open %s', input_file)
    try:
        with open(directory_name + "/" + input_file, 'a', newline='') as file:
            expanded_writer = csv.writer(file, delimiter=',',
                                         quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #logging.debug('Successfully opened file %s', input_file)
            for i in range(5, 10000, 1):
                new_list = []
                rand_name = random.choice(['John Doe', 'Jane Doe'])
                rand_add = random.randint(100, 999)
                if rand_name == 'John Doe':
                    rand_email = 'johndoe@gmail.com'
                else:
                    rand_email = 'janedoe@gmail.com'
                logging.debug('Generated random string')
                new_list = ['user' + '{:0>3d}'.format(i), rand_name,
                            str(rand_add) + ' Main St', '123-456-6789', rand_email]
                expanded_writer.writerow(new_list)
            logging.debug('Successfully expanded customers')

    except FileNotFoundError:
        logging.error('Could not open file')

def expand_products(directory_name, input_file):
    '''
    This module expands the data in the csv file
    '''
    #logging.debug('Attempting to open %s', input_file)
    try:
        with open(directory_name + "/" + input_file, 'a', newline='') as file:
            expanded_writer = csv.writer(file, delimiter=',',
                                         quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #logging.debug('Successfully opened file %s', input_file)
            for i in range(5, 20000, 1):
                new_list = []
                new_list = ['prd' + '{:0>3d}'.format(i), 'object', 'rand_categ',
                            random.randint(1, 10)]
                expanded_writer.writerow(new_list)
            logging.debug('Successfully expanded products')

    except FileNotFoundError:
        logging.error('Could not open file')

def expand_rentals(directory_name, input_file):
    '''
    This module expands the data in the csv file
    '''
    #logging.debug('Attempting to open %s', input_file)
    try:
        with open(directory_name + "/" + input_file, 'a', newline='') as file:
            expanded_writer = csv.writer(file, delimiter=',',
                                         quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #logging.debug('Successfully opened file %s', input_file)
            for i in range(5, 10000, 1):
                new_list = []
                new_list = ['user' + '{:0>3d}'.format(i),
                            'prd005']
                expanded_writer.writerow(new_list)
            logging.debug('Successfully expanded rentals')

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
    expand_customers(r'data', 'customers.csv')
    expand_products(r'data', 'products.csv')
    expand_rentals(r'data', 'rentals.csv')
