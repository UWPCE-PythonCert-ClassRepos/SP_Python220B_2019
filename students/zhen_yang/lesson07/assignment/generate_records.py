# generate_records.py
""" This module randomly generate thround of customer records, product records
    and rental records.
"""

import string
import random
import logging

# set logging configuration
LOG_FORMAT = "%(levelname)s %(filename)s %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def customer_record_generator(record_num, filename):
    """ This function randomly generate custmer records """
    LOGGER.debug('--- Start randomly generate customer records ---')
    # 1. generate the head line
    head_line = 'user_id,name,address,phone_number,email'
    email_list = ['yahoo.com', 'hotmail.com', 'uw.edu', 'gmail.com']
    # 2. generate each record
    with open(filename, 'w') as file:
        file.write(head_line + '\n')
        for num in range(6, record_num):
            customer_str = 'user' + str(num) + ',' + \
                ''.join(random.choices(string.ascii_uppercase, k=1)) +\
                ''.join(random.choices(string.ascii_lowercase, k=4)) + ' ' + ''\
                ''.join(random.choices(string.ascii_uppercase, k=1)) +\
                ''.join(random.choices(string.ascii_lowercase, k=4)) + ',' + ''\
                ''.join(random.choices(string.digits, k=4)) + ' ' + ''\
                ''.join(random.choices(string.ascii_uppercase, k=1)) + \
                ''.join(random.choices(string.ascii_lowercase, k=4)) + ' ' + ''\
                ''.join(random.choices(['Street', 'Avenue'], k=1)) + ',' + ''\
                ''.join(random.choices(string.digits, k=3)) + '-' + ''\
                ''.join(random.choices(string.digits, k=3)) + '-' + ''\
                ''.join(random.choices(string.digits, k=4)) + ',' + ''\
                ''.join(random.choices(string.ascii_lowercase, k=4)) + '@' + ''\
                ''.join(random.choices(email_list, k=1))
            file.write(customer_str + '\n')
    LOGGER.debug('--- End randomly generate customer records ---')

def product_record_generator(record_num, filename):
    """ This function randomly generate product records """
    LOGGER.debug('--- Start randomly generate product records ---')
    # 1. generate the head line
    head_line = 'product_id,description,product_type,quantity_available'
    # 2. generate each record
    description_list = ['60-inch TV stand,livingroom',
                        'L-shaped sofa,livingroom',
                        'dishwasher,kithen', 'microwave oven,kitchen',
                        'queen size bed,bedroom']
    with open(filename, 'w') as file:
        file.write(head_line + '\n')
        for num in range(6, record_num):
            product_str = 'prd' + str(num) + ',' + \
                ''.join(random.choices(description_list, k=1)) + ',' + ''\
                ''.join(random.choices(string.digits, k=1))
            file.write(product_str + '\n')
    LOGGER.debug('--- End randomly generate product records ---')


def rental_record_generator(record_num, filename):
    """ This function randomly generate rental records """
    LOGGER.debug('--- Start randomly generate rental records ---')
    # 1. generate the head line
    head_line = 'product_id,user_id'
    with open(filename, 'w') as file:
        file.write(head_line + '\n')
        for num in range(6, record_num):
            rental_str = 'prd' + str(num) + ',' + 'user' +\
                         str(random.randint(6, 999))
            file.write(rental_str + '\n')
    LOGGER.debug('--- End randomly generate rental records ---')

def generate_data_file(record_num, filename, file_flag):
    """ This function generate random records and write thenm to a .csv file """
    if file_flag == 1:
        product_record_generator(record_num, filename)
    if file_flag == 2:
        customer_record_generator(record_num, filename)
    if file_flag == 3:
        rental_record_generator(record_num, filename)
