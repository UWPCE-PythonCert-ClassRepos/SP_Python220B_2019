'''Module inventory.py'''
import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    '''Creates and/or updates invoice_file'''
    with open(invoice_file, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([customer_name, item_code, item_description, item_monthly_price])

def single_customer(customer_name, invoice_file):
    '''Iterates through rental_items adding each item to invoice_file.'''
    def rental_items(rentals_file):
        rental = partial(add_furniture, invoice_file, customer_name)
        with open(rentals_file, 'r') as csv_file:
            cvs_reader = csv.reader(csv_file)
            for row in cvs_reader:
                rental(*row)
    return rental_items
