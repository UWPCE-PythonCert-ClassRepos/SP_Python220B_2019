"""
Victor Medina
Assignment 8

"""

import os
import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    :param invoice_file:
    :param customer_name:
    :param item_code:
    :param item_description:
    :param item_monthly_price:
    :return:
    """

    invoice_dir_path = os.path.dirname(os.path.realpath(__file__))  + "\\" + invoice_file
    with open(invoice_dir_path, 'a') as invoices:
        csvwriter = csv.writer(invoices)
        row = customer_name, item_code, item_description, item_monthly_price
        csvwriter.writerow(row)


def single_customer(customer_name, invoice_file):
    """
    :param customer_name:
    :param invoice_file:
    :return:
    """
    def rentals(rental_items):
        """
        :param rental_items:
        :return:
        """
        rental_dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + rental_items
        with open(rental_dir_path) as invoices:
            invoice_csv_reader = csv.reader(invoices, delimiter=',', quotechar='"')
            items = partial(add_furniture, invoice_file=invoice_file,
                            customer_name=customer_name)
            for row in invoice_csv_reader:
                items(item_code=row[0], item_description=row[1], item_monthly_price=row[2])

    return rentals
