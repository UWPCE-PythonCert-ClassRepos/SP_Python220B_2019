"""module with functions for filling out an inventory csv file"""
import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """adds an entry to invoice file"""
    with open(invoice_file, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        entry = [customer_name, item_code, item_description, item_monthly_price]
        csvwriter.writerow(entry)

def single_customer(customer_name, invoice_file):
    """returns a function that goes through a file of items and adds them to invoice_file"""
    add_item = partial(add_furniture, invoice_file, customer_name)
    def read_file(rental_items):
        with open(rental_items, newline='') as rentfile:
            csvreader = csv.reader(rentfile, delimiter=',')
            for row in csvreader:
                code = row[0]
                description = row[1]
                price = row[2]
                add_item(code, description, price)
    return read_file
