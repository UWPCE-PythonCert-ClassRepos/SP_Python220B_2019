"""
    Lesson 08 main module.

"""

import csv
import logging
from functools import partial
import os


# Setup logging
CONSOLE_LOG_FORMAT = "%(filename)s:%(lineno)-4d %(message)s"
CONSOLE_FORMATTER = logging.Formatter(CONSOLE_LOG_FORMAT)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.WARNING)
CONSOLE_HANDLER.setFormatter(CONSOLE_FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Add the furniture items rented to customers to the invoice_file .csv in the following format
        customer_name,item_code,item_description,item_monthly_price
    Will create invoice_file if it doesn't exist or append a new line to it if it does.

    :param invoice_file: .csv file
    :param customer_name: string
    :param item_code: string
    :param item_description: string
    :param item_monthly_price: int
    :return: None
    """
    field_names = ['customer_name', 'item_code', 'item_description', 'item_monthly_price']
    # Test if file exists
    if not os.path.exists(invoice_file):
        with open(invoice_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()

    with open(invoice_file, 'a', newline='') as file:
        logging.debug('%s found, appending data.', file.name)
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writerow({'customer_name': customer_name,
                         'item_code': item_code,
                         'item_description': item_description,
                         'item_monthly_price': item_monthly_price})


def single_customer(customer_name, invoice_file):
    """
    Return a function that takes rental items and adds them to the invoice_file. Return function
    will leverage the add_furniture() func using functools.partial
    :param customer_name: string
    :param invoice_file: string
    :return: f(rental_items)
    """
    def single_customer_bulk(rental_items):
        # Use functools.partial
        partial_add = partial(add_furniture, invoice_file=invoice_file, customer_name=customer_name)
        # Read/write bulk records
        with open(rental_items, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                partial_add(item_code=row[1], item_description=row[2], item_monthly_price=row[3])

    return single_customer_bulk
