"""
create and update an inventory CSV file with all the information
"""

import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """This function will create invoice_file (to replace the spreadsheet’s data)
    if it doesn’t exist or append a new line to it if it does."""


    with open(invoice_file, 'a+', newline='') as csv_file:
        csv_file.write('{},{},{},{:0.2f}\n'.format(customer_name, item_code,
                                                   item_description, item_monthly_price))

def single_customer(customer_name, invoice_file):
    """Input parameters: customer_name, invoice_file.
    Output: Returns a function that takes one parameter, rental_items.
    single_customer needs to use functools.partial and closures,
    in order to return a function that will iterate through rental_items
    and add each item to invoice_file."""

    def return_func(rental_items):
        with open(rental_items) as csv_file:
            csv_reader = csv.reader(csv_file)
            curried_func = partial(add_furniture, invoice_file, customer_name)
            for row in csv_reader:
                curried_func(row[0], row[1], float(row[2]))
    return return_func
