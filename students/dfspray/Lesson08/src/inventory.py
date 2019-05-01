"""
This program will contain all the functions used for this assignment
"""

import csv
import os
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """This function will create invoice_file (to replace the spreadsheet’s data) if it
       doesn’t exist or append a new line to it if it does"""

    with open(os.path.join(os.path.dirname(__file__), invoice_file), 'a') as invoices:
        invoice_writer = csv.writer(invoices, delimiter=',', lineterminator='\n')
        invoice_row = [customer_name, item_code, item_description, item_monthly_price]
        invoice_writer.writerow(invoice_row)

def single_customer(customer_name, invoice_file):
    """This function returns a function that takes 'rental_items' as a parameter"""
    def rentals_iterator(rental_items):
        with open(os.path.join(os.path.dirname(__file__), rental_items)) as invoices:
            invoice_reader = csv.reader(invoices, delimiter=',', quotechar='"')
            add_items = partial(add_furniture, invoice_file=invoice_file,
                                customer_name=customer_name)
            for row in invoice_reader:
                add_items(item_code=row[0], item_description=row[1], item_monthly_price=row[2])
    return rentals_iterator
