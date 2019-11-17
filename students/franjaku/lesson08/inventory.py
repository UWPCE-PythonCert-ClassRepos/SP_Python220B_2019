"""
    Lesson 08 main module.

"""

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Add the furniture items rented to customers to the invoice_file .csv in the following format
        customer_name,item_code,item_description,item_monthly_price
    Will create invoice_file if it doesn't exist or append a new line to it if it does.

    :param invoice_file: .csv file
    :param customer_name: string
    :param item_code: string
    :param item_description: string
    :param item_monthly_price: int
    :return: None
    """
    pass


def single_customer(customer_name, invoice_file):
    """
    Return a function that takes rental items and adds them to the invoice_file. Return function
    will leverage the add_furniture() func using functools.partial
    :param customer_name: string
    :param invoice_file: string
    :return: f(rental_items)
    """
    pass