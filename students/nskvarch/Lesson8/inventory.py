#!usr/bin/env python3
"""Lesson 8 assignment "Closures and Currying"
Module creates or appends to a specified csv file with
the data given as parameters to add_furniture.
single_customer function returns a function that takes
a csv file as input and writes to the first specified csv file
a list of items that are then associated with one customer"""


import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """Creates or appends to a .csv file creating lines with data given"""
    add_line = [customer_name, item_code, item_description, item_monthly_price]
    with open(invoice_file, "a+", newline="") as file:
        file_write = csv.writer(file)
        file_write.writerow(add_line)


def single_customer(customer_name, invoice_file):
    """Returns a function that when given a csv file as input will write to
    the first csv file the list of items associated with the provided customer name"""
    def single_customer_rentals(rental_items):
        add_item = partial(add_furniture, customer_name=customer_name,
                           invoice_file=invoice_file)
        with open(rental_items, "r") as file:
            for row in csv.reader(file):
                add_item(item_code=row[0], item_description=row[1],
                         item_monthly_price=row[2])
    return single_customer_rentals


if __name__ == "__main__":
    add_furniture("invoice_file.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("invoice_file.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("invoice_file.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
    CREATE_INVOICE = single_customer("Susan Wong", "invoice_file.csv")
    CREATE_INVOICE("test_items.csv")
