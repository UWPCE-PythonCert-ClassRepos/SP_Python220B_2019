# Stella Kim
# Assignment 8: Functional Techniques

"""
Create program to create and update a CSV file.  Additionally, create
functionality to load individual customers rentals.
"""

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """Create and update a CSV file that lists furniture rented to customers"""
    filename = f'{invoice_file}.csv'
    with open(filename, 'a', newline='') as file:
        data_file = csv.writer(file, quoting=csv.QUOTE_NONE)
        row = (customer_name,
               item_code,
               item_description,
               item_monthly_price)
        data_file.writerow(row)


def single_customer(customer_name, invoice_file):
    """Load customer rentals"""
    rentals = partial(add_furniture, invoice_file, customer_name)

    def customer_rentals(rental_items):
        filename = f'{rental_items}.csv'
        with open(filename, 'r', newline='') as file:
            data_file = csv.reader(file, delimiter=',')
            for row in data_file:
                rentals(*row)
    return customer_rentals


if __name__ == "__main__":
    CREATE_INVOICE = single_customer('John Smith', 'rented_items')
    CREATE_INVOICE('test_items')
