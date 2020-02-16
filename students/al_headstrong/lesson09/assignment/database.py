"""Module to enter and view data in Mongo."""

# pylint: disable = invalid-name, too-many-locals

import logging
import os
import pandas as pd
from pymongo import MongoClient


def MongoLoggerConfigure(level):
    """Configure mongo context logger."""

    level_dict = {'0': logging.CRITICAL,
                  '1': logging.ERROR,
                  '2': logging.WARNING,
                  '3': logging.DEBUG}

    log_format = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'

    formatter = logging.Formatter(log_format)

    log_file = 'db.log'

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(level_dict[level])

    return logger


class MongoDBConnection:
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017, logging_level=1):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        self.logger = MongoLoggerConfigure(logging_level)

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        self.logger.info('Connecting to Mongo with host: %s and port: %s.', self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info('Closing connection to Mongo.')
        if exc_type:
            self.logger.info('exc_type: %s', exc_type)
            self.logger.info('exc_val: %s', exc_val)
            self.logger.info('exc_tb: %s', exc_tb)
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

            try:
                data, count = import_csv(directory_name, file_name)
                database.insert_many(data)
                count_error = 0

            except FileNotFoundError as error:
                mongo.logger.error('Error %s loading %s.', error, file_name)
                count_error = 1
                count = 0

            input_count.append(count)
            error_count.append(count_error)

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
        for rental in rentals.find({'product_id': product_id}):
            for customer in customers.find({'customer_id': rental['customer_id']}):
                renters[customer['customer_id']] = {
                    'name': customer['name'],
                    'address': customer['address'],
                    'phone_number': customer['phone_number'],
                    'email': customer['email']
                }
        return renters


def clear_database():
    """Delete database."""
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        db['products'].drop()
        db['customers'].drop()
        db['rentals'].drop()
