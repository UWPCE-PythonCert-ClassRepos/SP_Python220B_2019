"""Module for inventory"""

import csv
import logging
from functools import partial

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """Create an invoice_file"""
    LOGGER.info("Opening invoice file")
    with open(invoice_file, "a+", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([customer_name, item_code, item_description,
                         item_monthly_price])
        LOGGER.info("Added something")

def single_customer(customer_name, invoice_file):
    """Iterate through rental_items and add each item to invoice_file"""
    pass
