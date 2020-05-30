# Lesson 7 assignment Concurrency and Async Activity, created by Niels Skvarch
"""
import code taken from lesson 5 assignment, stripped down for testing run times.
Create a Mongo Database from 2 csv files given as input for customer and product
information. It will clear the database so that this module can be run again.
"""

import logging
import datetime
import time
import os
import csv
from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d")+"db.log"
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)


class MongoDBConnection:
    """MongoDB Connection taken from lesson example, establishes and
    closes connections to the Mongo Database engine."""

    def __init__(self, host='127.0.0.1', port=27017):
        """Connection Parameters"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Open database"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database"""
        self.connection.close()


def import_data(directory, customer_data_file, product_data_file):
    """Create a new Mongo Database using the provided 2 csv input files. Returns count
    information on records added and errors encountered for each record category."""
    cust_add, prod_add = 0, 0
    product_file_path = os.path.join(directory, product_data_file)
    customer_file_path = os.path.join(directory, customer_data_file)
    start = time.time()
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        customers = db["customers"]
        products = db["products"]

        product_start_count = products.count_documents({})
        customers_start_count = customers.count_documents({})

    with open(customer_file_path) as file:
        converted = csv.DictReader(file)
        for i in converted:
            add_customer = {"customer_id": i["customer_id"],
                            "name": i["name"],
                            "address": i["address"],
                            "phone_number": i["phone_number"],
                            "email_address": i["email_address"]}
            customers.insert_one(add_customer)
            LOGGER.info("Customer successfully added to the database.")
            cust_add += 1

    with open(product_file_path) as file:
        converted = csv.DictReader(file)
        for i in converted:
            add_product = {"product_id": i["product_id"],
                           "description": i["description"],
                           "type": i["type"],
                           "number_available": i["number_available"]}

            products.insert_one(add_product)
            LOGGER.info("Product successfully added to the database.")
            prod_add += 1

    run_time = format(time.time() - start, ".2f")
    product_end_count = products.count_documents({})
    customers_end_count = customers.count_documents({})
    product_report = (prod_add, product_start_count, product_end_count, run_time)
    customer_report = (cust_add, customers_start_count, customers_end_count, run_time)

    return product_report, customer_report


def clear_db():
    """Clears the database collections."""
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        db.products.drop()
        db.customers.drop()
        LOGGER.info("Database Collections have been cleared.")
