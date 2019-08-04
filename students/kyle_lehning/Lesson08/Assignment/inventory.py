#!/usr/bin/env python3
"""Module for adding rentals"""
import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """Write to invoice_file all other parameters. If invoice_file exists append, else new"""
    with open(invoice_file, "a+") as passed_csv:
        csv_writer = csv.writer(passed_csv, delimiter=',', lineterminator='\n')
        csv_writer.writerow([customer_name, item_code, item_description, item_monthly_price])


def single_customer(customer_name, invoice_file):
    """Create function to curry customer_name and invoice_file for add_furniture"""
    def customer_rental(rental_items):
        """
        Loop through rental_items file and append each row to curried invoice_file with same
        customer_name
        """
        customer = partial(add_furniture, invoice_file=invoice_file, customer_name=customer_name)
        with open(rental_items, "r") as rental_csv:
            for row in csv.reader(rental_csv):
                customer(item_code=row[0], item_description=row[1], item_monthly_price=row[2])
    return customer_rental


if __name__ == '__main__':
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
    create_invoice = single_customer("Susan Wong", "Susan_Invoice.csv")  # pylint: disable=C0103
    create_invoice("test_items.csv")
