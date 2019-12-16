""" Import customer rental information to an invoice file """

import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """ Add furniture rentals to invoice file """

    with open(invoice_file, "a") as csv_file:
        inventory_writer = csv.writer(csv_file)
        inventory_writer.writerow([customer_name, item_code, item_description, item_monthly_price])

def single_customer(customer_name, invoice_file):
    """ Import multiple items for a single customer from CSV file """

    def import_items(rental_items):
        single_entry = partial(add_furniture, invoice_file, customer_name)
        with open(rental_items, "r") as rental_file:
            rental_reader = csv.reader(rental_file)
            for row in rental_reader:
                item_code = row[0]
                item_description = row[1]
                item_monthly_price = row[2]
                single_entry(item_code, item_description, item_monthly_price)
    return import_items
