'''Module to track inventory against rentals'''
# Advanced Programming in Python -- Lesson 8 Assignment 1
# Jason Virtue
# Start Date 2/27/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name,too-few-public-methods,wrong-import-order,singleton-comparison,too-many-arguments,logging-format-interpolation,too-many-locals,no-else-return,unused-variable

import csv
import logging
from functools import partial

# Set up log file
logging.basicConfig(filename="db.log", format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M %p', level=logging.INFO)


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    '''Module adds furniture rentals to invoice file or creates a new one'''
    with open(invoice_file, 'a+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        csv_item = [customer_name, item_code, item_description, item_monthly_price]
        csv_writer.writerow(csv_item)
        logging.info(f'Adds furniture item {item_code} for {customer_name} to invoice file')

def single_customer(customer_name, invoice_file):
    '''Module to add rental for single customer to invoice file'''
    def rentals(rental_items):
        '''Module to read rentals file and input single customer from closure function'''
        with open(rental_items, 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            logging.info('Reads Invoice File into memory')
            add_rentals = partial(add_furniture, invoice_file, customer_name)
            for row in csv_reader:
                add_rentals(item_code=row[0], item_description=row[1], item_monthly_price=row[2])
    return rentals

if __name__ == '__main__':
    add_furniture("invoice_file.csv", "Elisa Miles", "LR04", "Leather Sofa", 25.00)
    add_furniture("invoice_file.csv", "Edward Data", "KT78", "Kitchen Table", 10.00)
    add_furniture("invoice_file.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17.00)

    #create_invoice is a function when called will enter for a single customers for all
    #the rentals from the rental_items.csv file.
    CREATE_INVOICE = single_customer("JJ Berra", "invoice_file.csv")
    CREATE_INVOICE("rental_items.csv")
