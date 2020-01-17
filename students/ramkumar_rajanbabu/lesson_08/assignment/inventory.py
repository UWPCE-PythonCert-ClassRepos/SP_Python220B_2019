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
    def return_rental(rental_file):
    	""""""
    	# partial makes a new version with arguments filled in
    	rental = partial(add_furniture, invoice_file, customer_name)
    	with open(rental_file, "r", newline="") as file:
	        reader = csv.reader(file)
	        for row in reader:
	        	item_code = row[0]
	        	item_description = row[1] 
	        	item_monthly_price = row[2]
	        	rental(item_code, item_description, item_monthly_price)
    return return_rental


if __name__ == "__main__":
    