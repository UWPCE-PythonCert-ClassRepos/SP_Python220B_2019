import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """add new entry to invoice_file"""
    with open(invoice_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        entry = [customer_name, item_code, item_description, item_monthly_price]
        writer.writerow(entry)

def single_customer(customer_name, invoice_file):
    """Using closure and currying, """
    add_rental_item = partial(add_furniture, invoice_file, customer_name)
    def read_customer_invoice(rental_items):
        with open(rental_items, newline='') as rentfile:
            reader = csv.reader(rentfile, delimiter=',')
            for row in reader:
                item_code = row[0]
                item_description = row[1]
                item_price = row[2]
                add_rental_item(item_code, item_description, item_price)
    return read_customer_invoice
