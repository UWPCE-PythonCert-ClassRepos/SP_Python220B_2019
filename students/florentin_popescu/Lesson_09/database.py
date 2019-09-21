# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 08:59:40 2019
@author: Florentin Popescu
"""

# imports
import csv
import logging
import pprint as pp
import operator as op

from contextlib import ContextDecorator
from pymongo import MongoClient
from pymongo import errors as mer
# ==================================

# set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("database.py")
LOGGER.info("loger active")
# ==================================


class TrackEntryExit(ContextDecorator):
    """ track logger """
    def __init__(self, name):
        """ initializer """
        self.name = name

    def __enter__(self):
        """ enter """
        pp.pprint(f"entering: {self.name}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ exit """
        pp.pprint(f"exiting: {self.name}")
        if exc_type:
            pp.pprint(f"exc_type: {exc_type}")
            pp.pprint(f"exc_val: {exc_val}")
            pp.pprint(f"exc_tb: {exc_tb}")
# ========================================


class MyPrinting(ContextDecorator):
    """ costumized printing """
    def __enter__(self):
        """ enter """
        pp.pprint("start printing")
        return self

    def __exit__(self, *exc):
        """ exit """
        pp.pprint("end printing")
        return False
# ==================================


class MongoDBConnection():
    """
        establish MongoDB connection (per assignment's example)
    """
    def __init__(self, host='127.0.0.1', port=27017):
        """
            use public ip-address and port
        """
        self.host = host
        self.port = port
        self.connection = None
        self.database = None
        self.product = None
        self.customer = None
        self.rental = None

    def __enter__(self):
        """ enter """
        if self.connection is None:
            try:
                self.connection = MongoClient(self.host, self.port)
                LOGGER.info("connected to mongo")
                LOGGER.info("entering host %s via port %s ",
                            self.host, self.port)
                self.database = self.connection.FlorentinDB
                self.product = self.database["product"]
                self.customer = self.database["customer"]
                self.rental = self.database["rental"]
                LOGGER.info("database %s established on mongo", self.database)
                LOGGER.info("collections %s, %s, %s available in %s",
                            self.product, self.customer, self.rental,
                            self.database)
            except mer.ConnectionFailure as err:
                LOGGER.info("error connecting to mongo\n %s", err)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ exit """
        if exc_type:
            pp.pprint(f"exc_type: {exc_type}")
            pp.pprint(f"exc_val: {exc_val}")
            pp.pprint(f"exc_tb: {exc_tb}")
        self.connection.close()
        LOGGER.info("disconected from mongo")
# =======================================================================


def import_csv(collection, path):
    """
        import csv file to MongoDB
    """
    with TrackEntryExit("import_csv"):
        try:
            with open(path, "r") as csvfile:
                try:
                    csv_dct = csv.DictReader(csvfile, delimiter=",")
                    ins_csv_dct = collection.insert_many(csv_dct)
                except mer.BulkWriteError as err:
                    LOGGER.info("insertion error: %s", err.details)

            with open(path, "r") as csvfile1:
                csv_dct1 = csv.DictReader(csvfile1, delimiter=",")
                csv_lst = list(csv_dct1)

            csv_err = 0
            for item in csv_lst:
                tmp_lst = list(item.values())
                no_err = [tmp_lst[i] for i in range(len(item))].count("")
                if op.ne(no_err, 0):
                    csv_err = op.iadd(csv_err, no_err)
                    LOGGER.info("inserted file has missing values")

            return len(ins_csv_dct.inserted_ids), csv_err

        except (FileNotFoundError, UnboundLocalError) as err:
            LOGGER.info("path-indicated file not found")
            LOGGER.info(err)
# ==================================


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
        import csv files into MongoDB.
    """
    with TrackEntryExit("import_data"):
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.FlorentinDB
            product = database["product"]
            customer = database["customer"]
            rental = database["rental"]

            cnt = (import_csv(product, f"{directory_name}/{product_file}"),
                   import_csv(customer, f"{directory_name}/{customer_file}"),
                   import_csv(rental, f"{directory_name}/{rentals_file}"))
            return cnt
# ==================================


def show_available_products():
    """
        list available products
    """
    with TrackEntryExit("show_available_products"):
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.FlorentinDB

            prod = database["product"].find({"quantity_available":
                                             {"$ne": "0"}})
            prod_dict = {prd["product_id"]:
                         {"description": prd["description"],
                          "product_type": prd["product_type"],
                          "quantity_available":
                              int(prd["quantity_available"])} for prd in prod}
            return prod_dict
# ==================================


def show_rentals(product_id):
    """
        list customers that rented products
    """
    with TrackEntryExit("show_rentals"):
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
                          "address": cust["address"], "phone": cust["phone"],
                          "email": cust["email"]} for cust in customers}
            return cust_dict
# ==================================


def print_products():
    """
        print products
    """
    with TrackEntryExit("print_products"):
        with MyPrinting():
            products = show_available_products()
            for prod in products:
                print(prod, products[prod])
# ==================================


def drop_data():
    """
        drop data from MongoDB
    """
    with TrackEntryExit("drop_data"):
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.FlorentinDB

            dbs = ["product", "customer", "rental"]
            for name in dbs:
                database[name].drop()
            return pp.pprint("data has been dropped from Mongo database")
# ==================================


if __name__ == "__main__":
    IMPORTED = import_data("csvdata", "products.csv",
                           "customers.csv", "rentals.csv")
    pp.pprint(IMPORTED)
    pp.pprint(show_rentals("prd0000"))
    print_products()
    pp.pprint(show_available_products())
    drop_data()
