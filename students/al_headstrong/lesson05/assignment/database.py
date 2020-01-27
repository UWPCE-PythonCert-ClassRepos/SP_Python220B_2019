"""
Module to establish mongo database, add and view data.
"""
# pylint: disable=invalid-name

import logging
import os
from pymongo import MongoClient
import pandas as pd

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'

FORMATTER = logging.Formatter(LOG_FORMAT)

LOG_FILE = 'db.log'

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


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


def import_csv(directory, file):
    """Read csv file in directory into data frame, then return list of dicts and dict count."""
    df = pd.read_csv(os.path.join(os.path.abspath(directory), file))
    return df.to_dict('records'), df.shape[0]


def import_data(directory_name, product_file, customer_file, rentals_file):
    """Add three files at directory to mongo db and return tuples of items added and errors."""
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        files = (product_file, customer_file, rentals_file)
        databases = (db['products'], db['customers'], db['rentals'])
        input_count = []
        error_count = []

        for file_name, database in zip(files, databases):
            LOGGER.debug('Attempting to load %s.', file_name)
            try:
                data, count = import_csv(directory_name, file_name)
                database.insert_many(data)
                error_count.append(0)
                LOGGER.debug('Successful addition to %s.', database)

            except FileNotFoundError as error:
                LOGGER.error('Error %s loading %s.', error, file_name)
                error_count.append(1)
                count = 0

            input_count.append(count)

        return tuple(input_count), tuple(error_count)


def show_available_products():
    """Return dict of dicts showing available products."""
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        products = db['products']
        available_products = {}
        for product in products.find():
            if product["quantity_available"] > 0:
                available_products[product['product_id']] = {
                    'description': product['description'],
                    'product_type': product['product_type'],
                    'quantity_available': product['quantity_available']
                }
        return available_products


def show_rentals(product_id):
    """Return dict of dicts showing the customers renting the product with product_id argument."""
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        rentals = db['rentals']
        customers = db['customers']
        renters = {}
        rentals_found = rentals.find({'product_id': product_id})
        if rentals_found:
            for rental in rentals_found:
                if not rental:
                    LOGGER.warning('Product ')
                for customer in customers.find({'customer_id': rental['customer_id']}):
                    renters[customer['customer_id']] = {
                        'name': customer['name'],
                        'address': customer['address'],
                        'phone_number': customer['phone_number'],
                        'email': customer['email']
                    }
        else:
            LOGGER.warning('Product not found in database.')
        return renters


def clear_database():
    """Delete database."""
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        db['products'].drop()
        db['customers'].drop()
        db['rentals'].drop()
        LOGGER.debug('Cleared database.')
