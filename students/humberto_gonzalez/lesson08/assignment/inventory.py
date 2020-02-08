# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:08:06 2020

@author: Humberto
"""

# pylint: disable=logging-format-interpolation

import logging
import csv
from functools import partial

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

LOG_FILE = 'db.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(FILE_HANDLER)

def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """creates a new file or appends info to an existing one"""

    with open(invoice_file, "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([customer_name,
                         item_code,
                         item_description,
                         item_monthly_price])


def single_customer(invoice_file, customer_name):
    """Returns a function that adds all items to a file"""

    def add_items(rental_items):
        """Adds all items to a file"""
        add_row = partial(add_furniture, invoice_file=invoice_file,
                          customer_name=customer_name)
        try:
            with open(rental_items, mode="r", newline="") as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    add_row(item_code=row[0],
                            item_description=row[1],
                            item_monthly_price=row[2])
                    LOGGER.info(f"Item {row[0]} added to file")
        except IOError:
            LOGGER.info(f"File with name {rental_items} does not exist")
    return add_items
