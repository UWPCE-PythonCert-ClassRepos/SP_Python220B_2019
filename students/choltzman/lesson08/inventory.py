# pylint: disable=invalid-name
"""Create invoice CSV file"""
import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """Create or append to invoice file"""
    with open(invoice_file, 'a+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([customer_name,
                         item_code,
                         item_description,
                         item_monthly_price])


def single_customer(customer_name, invoice_file):
    """Build a function to create or append to a file"""
    def add_rentals(rental_items):
        add_row = partial(add_furniture, invoice_file, customer_name)
        with open(rental_items, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                add_row(*row)

    return add_rentals


if __name__ == "__main__":
    newfunc = single_customer("Testy Test", "outfile.csv")
    newfunc("data/test_items.csv")
