# -*- coding: utf-8 -*-
"""
Spyder Editor
"""
# pylint: disable=too-many-locals,logging-format-interpolation,duplicate-code,duplicate-code,invalid-name

import time
import logging
import os
import csv
import peewee
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

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

def import_customer_data(directory_name, customer_file):
    """imports customer data from csv file"""

    start = time.time()

    mongo = MongoDBConnection()

    with mongo:
        LOGGER.info("Establishing MongoDB connection")
        database = mongo.connection.storeDB

        LOGGER.info("Establishing databases")
        customers = database["customers"]
        initial_entries = database.customers.count_documents({})

        #entry counts
        added_entries = 0

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
                    added_entries += 1
                    LOGGER.info(f"Added {entry[0]} to customer database")
                except peewee.IntegrityError:
                    LOGGER.info(f"Error adding {entry[0]} to customer database")

            final_entries = database.customers.count_documents({})

            return((initial_entries, added_entries, final_entries,
                    (time.time() - start)))

def import_product_data(directory_name, product_file):
    """imports product data from csv file"""

    start = time.time()

    mongo = MongoDBConnection()

    with mongo:
        LOGGER.info("Establishing MongoDB connection")
        database = mongo.connection.storeDB

        LOGGER.info("Establishing databases")
        products = database["products"]
        initial_entries = database.products.count_documents({})

        #entry counts
        added_entries = 0

        with open(os.path.join(directory_name, product_file)) as csv_file:

            product_data = csv.reader(csv_file, delimiter=",")
            for entry in product_data:
                try:
                    product_entry = {"product_id":entry[0],
                                     "description":entry[1],
                                     "product_type":entry[2],
                                     "quantity_available":entry[3]}
                    products.insert_one(product_entry)
                    added_entries += 1
                    LOGGER.info(f"Added {entry[0]} to product database")
                except peewee.IntegrityError:
                    LOGGER.info(f"Error adding {entry[0]} to product database")

            final_entries = database.products.count_documents({})

            return((initial_entries, added_entries, final_entries,
                    (time.time() - start)))

def import_rental_data(directory_name, rental_file):
    """imports rental data from csv file"""

    start = time.time()

    mongo = MongoDBConnection()

    with mongo:
        LOGGER.info("Establishing MongoDB connection")
        database = mongo.connection.storeDB

        LOGGER.info("Establishing databases")
        rentals = database["rentals"]
        initial_entries = database.rentals.count_documents({})

        #entry counts
        added_entries = 0

        with open(os.path.join(directory_name, rental_file)) as csv_file:

            rental_data = csv.reader(csv_file, delimiter=",")
            for entry in rental_data:
                try:
                    rental_entry = {"rental_id":entry[0],
                                    "user_id":entry[1],
                                    "product_id":entry[2]}
                    rentals.insert_one(rental_entry)
                    added_entries += 1
                    LOGGER.info(f"Added {entry[0]} to rental database")
                except peewee.IntegrityError:
                    LOGGER.info(f"Error adding {entry[0]} to rental database")

            final_entries = database.rentals.count_documents({})

            return((initial_entries, added_entries, final_entries,
                    (time.time() - start)))


def clear_database():
    """Clear the database for each collection"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.storeDB
        db["products"].drop()
        db["customers"].drop()
        db["rentals"].drop()


def print_results(results):
    """Prints out the report given the results"""
    print(f"Intial Entries: {results[0]}")
    print(f"Added Entries: {results[1]}")
    print(f"Final Entries: {results[2]}")
    print(f"Total Run Time: {results[3]}")
    print("\n")


if __name__ == "__main__":
    clear_database()
    start_time = time.time()
    customers_ = import_customer_data("./data", "customers.csv")
    products_ = import_product_data("./data", "products.csv")
    rentals_ = import_rental_data("./data", "rentals.csv")
    end_time = time.time()
    print("\n")
    print("Customers Report")
    print_results(customers_)
    print("Products Report")
    print_results(products_)
    print("Rentals Report")
    print_results(rentals_)
    print("\n")
    print(f"Total Run Time: {end_time-start_time}")
