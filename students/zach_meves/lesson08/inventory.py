"""
inventory.py

Zach Meves
Python 220
Assignment 8
"""

import os
from functools import partial

FMODE = {True: 'a', False: 'w'}  # File mode to use


def add_furniture(invoice_file: str, customer_name: str, item_code: str,
                  item_description: str, item_monthly_price: float):
    """
    This function will create invoice_file (to replace the spreadsheet’s data) if
    it doesn’t exist or append a new line to it if it does. The contents of the line
    will reflect the customer name and the rented furniture information.

    :param invoice_file: str, file to modify or create.
    :param customer_name: str, name of customer renting the furniture
    :param item_code: str, furniture ID code
    :param item_description: str, furniture description
    :param item_monthly_price: float, price per month of rental
    """

    if not invoice_file.endswith(".csv"):
        raise ValueError("invoice_file must be a .csv file")

    file = open(invoice_file, FMODE[os.path.exists(invoice_file)])

    try:
        file.write(",".join((customer_name, item_code, item_description,
                             f"{item_monthly_price:.2f}")) + '\n')
    except TypeError:
        file.close()
        raise

    file.close()


def single_customer(customer_name: str, invoice_file: str):
    """
    Return a function that will modify the invoice_file for a customer given
    a CSV file containing item rentals.

    :param customer_name: str, name of customer to generate bulk-addition function for
    :param invoice_file: str, name of invoice file to modify
    :return: function that accepts a file name containing furniture to add for the
             customer.
    """

    # Create partial function for use internally
    part_fun = partial(add_furniture, invoice_file, customer_name)

    def return_fun(rentals: str):
        with open(rentals) as file:
            for line in file:  # Iterate over lines (code, desc, price)
                elements = line.split(',')
                part_fun(*elements[:2], float(elements[2]))

    return return_fun
