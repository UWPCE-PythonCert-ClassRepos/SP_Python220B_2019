#!/usr/bin/env python
"""
Lesson 08
"""
import csv
import os
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Create invoice_file.csv if it doesn’t exist or append a new line to it if it does.

    :invoice_file:          csv filename in string form. filename only, no path.
    :customer_name:         string
    :item_code:             string
    :item_description:      string
    :item_monthly_price:    float
    """
    file_path = os.getcwd() + '/' + invoice_file
    entry = [customer_name, item_code, item_description, '{:0.2f}'.format(item_monthly_price)]
    with open(file_path, 'a', encoding='utf-8-sig', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(entry)


def single_customer(customer_name, invoice_file):
    """
    Return a function that takes parameter rental_items.

    :customer_name:         string
    :invoice_file:          csv filename in string form. filename only, no path.
    """
    def add_to_invoice(rental_items):
        """
        Use add_furniture to iterate through rental_items and add each item to invoice_file.

        :rental_items:      csv filename in string form. filename only, no path.
        """
        streamlined_add = partial(add_furniture, invoice_file=invoice_file,
                                  customer_name=customer_name)
        read_file_path = os.getcwd() + '/' + rental_items
        with open(read_file_path, 'r', encoding='utf-8-sig') as read_file:
            csv_reader = csv.reader(read_file)
            for row in csv_reader:
                streamlined_add(item_code=row[0], item_description=row[1],
                                item_monthly_price=float(row[2]))
    return add_to_invoice
