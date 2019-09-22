'''
Module to replace existing inventory spreadsheet
'''
import os
import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    '''
    Add furntiture information to csv file

    Args:
        invoice_file (str):
            Path to new or existing csv file
        customer_name (str):
            Customer name
        item_code (str):
            Code for item to add
        item_description (str):
            Description of item to add
        item_monthly_price (int):
            Price of item to add
    '''
    # Set flag to append/write based on existence of file
    flag = 'a' if os.path.exists(invoice_file) else 'w'
    with open(invoice_file, flag) as csv_file:
        csv_file.write('{},{},{},{:0.2f}\n'.format(customer_name,
                                                   item_code,
                                                   item_description,
                                                   item_monthly_price))

def single_customer(customer_name, invoice_file):
    '''
    Add furntiture data from csv file for single customer to new or existing
    csv file

    Args:
        customer_name (str):
            Customer name
        invoice_file (str):
            New or existing csv file to add rental items to
    '''
    def add_rentals(rental_items):
        '''
        Add rental items from existing csv file to new or existing csv file.
        Uses partial function to fix first two inputs of existing add_furniture
        function

        Args:
            rental_items (str):
                Path to csv file with furnture items to add

        Returns:
            add_rentals (function):
                Function that takes the existing csv file as input and makes
                use of currying to add the items to the csv file entered in the
                closure function with the customer name provided
        '''
        # Use partial to fix first two arguments of add_furniture
        add_furniture_curried = partial(add_furniture,
                                        invoice_file=invoice_file,
                                        customer_name=customer_name)
        # Open existing csv file and write items to new or existing csv file
        # Makes use of curried version of add_furniture
        with open(rental_items, 'r') as rental_file:
            csv_reader = csv.reader(rental_file)
            for row in csv_reader:
                item_code, item_description, item_monthly_price = row
                add_furniture_curried(item_code=item_code,
                                      item_description=item_description,
                                      item_monthly_price=float(item_monthly_price))
    return add_rentals
