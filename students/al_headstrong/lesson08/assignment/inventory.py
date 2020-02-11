import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    with open(invoice_file, 'a', newline='') as f:
        append_file = csv.writer(f)
        append_file.writerow([customer_name, item_code, item_description, item_monthly_price])


def single_customer(customer_name, invoice_file):
    def return_function(rental_items):
        func = partial(add_furniture,invoice_file, customer_name)
        with open(rental_items, 'r') as f:
            for row in csv.reader(f):
                func(*row)
    return return_function


