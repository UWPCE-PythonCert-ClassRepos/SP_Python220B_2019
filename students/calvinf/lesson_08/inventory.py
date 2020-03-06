"""Module for Lesson 8 Currying and closure"""
import csv
import os
import logging
from functools import partial

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.INFO)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(CONSOLE_HANDLER)


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    This function will create invoice_file (to replace the spreadsheet’s data)
    if it doesn’t exist or append a new line to it if it does.
    After adding a few items to the same file.
    """

    filenamepath = os.path.join(os.getcwd(), invoice_file)
    LOGGER.info("File path for csv file: %s", filenamepath)
    with open(filenamepath, 'a+', newline='') as csv_writer:
        writer = csv.writer(csv_writer)
        writer.writerow([customer_name, item_code,
                         item_description, item_monthly_price])


def single_customer(cust_name, inv_file):
    """
    Input parameters: customer_name, invoice_file.
    Output: Returns a function that takes one parameter, rental_items.
    single_customer needs to use functools.partial and closures, in order
    to return a function that will iterate through rental_items
    and add each item to invoice_file.
    """
    def single_customer_update(rental_items):
        filenamepath = os.path.join(os.getcwd(), rental_items)
        single_customer_add_furniture = partial(add_furniture, inv_file, cust_name)
        with open(filenamepath) as read_file:
            reader = csv.reader(read_file, delimiter=',')
            for row in reader:
                LOGGER.info(row)
                single_customer_add_furniture(*row)
    return single_customer_update


def main():
    """Main function for testing functions"""
    add_furniture('rented_items.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25.00)
    add_furniture('rented_items.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10.00)
    add_furniture('rented_items.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    create_invoice = single_customer("Susan Wong", "rented_items.csv")
    create_invoice("test_items.csv")


if __name__ == "__main__":
    main()
