'''
Module to replace existing inventory spreadsheet
'''
import os

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
        pass
