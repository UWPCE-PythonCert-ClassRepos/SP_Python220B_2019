import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """Function to add the customer rentals to a csv file"""
    with open(invoice_file, 'w+') as invoice:
        invoice_writer = csv.writer(invoice, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        customer = [customer_name, item_code, item_description, item_monthly_price]
        invoice_writer.writerow(customer)


def single_customer(customer_name, invoice_file):
    """Function returning a function which calls the parent with partial parameters"""

    def single_rentals(rental_items):
        with open(rental_items) as rentals:
            invoice_reader = csv.reader(rentals, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            add_single_items = partial(add_furniture, invoice_file, customer_name)
            for row in invoice_reader:
                add_single_items(row[0], row[1], row[2])

    return single_rentals


