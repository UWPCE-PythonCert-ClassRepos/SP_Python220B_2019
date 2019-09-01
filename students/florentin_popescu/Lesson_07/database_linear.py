# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 08:59:40 2019
Modified on Thu Aug 22 17:17:22 2019
@author: Florentin Popescu
"""

# imports
import csv
import logging
import time as tm
import psutil

from pymongo import MongoClient
from memory_profiler import memory_usage
# ==================================

# set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("database_linear.py")
LOGGER.info("loger active")
# ==================================

MEM_USAGE = memory_usage(proc=-1, interval=.1, timeout=None)
# ==================================


class Timer():
    """
        times execcution
    """
    def __init__(self):
        """ init """
        self.start = tm.perf_counter()

    def __repr__(self):
        """ repper """
        return f"timer started at: {self.start}"

    def get_time_hh_mm_ss_mss(self):
        """ display passed time """
        end = tm.perf_counter()
        milisec = ((end - self.start) % 1) * 1000
        mnt, sec = divmod(end - self.start, 60)
        hrs, mnt = divmod(mnt, 60)
        time_str = "h:m:s:ms>> %02d:%02d:%02d:%3d" % (hrs, mnt, sec, milisec)
        return time_str
# ==================================


class MongoDBConnection():
    """
        establish MongoDB connection
    """
    def __init__(self, host='127.0.0.1', port=27017):
        """ use public ip-address and port """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """ enter """
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ exit """
        self.connection.close()
# ==================================


def csv_to_mongo_linear(path, db_name):
    """
        import records one-by-one from file to mongodb
    """
    try:
        timer = Timer()
        # -----------------------------------------

        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.FlorentinDB
            dbs = database[db_name]
            prior_count = dbs.estimated_document_count()

            with open(path, "r") as csvfile:
                csv_dct = csv.DictReader(csvfile, delimiter=",")
                csv_lst = list(csv_dct)
                insert_count = len(csv_lst)

                dbs.insert_many(csv_lst)

                # insert_count = 0
                # for record in csv_dct:
                #    row = dict(map(list, zip(list(record.keys()),
                #                             list(record.values()))))
                #    dbs.insert_one(row)
                #    insert_count += 1

            after_count = dbs.estimated_document_count()
            insert_time = timer.get_time_hh_mm_ss_mss()
        # -----------------------------------------

        return insert_count, prior_count, after_count, insert_time

    except (FileNotFoundError, UnboundLocalError) as err:
        LOGGER.info("path-indicated file not found")
        LOGGER.info(err)
# ==================================


def main_linear(repo, colection):
    """
        main function
    """
    timer = Timer()
    # -----------------------

    tpl0 = csv_to_mongo_linear(repo[0], colection[0])
    LOGGER.info("inserted file:%s", repo[0])
    tpl1 = csv_to_mongo_linear(repo[1], colection[1])
    LOGGER.info("inserted file:%s", repo[1])
    # -----------------------
    LOGGER.info("<L> script cpu usage: %s%%", psutil.cpu_percent())
    LOGGER.info("<L> script memory usage  = %s", MEM_USAGE)
    LOGGER.info("<L> script total runtime: %s", timer.get_time_hh_mm_ss_mss())

    drop_data()

    return (tuple(item for item in tpl0),
            tuple(item for item in tpl1))
# ==================================


def drop_data():
    """
        drop data from MongoDB
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.FlorentinDB

    dbs = ["customer", "product", "rental"]
    for name in dbs:
        database[name].drop()

    return "data has been dropped from Mongo database"
# ==================================


def show_available_products():
    """
        list available products
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.FlorentinDB

    products = database["product"].find({"quantity_available": {"$ne": "0"}})
    products_dict = {prod["product_id"]:
                     {"description": prod["description"],
                      "product_type": prod["product_type"],
                      "quantity_available": int(prod["quantity_available"])}
                     for prod in products}

    return products_dict
# ==================================


def show_rentals(product_id):
    """
        list customers that rented products
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.FlorentinDB

    rentals = database["rental"].find({"product_id": product_id})\
        .sort("customer_id")
    rental_list = [rental["customer_id"] for rental in rentals]
    customers = database["customer"].find({"customer_id":
                                           {"$in": rental_list}})
    cust_dict = {cust["customer_id"]:
                 {"name": f"{cust['first_name']} {cust['last_name']}",
                  "address": cust["address"],
                  "phone": cust["phone"],
                  "email": cust["email"]}
                 for cust in customers}

    return cust_dict
# ==================================


def print_products():
    """
        print products
    """
    products = show_available_products()
    for prod in products:
        print(prod, products[prod])
# ==================================


# if __name__ == "__main__":
#    PATH = "csvdata/customers.csv", "csvdata/products.csv"
#    COLECTION = "customer", "product"
#    RESULTS = main_linear(PATH, COLECTION)
#    LOGGER.info(RESULTS)
# ==================================

# Example run - insert via 'insert_many()' method:
# INFO:__main__:database_linear.py
# INFO:__main__:loger active
# INFO:__main__:inserted file:csvdata/customers.csv
# INFO:__main__:inserted file:csvdata/products.csv
# INFO:__main__:<L> script cpu usage: 23.2%
# INFO:__main__:<L> script memory usage  = [114.64453125]
# INFO:__main__:<L> script total runtime: h:m:s:ms>> 00:00:00:176
# INFO:__main__:((1000, 0, 1000, 'h:m:s:ms>> 00:00:00: 99'),
#                (1000, 0, 1000, 'h:m:s:ms>> 00:00:00: 71'))

# Example run - insert one-by-one via 'insert_one()' method:
# INFO:__main__:database_linear.py
# INFO:__main__:loger active
# INFO:__main__:inserted file:csvdata/customers.csv
# INFO:__main__:inserted file:csvdata/products.csv
# INFO:__main__:<L> script cpu usage: 24.9%
# INFO:__main__:<L> script memory usage  = [114.6640625]
# INFO:__main__:<L> script total runtime: h:m:s:ms>> 00:00:01:152
# INFO:__main__:((1000, 0, 1000, 'h:m:s:ms>> 00:00:00:594'),
#                (1000, 0, 1000, 'h:m:s:ms>> 00:00:00:552'))
# ==================================
