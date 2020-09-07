#!/usr/bin/env python3
"""
A module that uses closures and currying to create and update an inventory CSV
file with all the information that is currently entered through the spreadsheet
program. Also includes functionality to to bulk-process a list of items, coming
from a separate CSV file, that have been rented out to a single customer. This
functionality will thus update the inventory list by adding that customer’s
rentals.
"""

import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """
    Create invoice_file if it doesn't exist or append new line to add furniture
    """
    with open(invoice_file, mode='a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([customer_name,
                         item_code,
                         item_description,
                         item_monthly_price])

def single_customer(customer_name, invoice_file):
    """ Uses functools.partial and closures to returns a function """
    def customer_rental(rental_items):
        """
        Takes one parameter, rental_items, and will iterate through it adding
        each item to invoice_file
        """
        try:
            with open(rental_items, "r") as rental_csv:
                add_row = partial(add_furniture,
                                  invoice_file=invoice_file,
                                  customer_name=customer_name)
                for row in csv.reader(rental_csv):
                    add_row(item_code=row[0],
                            item_description=row[1],
                            item_monthly_price=row[2])
        except FileNotFoundError:
            print('The file was not found.')

    return customer_rental

if __name__ == "__main__":
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
    CREATE_INVOICE = single_customer("Susan Wong", "rented_items.csv")
    CREATE_INVOICE("test_items.csv")
