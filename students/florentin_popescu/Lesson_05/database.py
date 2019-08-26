# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 08:59:40 2019
@author: Florentin Popescu
"""

# imports
import csv
import logging

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
# =======================================================================
# alternative set-up connectivity to MongoDB and document insertion
#           - left to experiment with outside the course -
#             (http://docs.mongoengine.org/tutorial.html)

# import mongoengine
# from mongoengine import *

# mongoengine.connect("FlorentinDB", host="localhost", port=27017)

# class Customer(Document):
#    customer_id = StringField(required=True, max_length=8)
#    first_name = StringField(max_length=50)
#    last_name = StringField(max_length=50)
#    address = StringField(max_length=500)
#    phone = StringField(max_length=10)
#    email = StringField(max_length=100)
#    meta = {"collection": "Customers"}

# sample_customer = Customer(customer_id = "user0000",
#                            first_name = "Lara",
#                            last_name = "Croft",
#                            address = "Los Angeles, CA 22222",
#                            phone = "8888888888",
#                            email = "lara_croft@usa.com")
# sample_customer.save()

# retriving sample_customer's info from collection 'Customers'
# for customer in Customer.objects:
#    print("Name: {}, {}".format(customer.last_name, customer.first_name))

# similar construction of 'Product' and 'Rental' classes and collections
# ========================================================================


def import_csv(collection, path):
    """
        import csv file to MongoDB
    """
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
            if "" in [tmp_lst[i] for i in range(len(item))]:
                no_err_row = [tmp_lst[i] for i in range(len(item))].count("")
                csv_err += no_err_row
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
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.FlorentinDB

    product = database["product"]
    customer = database["customer"]
    rental = database["rental"]

    cnt = (import_csv(product, f"{directory_name}/{product_file}")[0],
           import_csv(customer, f"{directory_name}/{customer_file}")[0],
           import_csv(rental, f"{directory_name}/{rentals_file}")[0])
    return cnt
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


def drop_data():
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
