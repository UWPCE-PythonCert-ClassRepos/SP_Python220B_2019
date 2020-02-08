"""Module to replace existing spreadsheet"""

# pylint: disable=line-too-long

import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """Write data to the given invoice_file"""
    with open(invoice_file, 'a') as csvfile:
        writer = csv.writer(csvfile)
        try:
            writer.writerow([customer_name, item_code, item_description, "{:.2f}".format(item_monthly_price)])
        except ValueError:
            writer.writerow([customer_name, item_code, item_description, item_monthly_price])
    return 'done'

def single_customer(customer_name, invoice_file):
    """Return a function that takes one parameter, rental_items"""
    # Create partial function to reuse customer_name and invoice_file
    simple_add_furniture = partial(add_furniture, customer_name=customer_name, invoice_file=invoice_file)
    def add_rental(rental_items):
        """Iterate through rental_items and add each item to invoice_file"""
        with open(rental_items) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            # Loop thru each row
            for row in reader:
                simple_add_furniture(item_code=row[0], item_description=row[1], item_monthly_price=row[2])
        return 'done'
    return add_rental
