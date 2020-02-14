"""
Module to replace direct use of csv file with functions.
"""

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """Add furniture details to invoice file."""
    with open(invoice_file, 'a', newline='') as file:
        append_file = csv.writer(file)
        append_file.writerow([customer_name, item_code, item_description, item_monthly_price])


def single_customer(customer_name, invoice_file):
    """Return function adding furniture in rental items to invoice file under customer's name."""
    def return_function(rental_items):
        func = partial(add_furniture, invoice_file, customer_name)
        with open(rental_items, 'r') as file:
            for row in csv.reader(file):
                func(*row)
    return return_function
