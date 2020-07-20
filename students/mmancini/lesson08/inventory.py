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


