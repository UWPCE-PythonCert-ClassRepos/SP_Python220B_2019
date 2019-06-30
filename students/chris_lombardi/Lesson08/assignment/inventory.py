"""
Module utilizing functional techniques to create and update a *.csv that contains
data about which furniture is rented to whcih customer.
"""

import os
import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """
    Add data to a *.csv file for tracking rentals.

    Params:
    invoice_file = name of *.csv file containing rental log.
    customer_name = name of customer renting item
    item_code = unique code for the item being rented
    item_description = description of item rented
    item_monthly_price = price of item
    """

    # Check if file exists and set file writing mode.
    if os.path.isfile(invoice_file):
        edit_mode = 'a'
    else:
        edit_mode = 'w'

    with open(invoice_file, mode=edit_mode, newline='') as file:
        writer = csv.writer(file)
        writer.writerow([customer_name,
                         item_code,
                         item_description,
                         float(item_monthly_price)])


def single_customer(customer_name, invoice_file):
    """Return a function to iterate through rental items and add
    each item to a file.

    Params:
    customer_name = name of customer
    invoice_file = *.csv to add information to
    """
    def rental_items(source_file):
        try:
            with open(source_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                add_row = partial(add_furniture, customer_name=customer_name,
                                  invoice_file=invoice_file)
                for row in reader:
                    add_row(item_code=row[0],
                            item_description=row[1],
                            item_monthly_price=row[2])
        except FileNotFoundError:
            print('The file you are trying to add data from does not exist.')

    return rental_items

if __name__ == '__main__':
    add_furniture('rented_items.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25)
    add_furniture('rented_items.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10)
    add_furniture('rented_items.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17)
    CREATE_INVOICE = single_customer('Susan Wong', 'rented_items.csv')
    CREATE_INVOICE('test_items.csv')
