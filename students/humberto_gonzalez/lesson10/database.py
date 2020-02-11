# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# pylint: disable=too-many-locals,logging-format-interpolation,bare-except,line-too-long

import logging
import os
import csv
import peewee
from pymongo import MongoClient
import time


def timekeeper(func):
    """rapper for keeping time of functions"""
    def func_wrapper(*arg, **kwargs):
        LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

        LOG_FILE = "timing.txt"

        FORMATTER = logging.Formatter(LOG_FORMAT)

        FILE_HANDLER = logging.FileHandler(LOG_FILE)
        FILE_HANDLER.setLevel(logging.WARNING)
        FILE_HANDLER.setFormatter(FORMATTER)
        CONSOLE_HANDLER = logging.StreamHandler()
        CONSOLE_HANDLER.setLevel(logging.DEBUG)
        CONSOLE_HANDLER.setFormatter(FORMATTER)
        LOGGER = logging.getLogger()
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.addHandler(FILE_HANDLER)
        LOGGER.addHandler(CONSOLE_HANDLER)

        LOGGER.setLevel(logging.DEBUG)
        FILE_HANDLER.setLevel(logging.DEBUG)
        CONSOLE_HANDLER.setLevel(logging.DEBUG)

        start_time = time.time()
        results = func(*arg, *kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        
        if func.__name__ == "import_data":
            added_entries = sum(results[0])
            LOGGER.info(f"{func.__name__} took {run_time} to process {added_entries} entries")
        else:
            LOGGER.info(f"{func.__name__} took {run_time} to run")
        return results
    return func_wrapper


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

@timekeeper
def import_data(directory_name, product_file, customer_file, rentals_file):
    """imports data from csv file, returns counts of entries and errors"""

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.storeDB

        customers = database["customers"]
        products = database["products"]
        rentals = database["rentals"]

        #entry counts
        customer_count = 0
        product_count = 0
        rental_count = 0

        #error_counts
        customer_errors = 0
        product_errors = 0
        rental_errors = 0

        with open(os.path.join(directory_name, product_file)) as csv_file:

            product_data = csv.reader(csv_file, delimiter=",")
            for entry in product_data:
                try:
                    product_entry = {"product_id":entry[0],
                                     "description":entry[1],
                                     "product_type":entry[2],
                                     "quantity_available":entry[3]}
                    products.insert_one(product_entry)
                    product_count += 1
                except peewee.IntegrityError:
                    product_errors += 1

        with open(os.path.join(directory_name, customer_file)) as csv_file:

            customer_data = csv.reader(csv_file, delimiter=",")
            for entry in customer_data:
                try:
                    customer_entry = {"user_id":entry[0],
                                      "name":entry[1],
                                      "address":entry[2],
                                      "phone_number":entry[3],
                                      "email":entry[4]}
                    customers.insert_one(customer_entry)
                    customer_count += 1
                except peewee.IntegrityError:
                    customer_errors += 1

        with open(os.path.join(directory_name, rentals_file)) as csv_file:

            rental_data = csv.reader(csv_file, delimiter=",")
            for entry in rental_data:
                try:
                    rental_entry = {"rental_id":entry[0],
                                    "user_id":entry[1],
                                    "product_id":entry[2]}
                    rentals.insert_one(rental_entry)
                    rental_count += 1
                except peewee.IntegrityError:
                    rental_errors += 1

    return ((customer_count, product_count, rental_count),
            (customer_errors, product_errors, rental_errors))

@timekeeper
def show_available_products():
    """Returns a dictionary of all available products in the database"""
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.storeDB
        products = database["products"]

        available_products = {}
        for product_entry in products.find({"quantity_available":{"$gt":"0"}}):
            available_products[product_entry["product_id"]] = {k:v for k, v in product_entry.items() if k not in ('_id', 'product_id')}
        return available_products

@timekeeper
def show_rentals(product_id):
    """Finds user and user information who have rented product with given product id"""

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.storeDB
        rentals = database["rentals"]
        customers = database["customers"]

        customer_info = {}
        customer_ids = []

        for rental_entry in rentals.find({"product_id":product_id}):
            customer_ids.append(rental_entry["user_id"])

        for usr_id in customer_ids:
            cust = customers.find_one({"user_id":usr_id})
            customer_info[usr_id] = {k:v for k, v in cust.items() if k != "_id"}

        return customer_info


def tearDown():
    """Tearing down anything created or used for testing purposes"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.storeDB
        #clearing the databases for testing purposes
        db["customers"].drop()
        db["products"].drop()
        db["rentals"].drop()


if __name__ == "__main__":
    directory_name = "./csv_files"
    import_data(directory_name, "products_short.csv", 
                "customers_short.csv", "rentals_short.csv")
    import_data(directory_name, "products_med.csv", 
                "customers_med.csv", "rentals_med.csv")
    import_data(directory_name, "products_large.csv", 
                "customers_large.csv", "rentals_large.csv")
    show_available_products()
    show_rentals("prd002")
    tearDown()
