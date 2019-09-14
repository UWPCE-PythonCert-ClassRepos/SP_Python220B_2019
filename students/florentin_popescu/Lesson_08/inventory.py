# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:18:22 2019
@author: Florentin Popescu
"""

# imports
import os
import csv
import logging
import time
from functools import partial
import psutil
from memory_profiler import memory_usage

# ==================================

# set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("inventory.py")
LOGGER.info("loger active")
# ===============================

MEM_USAGE = memory_usage(proc=-1, interval=.1, timeout=None)
# ===============================


def add_furniture(invoice_file, customer_name,
                  item_code, item_description, item_monthly_price):
    """
        add data to invoice file
    """
    with open(invoice_file, mode="a" if os.path.isfile(invoice_file) else "w",
              newline="") as file:
        writer = csv.writer(file)
        writer.writerow((customer_name, item_code, item_description,
                         round(float(item_monthly_price), 2)))
# ===============================


def single_customer(invoice_file, customer_name):
    """
        return a function iterating through rentals
        and adding them to invoice file
    """
    def rental_items(src_file):
        add_row = partial(add_furniture,
                          invoice_file=invoice_file,
                          customer_name=customer_name)
        try:
            with open(src_file, mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    add_row(item_code=row[0],
                            item_description=row[1],
                            item_monthly_price=row[2])

        except FileNotFoundError as err:
            LOGGER.info("file not found: %s", err)

    return rental_items
# ===============================


if __name__ == "__main__":
    START = time.perf_counter()
    add_furniture("rented_items.csv", "Elisa Miles", "LR04",
                  "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78",
                  "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzalez", "BR02",
                  "Queen Mattress", 17)
    INVOICE = single_customer("rented_items.csv", "Susan Wong")
    INVOICE("testdata/test_items.csv")
    LOGGER.info("script runtime: %s", time.perf_counter() - START)
    LOGGER.info("script cpu usage: %s%%", psutil.cpu_percent())
    LOGGER.info("script memory usage  = %s", MEM_USAGE)

# example run
# INFO:__main__:inventory.py
# INFO:__main__:loger active
# INFO:__main__:script runtime: 0.03658650000215857
# INFO:__main__:script cpu usage: 18.7%
# INFO:__main__:script memory usage  = [104.30859375]
