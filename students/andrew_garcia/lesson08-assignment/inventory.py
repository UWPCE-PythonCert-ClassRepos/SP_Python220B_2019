""" Manages a CSV rental file related to a customer """

import csv
import logging
from functools import partial

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """Adds a rental to an CSV file"""
    LOGGER.info('Opening File')
    with open(invoice_file, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([customer_name, item_code, item_description, item_monthly_price])
        LOGGER.info('Rental Added to File')


def single_customer(customer_name, invoice_file):
    """ Adds items to a single customers invoice file """
    def rental_items(rentals_file):
        rental = partial(add_furniture, invoice_file, customer_name)
        LOGGER.info('Opening Rentals File')
        with open(rentals_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                rental(row[1], row[2], row[3])
            LOGGER.info('Adding Rental Info')
    return rental_items
