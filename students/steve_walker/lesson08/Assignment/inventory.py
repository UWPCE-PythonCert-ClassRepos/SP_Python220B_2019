"""HP Norton furniture rental and invoice management tool."""

# pylint: disable=C0103

import os
import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """Add furniture rental to csv."""

    with open(invoice_file, 'a' if os.path.isfile(invoice_file) else 'w',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerow((customer_name, item_code, item_description,
                         item_monthly_price))


def single_customer(invoice_file, customer_name):
    """Return function that gives invoice data for a single customer."""

    def invoice_data(rental_items):
        customer_rentals = partial(add_furniture, invoice_file=invoice_file,
                                   customer_name=customer_name)

        with open(rental_items, 'r', newline='') as file:
            for row in csv.reader(file):
                customer_rentals(item_code=row[0],
                                 item_description=row[1],
                                 item_monthly_price=row[2])

    return invoice_data

if __name__ == "__main__":
    add_furniture('rented_items.csv', 'John Muir', '001', 'Polished stump', 3)
    rhianna_invoice = single_customer('rented_items.csv', 'Rhianna')
    rhianna_invoice('test_items.csv')
