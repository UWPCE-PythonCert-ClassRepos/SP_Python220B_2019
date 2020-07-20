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
        pass
    return customer_rental
