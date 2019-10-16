"""
This module contains the functionality to populate the inventory csv file.
"""

import csv
import os
import sys
from functools import partial

def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """write data to a csv file.
    :parm invoice_file: file to be written.
    :parm customer_name:
    :parm item_code:
    :parm item_description:
    :parm item_monthly_price:
    """
    with open(invoice_file, 'a+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        csv_writer.writerow([customer_name, item_code, item_description,
                             item_monthly_price])


def single_customer(customer_name, invoice_file):
    """
    Implement closure to return a function that will write to the invoice_file.
    :parm customer_name:
    :parm invoice_file:
    :return function:
    """
    def read_data(filename):
        add_item = partial(add_furniture, invoice_file, customer_name)
        if not os.path.exists(filename):
            print(f"{filename} doesn't exist")
            sys.exit(1)
        with open(filename, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for row in csv_reader:
                item_code = row[0]
                item_description = row[1]
                item_monthly_price = row[2]
                add_item(item_code, item_description, item_monthly_price)
    return read_data


if __name__ == "__main__":

    add_furniture('rentals.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25)
    add_furniture('rentals.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10)
    add_furniture('rentals.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17)
    CREATE_INVOICE = single_customer('John Smith', 'rentals.csv')
    CREATE_INVOICE('items.csv')
