"""
Adds furniture rental records from individual customers to a central CSV file.
"""

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """Create invoice_file if not exists, else append new line."""
    with open(invoice_file, 'a+') as write_file:
        csv_writer = csv.writer(write_file)
        csv_writer.writerow([customer_name, item_code, item_description,
                             item_monthly_price])


def single_customer(customer_name, invoice_file):
    """Returns a function that takes one parameter, rental_items."""
    partial_add = partial(add_furniture, invoice_file, customer_name)

    def return_func(rental_items):
        with open(rental_items) as read_file:
            csv_reader = csv.reader(read_file)
            for line in csv_reader:
                partial_add(line[0], line[1], line[2])
    return return_func

22
if __name__ == "__main__":
    OUTPUT_FILE = "rented_items.csv"
    with open("data/customer_records.csv") as cust_records_file:
        CSV_READER = csv.reader(cust_records_file)
        for row in CSV_READER:
            customer = row[0]
            filename = "data/" + row[1]
            n_records = row[2]
            func = single_customer(customer, OUTPUT_FILE)
            func(filename)
