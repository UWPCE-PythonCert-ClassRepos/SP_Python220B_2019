""" Imports customer rental data and creates or amends to a csv
 inventory file"""

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """adds to or creates invoice file, adds new line with customer name, item
    code and item monthly price"""
    with open(invoice_file, 'a', newline='') as invoice:
        invoice_write = csv.writer(invoice, delimiter=',')
        invoice_write.writerow([customer_name, item_code, item_description,
                                item_monthly_price])


def single_customer(customer_name, invoice_file):
    """creates a function to add the inventory from a file containing a single
    customers rentals"""
    def rental_function(rental_items):
        """creates the function that adds inventory from a specific customer"""
        with open(rental_items, 'r') as customer_file:
            new_data = csv.reader(customer_file)
            add_customer = partial(add_furniture, invoice_file=invoice_file,
                                   customer_name=customer_name)
            for row in new_data:
                add_customer(item_code=row[0], item_description=row[1],
                             item_monthly_price=row[2])
    return rental_function
