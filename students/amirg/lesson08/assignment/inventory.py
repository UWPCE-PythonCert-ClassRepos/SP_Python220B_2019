'''
This file contains the functions to add
information to an inventory database
'''

import csv
import logging
from functools import partial

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

def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    '''adds furniture information to a specified file'''
    with open(invoice_file, 'a+', newline='') as file:
        data_writer = csv.writer(file, delimiter=',',
                                 quotechar='"', quoting=csv.QUOTE_MINIMAL)
        new_item = [customer_name, item_code, item_description, item_monthly_price]
        data_writer.writerow(new_item)


def single_customer(customer_name, invoice_file):
    '''returns a function that goes through a rental file
       and adds specified info to the inventory database'''
    def add_cust_rental(rental_items):
        furniture_partial = partial(add_furniture, invoice_file=invoice_file,
                                    customer_name=customer_name)
        with open(rental_items, 'r') as file:
            data_reader = csv.reader(file, delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            for row in data_reader:
                furniture_partial(item_code=row[0],
                                  item_description=row[1], item_monthly_price=row[2])
    return add_cust_rental

