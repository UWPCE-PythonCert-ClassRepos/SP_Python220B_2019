# Advanced Programming In Python - Lesson 8 Assignment 1: Functional Techniques
# RedMine Issue - SchoolOps-18
# Code Poet: Anthony McKeever
# Start Date: 01/16/2019
# End Date: 01/16/2019

"""
A module for supporting relating customer rentals to inventory.
"""

from functools import partial
from os import path


def add_furnature(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """
    Appends customer rentals to an invoice file.
    Creates the invoice file if it doesn't exist.

    :invoice_file:          The invoice file to use.
    :customer_name:         The name of the customer.
    :item_code:             The identified of the rented item.
    :item_description:      The description of the rented item.
    :item_monthly_price:    The monthly rental price of the item
    """
    # Check if file exists and is not empty, if so append new line character to
    # the start of the write value so we don't start the file with a blank line
    use_new_line = path.exists(invoice_file) and path.getsize(invoice_file) > 0
    new_line = "\n" if use_new_line else ""

    write_val = "{0}{1},{2},{3},{4:0.2f}".format(new_line,
                                                 customer_name,
                                                 item_code,
                                                 item_description,
                                                 float(item_monthly_price))

    with open(invoice_file, "a+") as writer:
        writer.write(write_val)


def single_customer(customer_name, invoice_file):
    """
    Return a closure representing a customer.  The closure encompases a the
    method "add_rentals" which accepts a single parameter.

    :invoice_file:          The invoice file to use.
    :customer_name:         The name of the customer.

    Return Value:
        add_rentals(rental_items)
    """
    rental_handler = partial(add_furnature,
                             invoice_file=invoice_file,
                             customer_name=customer_name)

    def add_rentals(rental_items):
        """
        Adds a collection of rented items to the customer's invoice.

        :rental_items:  The path to the customer's rented items CSV file.
        """
        with open(rental_items, "r") as reader:
            # Read file line by line incase the CSV file is giant to prevent
            # out of memory issues.
            item_line = reader.readline()

            while item_line:
                item = item_line.split(',')
                rental_handler(item_code=item[0],
                               item_description=item[1],
                               item_monthly_price=item[2])

                item_line = reader.readline()

    return add_rentals
