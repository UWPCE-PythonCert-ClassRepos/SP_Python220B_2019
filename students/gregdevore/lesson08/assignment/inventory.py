'''
Module to replace existing inventory spreadsheet
'''
import os
import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    # Set flag to append/write based on existence of file
    flag = 'a' if os.path.exists(invoice_file) else 'w'
    with open(invoice_file, flag) as csv_file:
        csv_file.write('{},{},{},{:0.2f}\n'.format(customer_name,
                                                   item_code,
                                                   item_description,
                                                   item_monthly_price))

def single_customer(customer_name, invoice_file):
    def add_rentals(rental_items):
        add_furniture_curried = partial(add_furniture, invoice_file=invoice_file, customer_name=customer_name)
        with open(rental_items,'r') as rental_file:
            csv_reader = csv.reader(rental_file)
            for row in csv_reader:
                item_code, item_description, item_monthly_price = row
                add_furniture_curried(item_code=item_code,
                                      item_description=item_description,
                                      item_monthly_price=float(item_monthly_price))
    return add_rentals
