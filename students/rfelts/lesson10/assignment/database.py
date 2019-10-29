#!/usr/bin/env python3

# Russell Felts
# Assignment 10

""" Basic Mongo database functionality """

# pylint: disable=too-many-arguments

import logging
import csv
import os
import time
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, DuplicateKeyError

# Set up logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler("timings.txt")
FILE_HANDLER.setFormatter(FORMATTER)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)


class MongoDBConnection:
    """ Setup Mongo DB Connection """
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def perf_timer(func):
    """
    Decorator for timing functions
    :param func: Function being timed
    :return: Timing data
    """
    def wrapper(*args, **kwargs):
        """
        Function for timing a function
        """
        result_string = "It took function %s %s seconds to process %s records"
        start = time.perf_counter()
        result = func(*args, **kwargs)
        total_time = time.perf_counter() - start
        if func.__name__ == "import_data":
            LOGGER.info(result_string, func.__name__, total_time,
                        result[0][0] + result[0][1] + result[0][2])
        elif isinstance(result, dict) and result.get("record_count"):
            LOGGER.info(result_string, func.__name__, total_time, result["record_count"])
        else:
            LOGGER.info("It took function %s %s seconds to process", func.__name__, total_time)

        return result
    return wrapper


@perf_timer
def csv_to_list(csv_file):
    """
    Create list of maps containing the data to be imported into the databases
    :param csv_file: CSV file containing the info to be imported into the db
    :return: List containing maps of the data to be imported to each db
    """
    with open(csv_file, 'r') as file:
        reader = [{k: v for k, v in row.items()}
                  for row in csv.DictReader(file, skipinitialspace=True)]
        return reader


@perf_timer
def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Take a directory name three csv files as input, one with product data, one with customer data
    and the third one with rentals data and creates and populates a new MongoDB database with
    these data. It returns 2 tuples: the first with a record count of the number of products,
    customers and rentals added (in that order), the second with a count of any errors that
    occurred, in the same order.
    :param directory_name: Name of the directory containing the csv files
    :param product_file: The csv file containing the product data
    :param customer_file: The csv file containing the customer data
    :param rentals_file: The csv file containing the rental data
    :return: 2 tuples: the first with a record count of the number of products, customers and
    rentals added (in that order), the second with a count of any errors that occurred, in the
    same order
    """
    LOGGER.debug("\n\nConnecting the the Mongo DB")
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.media

        LOGGER.debug("Creating mongo collections for the product, customer, and rental data")

        products_col = mongo_db["products_col"]
        customers_col = mongo_db["customers_col"]
        rentals_col = mongo_db["rentals_col"]

        product_path = os.path.join(directory_name, product_file)
        customer_path = os.path.join(directory_name, customer_file)
        rental_path = os.path.join(directory_name, rentals_file)

        data_list = [{"name": "product", "path": product_path, "db": products_col, "errors": 0},
                     {"name": "customer", "path": customer_path, "db": customers_col, "errors": 0},
                     {"name": "rental", "path": rental_path, "db": rentals_col, "errors": 0}]

        for item in data_list:
            try:
                temp_list = csv_to_list(item.get("path"))
                try:
                    LOGGER.debug("Adding items to the %s database.", item.get("name"))
                    item.get("db").insert_many(temp_list)
                except BulkWriteError:
                    LOGGER.debug("BulkWriteError adding items to the %s collection.",
                                 item.get("name"))
                    item["errors"] += 1
                except DuplicateKeyError:
                    LOGGER.debug("DuplicateKeyError adding items to the %s collection.",
                                 item.get("name"))
                    item["errors"] += 1
            except FileNotFoundError:
                item["errors"] += 1
                LOGGER.debug("Number of errors for %s: %s", item.get("name"), item.get("errors"))
                LOGGER.error("The file %s was not found", product_path)

            LOGGER.debug("The total errors are %s", item.get("errors"))

        return (products_col.count_documents({}), customers_col.count_documents({}),
                rentals_col.count_documents({})),\
               (data_list[0].get("errors"), data_list[1].get("errors"), data_list[2].get("errors"))


@perf_timer
def show_available_products():
    """
    Return a Python dictionary of products listed as available with the following fields:
    product_id, description, product_type, quantity_available.
    :return: dictionary of products listed
    """
    LOGGER.debug("Connecting the the Mongo DB")
    product_dict = {}
    counter = 0
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.media
        LOGGER.debug("Finding all available products")
        for prod in mongo_db.products_col.find({"available": {"$gt": "0"}}):
            counter += 1
            product_dict[prod["id"]] = {"description": prod["description"],
                                        "type": prod["type"], "available": prod["available"]}
        product_dict["record_count"] = counter
        return product_dict


@perf_timer
def show_rentals(product_id):
    """
    Return a dictionary with the user information from users that have rented the
    product with matching product_id
    :param product_id: Product Id of the product that was rented
    :return: Dictionary with the user information - user_id, name, address, phone_number, email
    """
    LOGGER.debug("Connecting the the Mongo DB")
    cust_dict = {}
    counter = 0
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.media
        LOGGER.debug("Finding all products rented with id %s", product_id)
        for rental in mongo_db.rentals_col.find({"prod_id": product_id}):
            for customer in mongo_db.customers_col.find({"id": rental.get("cust_id")}):
                cust_dict[customer["id"]] = {"id": customer["id"],
                                             "first_name": customer["first_name"],
                                             "last_name": customer["last_name"],
                                             "address": customer["address"],
                                             "phone_number": customer["phone_number"],
                                             "email": customer["email"]}
                counter += 1
            counter += 1
        cust_dict["record_count"] = counter
        return cust_dict


@perf_timer
def drop_all_collections():
    """ Delete all collections in database """
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.media
        LOGGER.debug("\n\nDropping all database collections")
        mongo_db.products_col.drop()
        mongo_db.customers_col.drop()
        mongo_db.rentals_col.drop()
