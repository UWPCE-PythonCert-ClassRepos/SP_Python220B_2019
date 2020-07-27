#!/usr/bin/env python
""""
Lesson 08 - Using closures, partial from functools and currying
"""

import csv
import os
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    '''This function will create invoice_file (if it doesn't exist) or
    append a new line to it if it does'''
    with open(invoice_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([(customer_name), (item_code), (item_description), (item_monthly_price)])


def single_customer(customer_name, invoice_file):
    '''Uses functools.partial and closure in order to return a function that
    will iterate through rental_items and each item and add each item to the invoice file'''
    part_ref = partial(add_furniture, customer_name=customer_name, invoice_file=invoice_file)
    def return_function(source_csv):
        with open(source_csv, 'r', newline='') as csvfile:
            for row in csvfile:
                row = row[:-1]
                split = row.split(',')
                part_ref(item_code=split[0], item_description=split[1], item_monthly_price=split[2])
    return return_function


# Additional functions ----

def delete_csv(file_name):
    '''This will delete an existing .csv file'''
    try:
        os.remove(file_name)
        return 'Deletion successful'
    except FileNotFoundError:
        return f'The file slated for removal: "{file_name}" doesnt exist'

def read_csv(file_name):
    '''This reads an existing .csv file and returns a list of rows'''
    try:
        with open(file_name, 'r', newline='') as csvfile:
            file_data = []
            #reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            for row in csvfile:
                file_data.append(row) #need to append on the dictionary object
            return file_data
    except FileNotFoundError:
        return f'The file slated to be read: "{file_name}" does not exist'
