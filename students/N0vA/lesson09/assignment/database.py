"""
This file creates and manipulates the database for HP Norton
"""
# pylint:disable=logging-format-interpolation
# pylint:disable=invalid-name
# pylint:disable=too-many-locals

import csv
import logging
import os
from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
LOG_FILE = 'db_logger'

FORMATTER = logging.Formatter(LOG_FORMAT)

# File handler set up
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

# Console handler set up
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

# Get logger
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


class MongoDBConnection():
    """Setup for MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """Initialize MongoDB Database"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            LOGGER.warning(f'Exception type: {exc_type}')
            LOGGER.warning(f'Exception value: {exc_val}')
            LOGGER.warning(f'Exception traceback: {exc_tb}')
        self.connection.close()

def read_data(csv_file):
    """Reads csv file and creates list of dictionaries."""

    new_data = []

    with open(csv_file) as input_file:
        reader = csv.reader(input_file)
        header = next(reader)

        for row in reader:
            temp = dict(zip(header[:], row[:]))
            new_data.append(temp)

    return new_data

def import_data(directory_name, product_file, customer_file, rental_file):
    """Reads in data from a given directory and set of 3 input files for products,
    customers, and rentals in that order."""

    LOGGER.info('Importing data...')
    # Prep input data - filepaths
    product_path = os.path.join(directory_name, product_file)
    customer_path = os.path.join(directory_name, customer_file)
    rental_path = os.path.join(directory_name, rental_file)

    client = MongoDBConnection()

    with client:
        db = client.connection.hp_norton

        # Create and open tables for database
        products = db['products']
        customers = db['customers']
        rentals = db['rentals']

        # Setup for counts
        products_added = 0
        customers_added = 0
        rentals_added = 0
        customer_errors = 0
        product_errors = 0
        rental_errors = 0

        # Import product file
        try:
            product_data = read_data(product_path)
            products.insert_many(product_data)
            products_added += len(product_data)
        except FileNotFoundError as e:
            LOGGER.error(e)
            product_errors += 1

        #   Import customer file
        try:
            customer_data = read_data(customer_path)
            customers.insert_many(customer_data)
            customers_added += len(customer_data)
        except FileNotFoundError as e:
            LOGGER.error(e)
            customer_errors += 1

        #   Import rental file
        try:
            rental_data = read_data(rental_path)
            rentals.insert_many(rental_data)
            rentals_added += len(rental_data)
        except FileNotFoundError as e:
            LOGGER.error(e)
            rental_errors += 1

        # Create tuples for output of function
        input_counts = (products_added, customers_added, rentals_added)
        error_counts = (product_errors, customer_errors, rental_errors)

    LOGGER.debug('Data upload complete.')
    return input_counts, error_counts

def show_available_products():
    """Returns a python dictionary of product availability."""

    # Connect to database
    client = MongoDBConnection()
    with client:

        LOGGER.info('Find available products...')
        db = client.connection.hp_norton
        query = db['products']

        # Dictionary output
        available_products = {}

        # Iterate through products for dictionary
        for product in query.find():
            available_products[product['product_id']] = {
                'description': product['description'],
                'product_type': product['product_type'],
                'quantity_available': product['quantity_available']}

        return available_products

def show_rentals():
    """Returns a python dictionary for users that have rented products."""

    # Dictionary output
    rentals_available = {}

    # Connect to database
    client = MongoDBConnection()
    with client:
        db = client.connection.hp_norton

        LOGGER.debug('Querying rentals...')
        rentals = db['rentals']
        customers = db['customers']
        renters = []

        # Get list of customer ids who have rented products
        for rental in rentals.find():
            renters.append(rental['user_id'])

        # Get customer information for each person in renters list
        for renter in renters:
            for per in customers.find({'user_id': renter}):
                rentals_available[per['user_id']] = {'name': per['name'],
                                                     'address': per['address'],
                                                     'phone_number': per['phone_number'],
                                                     'email': per['email']}
        return rentals_available

def clear_database():
    """Clear database of existing data."""

    client = MongoDBConnection()
    with client:
        db = client.connection.hp_norton

        # Drop tables
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()

    LOGGER.info('Database all cleared.')
