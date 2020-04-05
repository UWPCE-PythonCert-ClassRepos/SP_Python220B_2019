#!/usr/bin/env python3

""" Updates inventory """

# pylint: disable= C0103

import csv
import os
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """ Add furniture data """

    if os.path.exists(invoice_file):
        with open(invoice_file, "a", newline='') as csv_file:
            furniture = csv.writer(csv_file)
            furniture.writerow([customer_name, item_code, item_description, item_monthly_price])
    else:
        with open(invoice_file, "w", newline='') as csv_file:
            furniture = csv.writer(csv_file)
            furniture.writerow([customer_name, item_code, item_description, item_monthly_price])


def single_customer(customer_name, invoice_file):
    """ Imports multiple items for single customer"""

    def get_items(rental_items):
        add_item = partial(add_furniture, invoice_file, customer_name)
        with open(rental_items, "r") as rental_file:
            rental_reader = csv.reader(rental_file)
            for row in rental_reader:
                item_code = row[0]
                item_description = row[1]
                item_monthly_price = row[2]
                add_item(item_code, item_description, item_monthly_price)
    return get_items


# testing
add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)

create_invoice = single_customer("Susan Wong", "rented_items.csv")
create_invoice("test_items.csv")
