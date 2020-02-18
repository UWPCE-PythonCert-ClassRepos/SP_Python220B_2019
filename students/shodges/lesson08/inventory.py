"""
Functionality to allow inventory management for HP Norton.
"""

import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Add a new record to the CSV invoice_file in this format:

    customer_name,item_code,item_description,item_monthly_price
    """
    with open(invoice_file, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow([customer_name, item_code, item_description, '{:.2f}'.format(item_monthly_price)])


def single_customer(customer_name, invoice_file):
    """
    Returns a curried function that will iterate through a file defined by rental_items and add
    them to the master inventory file, invoice_file, as rented to customer_name.
    """
    def import_from(rental_items):
        """
        Iterate through rental_items and add the discovered records to nonlocal invoice_file.
        Append nonlocal customer_name.
        """
        
