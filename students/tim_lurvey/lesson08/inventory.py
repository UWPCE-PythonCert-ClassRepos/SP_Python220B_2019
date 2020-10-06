#!/usr/env/bin python
""" Documentation for inventory.py
HP Norton has been using comma-separated files (.CSV extension) to keep track of which furniture
they have rented out to which customer. This is currently generated from a spreadsheet called
inventory.

Your Project Manager wants you to get the spreadsheet program out of the equation by creating a
Python function that will create and update an inventory CSV file with all the information that is
currently entered through the spreadsheet program. You have decided to use closures and currying to
develop the necessary functionality.

You will also develop functionality to to bulk-process a list of items, coming from a separate CSV
file, that have been rented out to a single customer. This functionality will thus update the
inventory list by adding that customer’s rentals.

To summarize: 1. You will create a program to initially create, and subsequently update, a CSV file
that lists which furniture is rented to which customer (to replace use of the spreadsheet mentioned
above). 2. You will create additionally functionality that will load individual customers rentals.
"""

from csv import reader


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """This function will create {invoice_file} (to replace the spreadsheet’s data)
    if it does not exist or append a new line to it if it does. After adding a few
    items to the same file, the file created by add_furniture should look something
    like this:
        Elisa Miles,LR04,Leather Sofa,25.00
        Edward Data,KT78,Kitchen Table,10.00
        Alex Gonzales,BR02,Queen Mattress,17.00
    You can create a starter file in this format for testing, or you can have your
    add function do it.

    :rtype: None
    :type invoice_file: str
    :type customer_name: str
    :type item_code: str
    :type item_description: str
    :type item_monthly_price: float
    """
    string = ",".join((customer_name,
                       item_code,
                       item_description,
                       f"{float(item_monthly_price):.2f}"))
    open(invoice_file, 'a').write(string + "\n")


def get_csv_lines(items_file: str) -> list:
    """line generator for file"""
    lines = reader(open(items_file, 'r'))
    for line in lines:
        yield line


def single_customer(customer_name, invoice_file):
    """single_customer needs to use functools.partial and closures, in order to return a function
    that will iterate through rental_items and add each item to invoice_file.
    :rtype: function that takes one parameter, rental_items
    :type customer_name: str
    :type invoice_file: str
    """
    def write_items(rental_items):
        for line in get_csv_lines(rental_items):
            add_furniture(invoice_file, customer_name, *line)
    return write_items


if __name__ == "__main__":
    create_invoice = single_customer("Susan Wong", "rented_items.csv")
    create_invoice("test_items.csv")
