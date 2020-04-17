"""
inventory.py
Assignment 8
Joli Umetsu
PY220
"""

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Updates invoice_file csv with rental data
    Returns: NA
    """
    with open(invoice_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([customer_name, item_code, item_description, item_monthly_price])



def single_customer(customer_name, invoice_file):
    """
    Adds each item in rentals_items_file csv to invoice_file all under customer_name
    Returns: Function with input parameter rental_items_file
    """
    def create_invoice(customer_name, invoice_file, rental_items_file):
        with open(rental_items_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for item in reader:
                add_furniture(invoice_file, customer_name, *item)

    return partial(create_invoice, customer_name, invoice_file)
