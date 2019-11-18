'''
lesson08 assignment
'''

import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    '''adds customer information to invoice csv file'''
    with open(invoice_file, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([customer_name, item_code, item_description, item_monthly_price])

def single_customer(customer_name, invoice_file):
    '''takes a rental csv file and imports all data to invoice file under
    customer name'''
    new_entry = partial(add_furniture, invoice_file, customer_name)
    def read_rentals(file):
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                item_code = row[0]
                item_description = row[1]
                item_monthly_price = row[2]
                new_entry(item_code, item_description, item_monthly_price)
    return read_rentals
