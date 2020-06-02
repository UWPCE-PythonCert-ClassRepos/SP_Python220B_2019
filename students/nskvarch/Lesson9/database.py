# Lesson 5 assignment HP Norton "Consume APIs with NoSQL Activity, created by Niels Skvarch
"""
Create a Mongo Database from 3 csv files given as input for customers, products,
and rental information. With the database created, execute queries for
sales information. Finally it will clear
the database so that this module can be run again.
"""

import logging
import datetime
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
        LOGGER.info("Connecting to the Mongo DB")
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database"""
        LOGGER.info("Mongo DB connection closed")
        self.connection.close()


def import_data(directory, customer_data_file, product_data_file, rental_data_file):
    """Create a new Mongo Database using the provided 3 csv input files. Returns count
    information on records added and errors encountered for each record category."""
    cust_err, prod_err, rent_err = 0, 0, 0
    product_file_path = os.path.join(directory, product_data_file)
    customer_file_path = os.path.join(directory, customer_data_file)
    rental_file_path = os.path.join(directory, rental_data_file)
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        customers = db["customers"]
        products = db["products"]
        rentals = db["rentals"]

    try:
        with open(customer_file_path) as file:
            converted = csv.DictReader(file)
            for i in converted:
                add_customer = {"customer_id": i["customer_id"],
                                "name": i["name"],
                                "address": i["address"],
                                "phone_number": i["phone_number"],
                                "email_address": i["email_address"]}
                try:
                    customers.insert_one(add_customer)
                    LOGGER.info("Customer successfully added to the database.")
                except NameError:
                    LOGGER.info("Error adding the following data %s", add_customer)
                    cust_err += 1
                    raise NameError
    except FileNotFoundError:
        LOGGER.info("Customer Data file was not found at %s.", customer_file_path)
        cust_err += 1

    try:
        with open(product_file_path) as file:
            converted = csv.DictReader(file)
            for i in converted:
                add_product = {"product_id": i["product_id"],
                               "description": i["description"],
                               "type": i["type"],
                               "number_available": i["number_available"]}
                try:
                    products.insert_one(add_product)
                    LOGGER.info("Product successfully added to the database.")
                except NameError:
                    LOGGER.info("Error adding the following data %s", add_product)
                    prod_err += 1
    except FileNotFoundError:
        LOGGER.info("Product Data file was not found at %s.", product_file_path)
        prod_err += 1

    try:
        with open(rental_file_path) as file:
            converted = csv.DictReader(file)
            for i in converted:
                add_rental = {"customer_id": i["customer_id"],
                              "product_id": i["product_id"]}
                try:
                    rentals.insert_one(add_rental)
                    LOGGER.info("Rental info successfully added to the database.")
                except NameError:
                    LOGGER.info("Error adding the following data %s", add_rental)
                    rent_err += 1
    except FileNotFoundError:
        LOGGER.info("Rental Data file was not found at %s.", rental_file_path)
        rent_err += 1
    success_count = (products.count_documents({}), customers.count_documents({}),
                     rentals.count_documents({}))
    error_count = (prod_err, cust_err, rent_err)
    return success_count, error_count


def show_available_products():
    """Return a dictionary of available products."""
    mongo = MongoDBConnection()
    product_dict = {}

    with mongo:
        db = mongo.connection.media
        for i in db.products.find({"number_available": {"$gt": "0"}}):
            prod_data = {"description": i["description"], "type": i["type"],
                         "number_available": i["number_available"]}
            product_dict[i["product_id"]] = prod_data
    return product_dict


def show_rentals(product_id):
    """Return a dictionary of customers who have rented a specific
     product form the provided product_id."""
    mongo = MongoDBConnection()
    customer_dict = {}

    with mongo:
        db = mongo.connection.media
        for i in db.rentals.find({"product_id": product_id}):
            for j in db.customers.find({"customer_id": i["customer_id"]}):
                customer_dict[j["customer_id"]] = {"name": j["name"], "address": j["address"],
                                                   "phone_number": j["phone_number"],
                                                   "email_address": j["email_address"]}
    return customer_dict


def clear_db():
    """Clears the database collections."""
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()
        LOGGER.info("Database Collections have been cleared.")
