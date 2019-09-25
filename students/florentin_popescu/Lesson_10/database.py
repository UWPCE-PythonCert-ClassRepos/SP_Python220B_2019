# -*- coding: utf-8 -*-
"""
Created on Mon Aug  16 19:10:38 2019
@author: Florentin Popescu
"""
# pylint: disable=R0201

# imports
import csv
import logging
import operator as op
import types
import time as tm
import contextlib

from pymongo import MongoClient
# ==================================

# set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("database.py")
LOGGER.info("loger active")
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

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
# ==================================


def timer(method):
    """ decorator adding ability to time function's call"""
    def timewraper(*args, **kwargs):
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.FlorentinDB
            # -----------------------------------------------
            start = tm.time()
            pre_cnt = (database.product.estimated_document_count(),
                       database.customer.estimated_document_count(),
                       database.rental.estimated_document_count())
            # --------------------
            timedfunction = method(*args, **kwargs)
            # --------------------
            pst_cnt = (database.product.estimated_document_count(),
                       database.customer.estimated_document_count(),
                       database.rental.estimated_document_count())
            end = tm.time()
            # -----------------------------------------------
            cnt_prod, cnt_cust, cnt_rent = ((abs(pst_cnt[i] - pre_cnt[i])
                                             for i in range(3)))
            if "log_time" in kwargs:
                name = kwargs.get("log_name", method.__name__.upper())
                kwargs["log_time"][name] = round(abs((end - start) * 1000), 4)
            else:
                LOGGER.info("method: %r, time: %2.4f ms, records: %s \n",
                            method.__name__, round(abs(end - start) * 1000, 4),
                            (cnt_prod, cnt_cust, cnt_rent))

                with open("timing.txt", mode="a+") as file:
                    file.write(f"function name: {method.__name__}, "
                               + f"time: {round(abs(end - start)*1000, 4)} ms,"
                               + f" records processed: "
                               + f"{cnt_prod} products, "
                               + f"{cnt_cust} customers, "
                               + f"{cnt_rent} rentals\n")
            return timedfunction
    return timewraper
# ==================================


class MetaTimer(type):
    """
        metaclass to add timing to classes
    """
    def __new__(cls, clsname, bases, clsdict):
        """ make a new instance of the class """
        if op.gt(len(bases), 1):
            raise TypeError("multiple base classes inherited")
        for attr, val in clsdict.items():
            if isinstance(val, types.FunctionType):
                clsdict[attr] = timer(val)
                cls.type_name = type(attr).__name__
        obj = super(MetaTimer, cls).__new__(cls, clsname, bases, clsdict)
        obj.attr = []
        return obj

    def __init__(cls, clsname, bases, clsdict):
        """ initializer of an instance of the class"""
        LOGGER.info("initializing class %s in MetaTimer", clsname)
        super(MetaTimer, cls).__init__(clsname, bases, clsdict)

    def __call__(cls, *args, **kwargs):
        """ call metaclass to instantiate the class """
        LOGGER.info("MetaTimer called to instantiate %s", cls)
        return type.__call__(cls, *args, **kwargs)

    def __str__(cls, *args, **kwargs):
        """ class sttucture """
        show_attr = []
        for attr, val in sorted(cls.__dict__.items()):
            show_attr.append(f"{attr}: {val}")
        return "{} with time wraped {}\n".format(cls.__class__.__name__,
                                                 ", ".join(show_attr))
# ==================================


class LoadToMongo(metaclass=MetaTimer):
    """
        class of all operation on database
    """

    def __init__(self):
        cls = self.__class__
        LOGGER.info("%s operations to be executed:", cls.__name__)

    def import_csv(self, collection, path):
        """ import csv file to MongoDB """
        try:
            with open(path, "r") as csvfile:
                csv_dct = csv.DictReader(csvfile, delimiter=",")
                ins_csv_dct = collection.insert_many(csv_dct)

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

    def import_data(self, directory_name, product_file,
                    customer_file, rentals_file):
        """ import csv files into MongoDB """
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.FlorentinDB

            LOGGER.info("import product file:")
            product = database["product"]
            cnt_prod = self.import_csv(product,
                                       f"{directory_name}/{product_file}")

            LOGGER.info("import customer file:")
            customer = database["customer"]
            cnt_cust = self.import_csv(customer,
                                       f"{directory_name}/{customer_file}")

            LOGGER.info("import rental file:")
            rental = database["rental"]
            cnt_rent = self.import_csv(rental,
                                       f"{directory_name}/{rentals_file}")

            return cnt_prod, cnt_cust, cnt_rent
    # ==================================

    def show_available_products(self):
        """ list available products """
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

    def show_rentals(self, product_id):
        """ list customers that rented products """
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

    def print_products(self):
        """ print products """
        products = self.show_available_products()
        for prod in products:
            print(prod, products[prod])
    # ==================================

    def drop_data(self):
        """
            drop data from MongoDB
        """
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.FlorentinDB

            dbs = ["product", "customer", "rental"]
            for name in dbs:
                database[name].drop()
            return "data has been dropped from Mongo database"
    # ==================================


if __name__ == "__main__":
    IMP = LoadToMongo()

    with contextlib.redirect_stdout(None):
        IMP.import_data("csvdata", "products.csv",
                        "customers.csv", "rentals.csv")
        IMP.show_rentals("prd0000")
        IMP.print_products()
        IMP.show_available_products()
        IMP.drop_data()
