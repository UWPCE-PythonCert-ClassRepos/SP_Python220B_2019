"""Python 220 - Assignment 08"""

import csv
from functools import partial

import logging

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """This function will create invoice_file (to replace the spreadsheet’s data) if it doesn’t
    exist or append a new line to it if it does."""
    with open("./" + invoice_file, 'a', newline='') as csvfile:
        mywriter = csv.writer(csvfile, delimiter=',')
        mywriter.writerow([customer_name, item_code, item_description, item_monthly_price])


def single_customer(customer_name, invoice_file):
    """The idea is for the single_customer() function to return a new function (with a fixed
    customer name and destination inventory file) that will add all items in a source file to
    the overall inventory under a single customer name. Internally, single_customer() should
    leverage add_furniture() by fixing the first two parameters."""
    def rentals(rental_items):
        try:
            with open("./" + rental_items, newline='') as csvfile:
                myreader = csv.reader(csvfile, delimiter=',')
                add_items = partial(add_furniture, invoice_file, customer_name)
                for row in myreader:
                    add_items(row[0], row[1], row[2])
        except FileNotFoundError:
            logging.error("%s; file not found", rental_items)
    return rentals

if __name__ == '__main__':
    #add_furniture can be tested manually, as shown below.
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25.00)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10.00)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17.00)

    #So, using create_invoice() will, in this case, add all items in test_items.csv to
    #rented_items.csv under the name “Susan Wong”.
    CREATE_INVOICE = single_customer("Susan Wong", "rented_items.csv")
    CREATE_INVOICE("test_items.csv")
