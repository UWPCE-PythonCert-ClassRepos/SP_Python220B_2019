#!/usr/bin/env python3

"""
Creates a Mongo database connection, adds data, and queries data
"""

# pylint: disable= C0301, E0401, R0914, C0103, W1202

import csv
import logging
import os
import time
from pymongo import MongoClient

logging.basicConfig(level=logging.WARNING)


class MongoDBConnection:
    """
    Connect to Mongo database, opens and closes.
    """

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def timer(func):
    """
    Decorator that times functions
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        output = func(*args, **kwargs)
        end = time.time()
        total_time = end - start
        logging.info('{}: {:3f}'.format(func.__name__, total_time))
        return output
    return wrapper


def logger_setup():
    """
    Function to configure logger
    """
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = "timings.txt"
    formatter = logging.Formatter(log_format)
    logger = logging.getLogger()
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)


@timer
def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Creates a connection to Mongo database, clears data, and updates with data from CSVs
    """
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.hpn
        logging.info("Creating Mongo database.")

        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        logging.info("Dropping old data.")
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()

        product_csv = os.path.join(directory_name, product_file)
        customer_csv = os.path.join(directory_name, customer_file)
        rental_csv = os.path.join(directory_name, rentals_file)

        csvs = {product_csv: products, customer_csv: customers, rental_csv: rentals}

        added_list = []
        errors_list = []

        for csv_path, collection in csvs.items():
            adds = 0
            errors = 0
            try:
                logging.info(f"Importing {csv_path}")
                with open(csv_path) as csv_data:
                    data = csv.DictReader(csv_data)
                    for row in data:
                        try:
                            collection.insert_one(row)
                            adds += 1
                        except MongoClient.OperationFailure:
                            errors += 1
            except FileNotFoundError:
                logging.error(f"{csv_path} was not found")
                errors += 1

            added_list.append(adds)
            errors_list.append(errors)

        return tuple(added_list), tuple(errors_list)


@timer
def show_available_products():
    """
    Creates a dictionary of available products
    """

    available_products = {}
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.hpn
        logging.info("Searching for products.")

        for prod in db.products.find({"quantity_available": {"$gt": "0"}}):
            available_products[prod["product_id"]] = {'description': prod["description"],
                                                      'product_type': prod["product_type"],
                                                      'quantity_available': prod["quantity_available"]}
    return available_products


@timer
def show_rentals(product_id):
    """
    Creates a dictionary of user rentals
    """

    rental_dict = {}
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.hpn
        logging.info(f"Searching for {product_id} rentals.")

        for rental in db.rentals.find({"product_id": product_id}):
            users = rental["user_id"]
            logging.info(f"Details for {users}")
            for user in db.customers.find({"user_id": users}):
                rental_dict[users] = {'name': user["name"],
                                      'address': user["address"],
                                      'phone_number': user["phone_number"],
                                      'email': user["email"]}
    return rental_dict


if __name__ == '__main__':
    logger_setup()
    import_data("csvs", "products_1000.csv", "customers_1000.csv", "rentals_1000.csv")
    show_available_products()
    show_rentals("pid582")

    import_data("csvs", "products_10000.csv", "customers_10000.csv", "rentals_10000.csv")
    show_available_products()
    show_rentals("pid582")

    import_data("csvs", "products_100000.csv", "customers_100000.csv", "rentals_100000.csv")
    show_available_products()
    show_rentals("pid582")
