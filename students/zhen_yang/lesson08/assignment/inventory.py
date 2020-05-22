# inventory.py
""" This module defines functions to initially create, and subsequently update
    a CSV file that lists which furniture is rented to which customer.
"""
import logging
from functools import partial

# set logging configuration
LOG_FORMAT = "%(levelname)s %(filename)s %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """ This function creates invoice_file .csv if it doesn't exit or append
        new line to it if it does. It will write 'customer_name,itemcode,
        item_description,item_monthly_price' to the .csv file.
    """
    the_list = [customer_name, ',', item_code, ',',
                item_description, ',', str(item_monthly_price)]
    with open(invoice_file, 'a') as outfile:
        outfile.write(''.join(the_list))
        outfile.write('\n')

def single_customer(customer_name, invoice_file):
    """ This function returns a function that will iterate through rental_items
        and add each item to invoice_file.
    """
    def add_item(rental_items_file):
        simple_add = partial(add_furniture, invoice_file, customer_name)
        with open(rental_items_file, 'r') as infile:
            for line in infile:
                item = list(line.strip('\n').split(','))
                simple_add(item[0], item[1], item[2])
    return add_item
