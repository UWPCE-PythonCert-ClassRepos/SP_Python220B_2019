"""Import and read customers, products and rentals databases from csv."""

# pylint: disable=W1202, W0621, C0103, R0914

import logging
import csv
import os
import time
from pymongo import MongoClient


# Set logging level at info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class MongoDBConnection():
    """Establish MongoDB connection."""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def csv_to_dict(path):
    """Converts data from csv to mongo-readable dict."""

    table_data = []

    # Get csv data and return as dict
    with open(path) as csv_file:
        for row in csv.DictReader(csv_file):
            table_data.append(row)

    logging.info(f"{path} converted from csv to mongo-readable dict.")

    return table_data


def import_data(directory_name, product_file, customer_file, rentals_file):
    """Import HP Norton csv data to MongoDB."""

    start_time = time.time()
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        # Create collections
        products = database['products']
        customers = database['customers']
        rentals = database['rentals']

        start_product_count = products.count_documents({})
        start_customer_count = customers.count_documents({})

        # Create iterable list for the for loop below
        collections = [{'db': products, 'file_name': product_file, 'order': 0},
                       {'db': customers, 'file_name': customer_file, 'order': 1},
                       {'db': rentals, 'file_name': rentals_file, 'order': 2}]

        for collection in collections:

            try:
                # Populate collections with csv data
                path = os.path.join(directory_name, collection['file_name'])
                data = csv_to_dict(path)
                collection['db'].insert_many(data)

                logging.info(f"Data from {path} added to database.")

            except FileNotFoundError as err:
                logging.error(err)

        final_product_count = products.count_documents({})
        final_customer_count = customers.count_documents({})

        run_time = time.time() - start_time

        products_tuple = (final_product_count - start_product_count,
                          start_product_count, final_product_count,
                          run_time)
        customers_tuple = (final_customer_count - start_customer_count,
                           start_customer_count, final_customer_count,
                           run_time)

        print(products_tuple, customers_tuple)
        return [products_tuple, customers_tuple]

def drop_data():
    """Clear data from the database."""

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media

    for name in ['customers', 'products', 'rentals']:
        database[name].drop()

    logging.info("All data has been cleared from the database.")

import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
