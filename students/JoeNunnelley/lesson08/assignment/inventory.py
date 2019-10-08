#! /usr/bin/env python3

"""
Assignment

You will create a program to initially create, and subsequently update, a CSV
file that lists which furniture is rented to which customer (to replace use of
the spreadsheet mentioned above).

You will create additionally functionality that will load individual customers
rentals.

Testing

You can create the test_items.csv file for testing of your single_customer
function. The layout of the csv will be something like this:

    LR04,Leather Sofa,25.00
    KT78,Kitchen Table,10.00
    BR02,Queen Mattress,17.00

add_furniture can be tested manually, as shown below.

The idea is for the single_customer() function to return a new function (with a
fixed customer name and destination inventory file) that will add all items in
a source file to the overall inventory under a single customer name.
Internally, single_customer() should leverage add_furniture() by fixing the
first two parameters.

from inventory import *
add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
add_furniture("rented_items.csv", "Alex Gonzales", "Queen Mattress", 17)
create_invoice = single_customer("Susan Wong", "rented_items.csv")
create_invoice("test_items.csv")
"""
import csv
import json
import logging
from os import path, remove
import pandas as pd

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger('console')
FH = logging.FileHandler('inventory.log', 'w+')
FH.setLevel(logging.DEBUG)
FORMATTER = logging.Formatter(FORMAT)
FH.setFormatter(FORMATTER)
LOGGER.addHandler(FH)


def csv_to_json(directory_name, filename):
    """ Load a csv file to a list """
    path_file = directory_name + "/" + filename
    if path.isfile(path_file):
        LOGGER.debug('Loading file: %s', path_file)
        data = pd.read_csv(path_file)
        return json.loads(data.to_json(orient='records'))

    LOGGER.error('Failed to load file: %s', path_file)
    return {}


def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """
    Create a function called add_furniture that takes the following input
    parameters:

        invoice_file
        customer_name
        item_code
        item_description
        item_monthly_price

    This function will create invoice_file (to replace the spreadsheet’s
    data) if it doesn’t exist or append a new line to it if it does. After
    adding a few items to the same file, the file created by add_furniture
    should look something like this:

    Elisa Miles,LR04,Leather Sofa,25.00$
    Edward Data,KT78,Kitchen Table,10.00$
    Alex Gonzales,BR02,Queen Mattress,17.00
    """
    LOGGER.debug("%s %s %s %s %s", invoice_file, customer_name, item_code,
                 item_description, item_monthly_price)
    LOGGER.debug("Add furniture")

    write_header = not path.exists(invoice_file)

    with open(invoice_file, mode='a', newline='') as csv_file:
        fieldnames = ['RENTER_NAME',
                      'PRODUCT_ID',
                      'PRODUCT_NAME',
                      'MONTHLY_PRICE']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        writer.writerow({'RENTER_NAME': customer_name,
                         'PRODUCT_ID': item_code,
                         'PRODUCT_NAME': item_description,
                         'MONTHLY_PRICE': float(item_monthly_price)})


def single_customer(customer_name, invoice_file):
    """
    Create a function called single_customer:

        Input parameters: customer_name, invoice_file.
        Output: Returns a function that takes one parameter, rental_items.

    single_customer needs to use functools.partial and closures, in order
    to return a function that will iterate through rental_items and add
    each item to invoice_file.
    """

    def create_invoice(rental_items):
        """
        Function to create an invoice from the list of rentals for a specific
        user
        """
        rentals = csv_to_json('.', rental_items)
        LOGGER.debug("Creating invoice for %s", customer_name)
        invoice = []

        for rental in rentals:
            LOGGER.debug("Adding : %s", rental)
            invoice.append(rental)
            add_furniture(invoice_file, customer_name, rental['PRODUCT_ID'],
                          rental['PRODUCT_NAME'], rental['MONTHLY_PRICE'])

    return create_invoice


def main():
    """
    So, using create_invoice() will, in this case, add all items in
    test_items.csv to rented_items.csv under the name 'Susan Wong'.
    """
    invoice_file = 'rented_items.csv'
    if path.exists(invoice_file):
        remove(invoice_file)

    items = csv_to_json('.', 'test_items.csv')
    LOGGER.debug(items)
    add_furniture("rented_items.csv", "Elisa Miles",
                  "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data",
                  "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales",
                  "BR02", "Queen Mattress", 17)
    create_invoice = single_customer("Elisa Miles", invoice_file)
    create_invoice('test_items.csv')


if __name__ == "__main__":
    main()
