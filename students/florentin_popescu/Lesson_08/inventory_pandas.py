# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:02:03 2019
@author: Florentin Popescu
"""

# imports
import os
import logging
import time
from functools import partial
import psutil
import pandas as pd
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
    col_names = "customer_name", "item_code", "item_description", "price"

    if os.path.isfile(invoice_file):
        try:
            dfr = pd.read_csv(invoice_file, sep=",",
                              header=None, names=col_names)
            dfr = dfr.append({"customer_name": customer_name,
                              "item_code": item_code,
                              "item_description": item_description,
                              "price": round(float(item_monthly_price), 2)},
                             ignore_index=True)
        except PermissionError as err:
            LOGGER.info("file is open: %s", err)
        with open(invoice_file, mode="w", newline="") as file:
            dfr.to_csv(file, index=False, header=False)
    else:
        dfr = pd.DataFrame(columns=col_names)
        dfr = dfr.append({"customer_name": customer_name,
                          "item_code": item_code,
                          "item_description": item_description,
                          "price": round(float(item_monthly_price), 2)},
                         ignore_index=True)
        dfr.to_csv(invoice_file, index=False,
                   header=False, line_terminator="\n")
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
            cols = "item_code", "item_description", "price"
            with open(src_file, mode="r", newline="") as file:
                dfr = pd.read_csv(file, sep=",",
                                  header=None,
                                  names=cols)
                for row in dfr.itertuples():
                    add_row(item_code=row.item_code,
                            item_description=row.item_description,
                            item_monthly_price=row.price)

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
# INFO:__main__:script runtime: 0.07230200000049081
# INFO:__main__:script cpu usage: 16.8%
# INFO:__main__:script memory usage  = [104.53125]

# while cpu and memory usages are comparable, the pandas-based
# "inventory_pandas.py" is about two times slower than the "inventory.py"
