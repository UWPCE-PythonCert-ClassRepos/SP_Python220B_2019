"""Module for inventory"""

import csv
import logging
from functools import partial

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """Create an invoice_file"""
    LOGGER.info("Opening invoice file")
    with open(invoice_file, "a+", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([customer_name,
                         item_code,
                         item_description,
                         item_monthly_price])
        LOGGER.info("Added row")


def single_customer(customer_name, invoice_file):
    """Iterate through rental_items and add each item to invoice_file"""
    def rental_items(rental_file):
        """Rental items information"""
        add_row = partial(add_furniture, invoice_file, customer_name)
        try:
            # partial makes a new version with arguments filled in
            with open(rental_file, mode="r", newline="",
                      encoding="utf-8-sig") as file:
                reader = csv.reader(file)
                LOGGER.info("Read file")
                for row in reader:
                    add_row(item_code=row[0],
                            item_description=row[1],
                            item_monthly_price=row[2])
                LOGGER.info("Added rent info")
        except FileNotFoundError:
            LOGGER.info("File was not found!")
    return rental_items


if __name__ == "__main__":
    add_furniture("rented_items.csv", "Elisa Miles", "LR04",
                  "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78",
                  "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02",
                  "Queen Mattress", 17)
    CREATE_INVOICE = single_customer("Susan Wong", "rented_items.csv")
    CREATE_INVOICE("test_items.csv")
