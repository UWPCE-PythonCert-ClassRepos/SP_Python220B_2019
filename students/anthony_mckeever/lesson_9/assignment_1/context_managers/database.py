# Advanced Programming In Python - Lesson 9 Assignment 1.2: Context Managers
# RedMine Issue - SchoolOps-15
# Code Poet: Anthony McKeever
# Start Date: 01/22/2019
# End Date: 01/23/2019

"""
Customer and Product Database Helper

Helps connect to and read content from the Customer and Product NoSQL databases
"""

import csv
import logging
import os.path

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


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


class HPNorton(MongoDBConnection):
    """
    Context Managing class for the HP_Norton database using a MongoDBConnection
    """

    def __init__(self):
        super().__init__()
        self.database = None

    def __enter__(self):
        super().__enter__()
        self.database = self.connection.hp_norton
        return self

    def get_collection(self, collection):
        """
        Return a collection from the database.

        :collection:    The collection to acquire
        """
        return self.database[collection]


def format_row_integers(row):
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


def ingest_file(db_collection, directory, file_name):
    """
    Ingests a file into the MongoDB collection.
    Return how many errors was encounterd and how many documents the collection
    has.

    :database:      The MongoDB database.
    :directory:     The directory of the input CSV file.
    :file_name:     The name of the input CSV file.
    :collection:    The name of the collection to ingest the file to.
    """
    file_path = os.path.join(directory, file_name)
    errors = 0

    try:
        LOGGER.info("Attempting to ingest %s", file_name)
        with open(file_path) as open_file:
            contents = csv.DictReader(open_file)

            for row in contents:
                try:
                    row = format_row_integers(row)
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

    LOGGER.debug("Encountered %d errors while importing %s", errors, file_name)

    return errors, db_collection.count()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Imports CSV files into the MongoDB database.

    :directory_name:    The directory of the CSV files.
    :product_file:      The name of the CSV file containing products.
    :customer_file:     The name of the CSV file containing customers.
    :rentals_file:      The name of the CSV file containing rentals.
    """
    hp_norton = HPNorton()

    collections = {"products": product_file,
                   "customers": customer_file,
                   "rentals": rentals_file}

    counts = {"products": {"errors": 0, "count": 0},
              "customers": {"errors": 0, "count": 0},
              "rentals": {"errors": 0, "count": 0}}

    with hp_norton as database:
        for collection_name, csv_file in collections.items():
            LOGGER.info("Importing %s...", collection_name)
            collect = database.get_collection(collection_name)
            errors, count = ingest_file(collect, directory_name, csv_file)

            counts[collection_name]["errors"] = errors
            counts[collection_name]["count"] = count

    records = (counts["products"]["count"],
               counts["customers"]["count"],
               counts["rentals"]["count"])
    errors = (counts["products"]["errors"],
              counts["customers"]["errors"],
              counts["rentals"]["errors"])
    return records, errors


def show_available_products():
    """
    Return a dictionary of available products with the product_id as the key.

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
    hp_norton = HPNorton()
    query = {"quantity_available": {"$gt": 0}}
    available_products = {}

    LOGGER.info("Gathering available products.")
    LOGGER.debug("Products query: \"%s\"", query)

    with hp_norton as database:
        products_collection = database.get_collection("products")
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


def show_rentals(product_id):
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
    hp_norton = HPNorton()
    query = {"product_id": product_id}
    renting_customers = {}

    LOGGER.info("Gathering rentals for %s.", product_id)
    LOGGER.debug("Rentals query: \"%s\"", query)

    with hp_norton as database:
        customer_collection = database.get_collection("customers")
        rental_collection = database.get_collection("rentals")
        rentals = rental_collection.find(query)

        LOGGER.info("Found %d rentals for product.", rentals.count(False))
        for rental in rentals:
            # Do not log customers to prevent exposure of PII to unauthorized
            # users or developers.
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
