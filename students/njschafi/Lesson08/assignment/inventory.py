"""Inventory Module for Lesson08 Assignment"""
import csv
from functools import partial
#pylint: disable=E0602, W0613, C0103

def add_furniture(invoice_file='', customer_name='', item_code='',
                  item_description='', item_monthly_price=''):
    """Adds furniture with given user inputs to invoice_file.csv"""

    with open(invoice_file, "a+", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        row = customer_name, item_code, item_description, item_monthly_price
        csvwriter.writerow(row)

def start_data():
    """Adds initial data to invoice_file.csv"""
    add_furniture('invoice_file.csv', 'Post Malone', 'KJ809', 'Walkman', 50.00)
    add_furniture('invoice_file.csv', 'ABSIV', 'LL999', 'Horse', 25.00)
    add_furniture('invoice_file.csv', 'Rob Crow', 'MN1234', 'Post Malone Album',
                  10.00)

def single_customer(customer_name, invoice_file):
    """Returns a new function (with a fixed customer name and destination
    inventory file) that will add all items in a source file to the overall
    inventory under a single customer name."""
    def inner(rental_items):
        with open(rental_items) as csvfile:
            csvreader = csv.reader(csvfile)
            add_item = partial(add_furniture, invoice_file=invoice_file,
                               customer_name=customer_name)
            for row in csvreader:
                add_item(item_code=row[0], item_description=row[1],
                         item_monthly_price=row[2])
    return inner

if __name__ == "__main__":
    start_data()
    customer_one = single_customer('Post Malone', 'invoice_file.csv')
    customer_one('test_items.csv')
