#!/usr/bin/env python3

# Russell Felts
# Assignment 7

""" Basic Mongo database functionality """

# pylint: disable=too-many-arguments, too-many-locals

import logging
import csv
import os
import time
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, DuplicateKeyError


# Set up logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"

FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler("db.log")
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


def csv_to_list(csv_file):
    """
    Create list of maps containing the data to be imported into the databases
    :param csv_file: CSV file containing the info to be imported into the db
    :return: List containing maps of the data to be imported to each db
    """
    with open(csv_file, 'r') as file:
        LOGGER.info("Reading the file")
        reader = [{k: v for k, v in row.items()}
                  for row in csv.DictReader(file, skipinitialspace=True)]
        LOGGER.info("Done reading the file")
        return reader


def import_data(directory_name, product_file, customer_file):
    """
    Take a directory name and two csv files as input, one with product data, one with
    customer data and creates a db. Then calls import_file which populates database.
    It returns 2 tuples: the number of records processed (int), the record count in the database
    prior to running (int), the record count after running (int), and the time taken to run
    the module (float).
    :param directory_name: Name of the directory containing the csv files
    :param product_file: The csv file containing the product data
    :param customer_file: The csv file containing the customer data
    :return: 2 tuples: the number of records processed (int), the record count in the database
    prior to running (int), the record count after running (int), and the time taken to run
    the module (float)
    """
    LOGGER.info("\n\nConnecting the the Mongo DB")
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.media

        LOGGER.info("Creating mongo collections for the product, customer, and rental data")

        products_col = mongo_db["products_col"]
        customers_col = mongo_db["customers_col"]

        product_path = os.path.join(directory_name, product_file)
        customer_path = os.path.join(directory_name, customer_file)

        data_list = [{"name": "product", "path": product_path, "db": products_col, "errors": 0},
                     {"name": "customer", "path": customer_path, "db": customers_col, "errors": 0}]
        with ThreadPoolExecutor(max_workers=2) as executor:
            start_time = time.perf_counter()
            data = executor.map(import_file, data_list)
        LOGGER.info("It took %s seconds to import the data", time.perf_counter() - start_time)
        data_tuples = []
        for temp_data in data:
            data_tuples.append(temp_data)
        return data_tuples


def import_file(item):
    """
    Populates a MongoDB database with the data that was passed in.
    :param item: Map including a name, path, db, and errors
    :return: A tuple containing record count and a count of any errors
    """
    start_time = time.perf_counter()

    try:
        temp_list = csv_to_list(item.get("path"))
        try:
            LOGGER.info("Adding items to the %s database.", item.get("name"))
            init_records = item.get("db").count_documents({})
            item.get("db").insert_many(temp_list)
        except BulkWriteError:
            LOGGER.info("BulkWriteError adding items to the %s collection.",
                        item.get("name"))
            item["errors"] += 1
        except DuplicateKeyError:
            LOGGER.info("DuplicateKeyError adding items to the %s collection.",
                        item.get("name"))
            item["errors"] += 1
    except FileNotFoundError:
        item["errors"] += 1
        LOGGER.info("Number of errors for %s: %s", item.get("name"), item.get("errors"))
        LOGGER.error("The file %s was not found", item.get("path"))

    import_time = time.perf_counter() - start_time
    # LOGGER.info("It took %s seconds to import the data", import_time)

    LOGGER.info("The total errors are %s", item.get("errors"))
    LOGGER.info("Got %s count of %s", item.get("db").count_documents({}), item.get("name"))
    LOGGER.info("The %s collection had %s records imported. There were initially %s records. "
                "There now are %s records. It took %s seconds for the import action to complete.",
                item.get("name"), item.get("db").count_documents({}) - init_records, init_records,
                item.get("db").count_documents({}), import_time)
    return (item.get("db").count_documents({}) - init_records, init_records,
            item.get("db").count_documents({}), import_time)


def show_available_products():
    """
    Return a Python dictionary of products listed as available with the following fields:
    product_id, description, product_type, quantity_available.
    :return: dictionary of products listed
    """
    LOGGER.info("Connecting the the Mongo DB")
    product_dict = {}
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.media
        LOGGER.info("Finding all available products")
        for prod in mongo_db.products_col.find({"available": {"$gt": "0"}}):
            product_dict[prod["id"]] = {"description": prod["description"],
                                        "type": prod["type"], "available": prod["available"]}
        return product_dict


def show_rentals(product_id):
    """
    Return a dictionary with the user information from users that have rented the
    product with matching product_id
    :param product_id: Product Id of the product that was rented
    :return: Dictionary with the user information - user_id, name, address, phone_number, email
    """
    LOGGER.info("Connecting the the Mongo DB")
    cust_dict = {}
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.media
        LOGGER.info("Finding all products rented with id %s", product_id)
        for rental in mongo_db.rentals_col.find({"prod_id": product_id}):
            for customer in mongo_db.customers_col.find({"id": rental.get("cust_id")}):
                cust_dict[customer["id"]] = {"id": customer["id"],
                                             "first_name": customer["first_name"],
                                             "last_name": customer["last_name"],
                                             "address": customer["address"],
                                             "phone_number": customer["phone_number"],
                                             "email": customer["email"]}
        return cust_dict


def drop_all_collections():
    """ Delete all collections in database """
    mongo = MongoDBConnection()
    with mongo:
        mongo_db = mongo.connection.media
        LOGGER.info("\n\nDropping all database collections")
        mongo_db.products_col.drop()
        mongo_db.customers_col.drop()
        mongo_db.rentals_col.drop()
