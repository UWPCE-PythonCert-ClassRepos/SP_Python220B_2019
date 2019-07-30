"""
Replace the existing spreadsheet
"""

import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """
    Create invoice_file (to replace the spreadsheet’s data) if it doesn’t
    exist or append a new line to it if it does
    """
    add_list = [customer_name, item_code, item_description,
                item_monthly_price]

    with open(invoice_file, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(add_list)


def single_customer(customer_name, invoice_file):
    """
    Return a function that will iterate through rental_items and add each
    item to invoice_file
    """
    def add_items(rental_items):
        item = partial(add_furniture, invoice_file=invoice_file,
                       customer_name=customer_name)
        with open(rental_items, 'r') as csv_file:
            for row in csv.reader(csv_file):
                item(item_code=row[0],
                     item_description=row[1],
                     item_monthly_price=row[2])
    return add_items

if __name__ == "__main__":
    CREATE_INVOICE = single_customer("Susan Wong", "rented_items.csv")
    CREATE_INVOICE("test_items.csv")
