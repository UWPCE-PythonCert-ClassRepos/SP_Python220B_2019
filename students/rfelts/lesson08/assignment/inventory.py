#!/usr/bin/env python3

# Russell Felts
# Assignment 8

""" Create CSV file for rental data """


import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Create invoice_file if it doesn’t exist or append a new line to it if it does.
    :param invoice_file: String containing the file path
    :param customer_name: String containing the customer name
    :param item_code: String containing the item code
    :param item_description: String containing the item description
    :param item_monthly_price: String containing the item monthly price
    """
    try:
        with open(invoice_file, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([customer_name, item_code, item_description, item_monthly_price])
    except IOError:
        print("File IO Error")


def single_customer(customer_name, invoice_file):
    """
    Use functools.partial and closures, in order to return a function that will iterate
    through rental_items and add each item to invoice_file.
    :param customer_name: String containing the customer name
    :param invoice_file: String containing the file path
    :return function that takes one parameter, rental_items
    """
    def process_rental_data(rental_items):
        add_rental_data = partial(add_furniture, invoice_file, customer_name)
        try:
            with open(rental_items, 'r') as rental_file:
                reader = csv.reader(rental_file)
                for row in reader:
                    add_rental_data(row[0], row[1], row[2])
        except IOError:
            print("File IO Error")

    return process_rental_data
