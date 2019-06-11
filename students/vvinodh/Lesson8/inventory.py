"""Inventory Module for Lesson08 Assignment"""
import csv
from functools import partial
#pylint: disable=E0602, W0613, C0103

def add_furniture(*args):
    """Adds furniture with given user inputs to invoice_file.csv"""
    if args:
        with open(args[0], "a+", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            row = args[1], args[2], args[3], args[4]
            csvwriter.writerow(row)

def start_data():
    """Adds initial data to invoice_file.csv"""
    add_furniture('invoice_file.csv', 'Vinodh', 'AB123', 'Walkman', 50.00)
    add_furniture('invoice_file.csv', 'Ram', 'BC345', 'Horse', 25.00)
    add_furniture('invoice_file.csv', 'Shiva', 'KY890', 'Book',
                  10.00)
    add_furniture()

def single_customer(customer_name, invoice_file):
    """Returns a new function (with a fixed customer name and destination
    inventory file) that will add all items in a source file to the overall
    inventory under a single customer name."""
    def inner(rental_items):
        with open(rental_items) as csvfile:
            csvreader = csv.reader(csvfile)
            add_item = partial(add_furniture, invoice_file, customer_name)
            for row in csvreader:
                add_item(row[0], row[1], row[2])
    return inner

if __name__ == "__main__":
    start_data()
    customer_one = single_customer('Jeff Beso', 'invoice_file.csv')
    customer_one('test_items.csv')
    