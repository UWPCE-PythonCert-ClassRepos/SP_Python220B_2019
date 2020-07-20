'''
    inventory.py
'''

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """ append to invoices customer info """
    with open(invoice_file, "a+") as invoice_csv:
        csv_writer = csv.writer(invoice_csv, delimiter=',', lineterminator='\n')
        csv_writer.writerow([customer_name, item_code, item_description, item_monthly_price])


def single_customer(customer_name, invoice_file):
    """ define function which curries customer_name and invoice_file for add_furniture"""
    def customer_rental(rental_items):
        """ process rented items """
        customer = partial(add_furniture, invoice_file=invoice_file, customer_name=customer_name)
        with open(rental_items, "r") as rental_csv:
            for row in csv.reader(rental_csv):
                customer(item_code=row[0], item_description=row[1], item_monthly_price=row[2])
    return customer_rental
