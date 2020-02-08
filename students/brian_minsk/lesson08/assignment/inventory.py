""" lesson08 code - Brian Minsk
"""

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """ Add a row with comma seperated values to a csv file. Create the file if it does not exist.

    Arguments:
    invoice_file - csv file with customer rentals
    customer_name - first and last name of a customer
    item_code - furniture item code
    item_description - furniture item description
    item_monthly_price - furniture item's rental price per month
    """
    with open(invoice_file, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([customer_name, item_code, item_description, item_monthly_price])


def single_customer(customer_name, invoice_file="rented_items.csv"):
    """ Return a function called add_rented_items that adds rented items from a csv file for a
    single customer to the invoice file.

    Arguments:
    invoice_file - csv file with customer rentals
    customer_name - first and last name of a customer

    Arguments in returned function:
    rental_items - csv file with rental product data
    """
    def add_rented_items(rental_items="test_items.csv"):
        with open(rental_items, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, quoting=csv.QUOTE_NONE)
            for line in csv_reader:
                add_furniture(invoice_file, customer_name, line[0], line[1], line[2])
    return add_rented_items


def single_customer_with_partial(customer_name, invoice_file="rented_items.csv"):
    """ Return a function called add_rented_items that adds rented items from a csv file for a
    single customer to the invoice file.

    Arguments:
    invoice_file - csv file with customer rentals
    customer_name - first and last name of a customer

    Arguments in returned function:
    rental_items - csv file with rental product data
    """
    add_furniture_for_customer = partial(add_furniture, invoice_file, customer_name)

    def add_rented_items(rental_items="test_items.csv"):
        with open(rental_items, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, quoting=csv.QUOTE_NONE)
            for line in csv_reader:
                add_furniture_for_customer(line[0], line[1], line[2])
    return add_rented_items


if __name__ == "__main__":
    # I have no idea why pylint is reporting too many positional arguments for the first three
    # lines of code below(the ones that call add_furniture).
    # pylint: disable=too-many-function-args
    # pylint: disable=invalid-name
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25.00)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10.00)
    add_furniture("rented_items.csv", "Alex Gonzales", "BK55", "Queen Mattress", 17.00)
    create_invoice = single_customer("Susan Wong", "rented_items.csv")
    create_invoice("test_items.csv")
    create_invoice = single_customer_with_partial("Wusan Song", "rented_items.csv")
    create_invoice("test_items.csv")
    