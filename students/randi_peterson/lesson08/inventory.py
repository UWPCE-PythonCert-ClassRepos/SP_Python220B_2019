"""This file replaces the existing spreadsheet for Lesson 08"""

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """This function creates a new invoice file"""
    with open(invoice_file, mode='a', newline='') as wkg_file:
        writer = csv.writer(wkg_file, delimiter=',', quotechar='"')
        new_list = [customer_name, item_code, item_description, item_monthly_price]
        writer.writerow(new_list)


def single_customer(customer_name, invoice_file):
    """This function returns a function to iterate through rental_items and add each
    item to invoice_file"""
    def rental_function(rental_items):
        with open(rental_items) as file:
            new_item = partial(add_furniture, invoice_file, customer_name)
            reader = csv.reader(file)
            for row in reader:
                identifier = row[0]
                item = row[1]
                price = row[2]
                new_item(identifier, item, price)

    return rental_function


if __name__ == "__main__":
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
    CREATE_INVOICE = single_customer("Susan Wong", "rented_items.csv")
    CREATE_INVOICE("test_items.csv")
