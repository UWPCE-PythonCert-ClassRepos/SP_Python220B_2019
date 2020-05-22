""" Inventory CSV Generator """
import os
import csv
from pathlib import Path
from functools import partial

INVOICE_DIRECTORY = Path("./invoices")


def add_furniture(invoice, customer_name, item_code, item_description, monthly_price):
    """
    Function to create and add data to and invoice file.

    Args:
        invoice_file: File name of invoice
        customer_name: Name of custer being invoiced
        item_code: Product ID
        item_description: Description of product
        item_monthly_price: Rental price per month (USD)
    """
    furniture_list = [customer_name, item_code, item_description, monthly_price]
    if not os.path.isdir(INVOICE_DIRECTORY):
        os.mkdir(INVOICE_DIRECTORY)

    with open(INVOICE_DIRECTORY / invoice, "a+", newline="") as csv_f:
        csv_write = csv.writer(csv_f)
        csv_write.writerow(furniture_list)


def single_customer(customer_name, invoice_file):
    """
    Returns a function that will iterate through rental_items and add
    each item to the invoice_file.  Uses functools.partials and closures

    Args:
        customer_name: Name of the customer
        invoice_file: Invoice filename
    Returns
        func: function which take input argument rental item and adds it to
        the invoice file
    """
    writer_file = partial(add_furniture, invoice_file, customer_name)

    def generate_invoice(file_name):
        with open(INVOICE_DIRECTORY / file_name, "r") as csv_f:
            csv_read = csv.reader(csv_f)
            for line in csv_read:
                writer_file(line[0], line[1], line[2])

    return generate_invoice


if __name__ == "__main__":
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
    CREATE_INVOICE = single_customer("Susan Wong", "rented_items.csv")
    CREATE_INVOICE("test_items.csv")
