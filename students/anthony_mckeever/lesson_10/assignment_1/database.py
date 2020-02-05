# Advanced Programming In Python - Lesson 10 Assignment 1: Meta Programming
# RedMine Issue - SchoolOps-20
# Code Poet: Anthony McKeever
# Start Date: 01/30/2020
# End Date: 01/30/2020

"""
Customer and Product Database Helper

Helps connect to and read content from the Customer and Product NoSQL databases
"""

import csv
import logging
import os.path
import time
import types

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# pylint: disable=no-self-use


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        LOGGER.info("Connecting to MongoDB at %s on port %d.",
                    self.host, self.port)
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        LOGGER.info("Closing connection.")
        self.connection.close()


class MetaTimer(type):
    """
    A Metaclass that provides a timing closure for all functions of a class.
    """

    def __new__(cls, name, bases, attrs):
        """
        Wraps all functions of a given class into the timer_function method.

        :cls:       This class.
        :name:      The name of the inheriting class.
        :bases:     The base classes.
        :attrs:     The attributes of the inheriting class.
        """
        for attr, func in attrs.items():
            if isinstance(func, types.FunctionType):
                attrs[attr] = cls.timer_function(func)

        return super(MetaTimer, cls).__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        """
        Sets up the class upon call.
        """
        return type.__call__(cls, *args)

    @classmethod
    def timer_function(cls, func):
        """
        A closure for the temporal logger function.  The temporal_logger
        handles logging a function when it is called.

        :self:  This class.
        :func:  The function to wrap in the logging function
        """
        def temporal_logger(*args, **kwargs):
            """
            Return the return value of func(*args, **kwargs).
            Write the time it took to run a method to the LOGGER.info output.

            :*args:     The arguments of the wrapped function.
            :**kwargs:  The keyword arguments of the wrapped function.
            """
            LOGGER.info("Enter Function: %s", func.__name__)

            start_time = time.time()
            return_val = func(*args, **kwargs)
            end_time = time.time() - start_time

            LOGGER.info("Exit Function: %s", func.__name__)

            msg = str(f"Function: {func.__name__} - " +
                      f"Execution time: {end_time} seconds.")
            LOGGER.info(msg)
            return return_val

        return temporal_logger


class DatabaseHandler(metaclass=MetaTimer):
    """
    A class that handles calls to the database.
    """

    def format_row_integers(self, row):
        """
        Formats all integer fields in a row from strings to integers

        :row:   The CSV row to modify
        """

        for key, value in row.items():
            if value.isdigit():
                msg = f"Converting string {value} to integer"
                LOGGER.debug(msg)
                row[key] = int(value)

        return row

    def ingest_file(self, database, directory, file_name, collection):
        """
        Ingests a file into the MongoDB collection.
        Return how many errors was encounterd and how many documents the
        collection has.

        :database:      The MongoDB database.
        :directory:     The directory of the input CSV file.
        :file_name:     The name of the input CSV file.
        :collection:    The name of the collection to ingest the file to.
        """
        file_path = os.path.join(directory, file_name)
        db_collection = database[collection]
        errors = 0

        try:
            LOGGER.info("Attempting to ingest %s", file_name)
            with open(file_path) as open_file:
                contents = csv.DictReader(open_file)

                for row in contents:
                    try:
                        row = self.format_row_integers(row)
                        LOGGER.debug("Inserting one record: %s", row)
                        db_collection.insert_one(row)

                    except DuplicateKeyError as dupe_key:
                        LOGGER.info("Unable to insert row.")
                        LOGGER.error(dupe_key)
                        errors += 1

                LOGGER.info("File ingestion complete.")

        except FileNotFoundError as file_not_found:
            LOGGER.info("File %s was not found.", file_name)
            LOGGER.error(file_not_found)
            errors += 1

        LOGGER.debug("Encountered %d errors while importing %s",
                     errors,
                     file_name)

        return errors, db_collection.count()

    def import_data(self, directory_name, product_file,
                    customer_file, rentals_file):
        """
        Imports CSV files into the MongoDB database.

        :directory_name:    The directory of the CSV files.
        :product_file:      The name of the CSV file containing products.
        :customer_file:     The name of the CSV file containing customers.
        :rentals_file:      The name of the CSV file containing rentals.
        """
        mongo = MongoDBConnection()

        product_errors, customer_errors, rentals_errors = 0, 0, 0
        products, customers, rentals = 0, 0, 0

        with mongo:
            database = mongo.connection.hp_norton

            LOGGER.info("Importing products...")
            product_errors, products = self.ingest_file(database,
                                                        directory_name,
                                                        product_file,
                                                        "products")

            LOGGER.info("Importing customers...")
            customer_errors, customers = self.ingest_file(database,
                                                          directory_name,
                                                          customer_file,
                                                          "customers")

            LOGGER.info("Importing rentals...")
            rentals_errors, rentals = self.ingest_file(database,
                                                       directory_name,
                                                       rentals_file,
                                                       "rentals")

        records = (products, customers, rentals)
        errors = (product_errors, customer_errors, rentals_errors)
        return records, errors

    def show_available_products(self):
        """
        Return a dictionary of available products with the product_id
        as the key.

        Return Format:
        {
            product_id:
            {
                product_type: value,
                description: value,
                quantity_available: value
            }
        }
        """
        mongo = MongoDBConnection()
        query = {"quantity_available": {"$gt": 0}}
        available_products = {}

        LOGGER.info("Gathering available products.")
        LOGGER.debug("Products query: \"%s\"", query)

        with mongo:
            products_collection = mongo.connection.hp_norton["products"]
            products = products_collection.find(query)

            LOGGER.info("Found %d available products.", products.count(False))
            for product in products:
                prod_key = None
                prod_detail = {}

                for key, value in product.items():
                    if key == "_id":
                        prod_key = value
                    else:
                        prod_detail[key] = value

                available_products[prod_key] = prod_detail

        return available_products

    def show_rentals(self, product_id):
        """
        Return a dictionary of customers renting a specific product.

        Return Format:
        {
            customer_id:
            {
                name: value,
                address: value,
                phone_number: value,
                email_address: value
            }
        }

        :product_id:    The product to query.
        """
        mongo = MongoDBConnection()
        query = {"product_id": product_id}
        renting_customers = {}

        LOGGER.info("Gathering rentals for %s.", product_id)
        LOGGER.debug("Rentals query: \"%s\"", query)

        with mongo:
            customer_collection = mongo.connection.hp_norton["customers"]
            rental_collection = mongo.connection.hp_norton["rentals"]
            rentals = rental_collection.find(query)

            LOGGER.info("Found %d rentals for product.", rentals.count(False))
            for rental in rentals:
                # Do not log customers to prevent exposure of PII
                # to unauthorized users or developers.
                customer_id = rental["customer_id"]
                customer_query = {"_id": customer_id}
                customer = customer_collection.find_one(customer_query)
                customer_detail = {}

                for key, value in customer.items():
                    if key == "_id":
                        continue

                    customer_detail[key] = value

                renting_customers[customer_id] = customer_detail

        return renting_customers
