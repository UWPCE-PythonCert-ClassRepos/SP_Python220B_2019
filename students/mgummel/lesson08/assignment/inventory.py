"""Module inventory.py"""
#!/usr/bin/python3
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Writes a file that contains customer name and all item information
    on one line for a more efficient look up.

    :param invoice_file: file to write customer rental items
    :param customer_name: customer
    :param item_code: item code of the rental
    :param item_description: description of the rental item
    :param item_monthly_price: monthly cost of rental item
    :return: None
    """
    with open(invoice_file, mode='a+') as invoice:
        invoice.write(f"{customer_name},{item_code}," \
                      f"{item_description},{item_monthly_price}\n")


def single_customer(customer_name, invoice_file):
    """
    A curried function for a single customer that
    takes a file with rental items and writes information
    to an invoice file that is associated with all customer
    rentals.

    When running the function a file will be specified to
    stream all customer rental items

    :param customer_name: customer
    :param invoice_file: file to write customer rental items
    :return: Closure function rental_items
    """

    def rental_items(input_file):
        """
        :param input_file: file to grab rental items from
        :return: None
        """
        add = partial(add_furniture, invoice_file, customer_name)

        with open(input_file, mode='r+') as items:
            for line_item in items:
                param_list = line_item.rstrip().split(',')
                add(*param_list)
    return rental_items
