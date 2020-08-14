# Stella Kim
# Assignment 8: Functional Techniques

"""
Create program to create and update a CSV file.  Additionally, create
functionality to load individual customers rentals.
"""

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """Create and update a CSV file that lists furniture rented to customers"""
    filename = f'{invoice_file}.csv'
    with open(filename, 'a', newline='') as file:
        data_file = csv.writer(file, quoting=csv.QUOTE_NONE)
        row = (customer_name,
               item_code,
               item_description,
               f'{item_monthly_price:.2f}')
        data_file.writerow(row)


def single_customer(customer_name, invoice_file):
    """Load customer rentals"""
    filename = f'{invoice_file}.csv'
    with open(filename, 'r', newline='') as file:

    def rentals(rental_items):

    return rentals

    # single_customer needs to use functools.partial and closures, in order
    # to return a function that will iterate through rental_items and add
    # each item to invoice_file.

    # The idea is for the single_customer() function to return a new function
    # (with a fixed customer name and destination inventory file) that will
    # add all items in a source file to the overall inventory under a single
    # customer name. Internally, single_customer() should leverage
    # add_furniture() by fixing the first two parameters.


if __name__ == "__main__":
    add_furniture('rented_items', 'John Smith', 'KT28', 'Blender', 15)
    # single_customer('Sandra Lee', 'rented_items')
