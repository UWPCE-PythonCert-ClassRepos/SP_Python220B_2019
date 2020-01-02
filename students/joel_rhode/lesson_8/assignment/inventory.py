"""Provides functions for adding customer furniture rentals to invoice file csv."""

from csv import writer
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """Add furniture rental to invoice_file csv"""
    with open(invoice_file, mode='a', newline='') as write_file:
        writer(write_file).writerow((customer_name, item_code, item_description,
                                     item_monthly_price))


def single_customer(customer_name, invoice_file):
    """
    Generates function that takes argurment rental_items (iterator) and
    adds them to under customer_name in invoice_file csv.
    """
    def add_rental_items(invoice_file, customer_name, rental_items):
        """Adds rental items to invoice file csv"""
        for item in rental_items:
            add_furniture(invoice_file, customer_name, *item)

    return partial(add_rental_items, invoice_file, customer_name)
