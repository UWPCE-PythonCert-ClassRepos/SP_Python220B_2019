"""Module to add furniture data to a MongoDB database."""

#pylint: disable=too-many-statements
#pylint: disable=invalid-name
#pylint: disable=too-many-locals

import logging
import csv
import os
from pymongo import errors as pyerror
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

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

def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Take three *.csv files as input and populate a new MongoDB database.

    params:
    directory name: name of Database
    product_file: file with product data
    customer_file: file with customer data
    retnals_file: file wit rental data

    return:
    record_count = tuple with counts of products, customers, and rentals added
    fail_count = tuple with counts of failed adds of products, customers, and rentals.
    """
    # Variables for counting the number of errors raised when importing data.
    error_prod, error_cust, error_rentals = 0, 0, 0
    product_file_path = os.path.join(directory_name, product_file)
    customer_file_path = os.path.join(directory_name, customer_file)
    rentals_file_path = os.path.join(directory_name, rentals_file)

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton
        # A collection of products in the database.
        products = db['products']
        # A collection of customers in the database.
        customers = db['customers']
        # A collection of rentals in the database.
        rentals = db['rentals']

        # Import product data file into database.
        try:
            with open(product_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    prod_add = {'product_id': row['product_id'],
                                'description': row['description'],
                                'product_type': row['product_type'],
                                'quantity_available': row['quantity_available']}
                    try:
                        products.insert_one(prod_add)
                        LOGGER.info('Added product to the database.')
                    except pyerror.DuplicateKeyError as error:
                        LOGGER.info(error)
                        LOGGER.info('Error adding product to database.')
                        error_prod += 1
        except FileNotFoundError:
            LOGGER.info('Product file not found')
            error_prod += 1

        # Import customer data file into database.
        try:
            with open(customer_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cust_add = {'user_id': row['user_id'],
                                'name': row['name'],
                                'address': row['address'],
                                'phone_number': row['phone_number'],
                                'email': row['email']}
                    try:
                        customers.insert_one(cust_add)
                        LOGGER.info('Added customer to the database.')
                    except pyerror.DuplicateKeyError as error:
                        LOGGER.info(error)
                        LOGGER.info('Error adding customer to the database.')
                        error_cust += 1
        except FileNotFoundError:
            LOGGER.info('Customer file not found')
            error_cust += 1

        # Import rental data file into database.
        try:
            with open(rentals_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rental_add = {'product_id': row['product_id'],
                                  'user_id': row['user_id']}
                    try:
                        rentals.insert_one(rental_add)
                        LOGGER.info('Added rental to the database.')
                    except pyerror.DuplicateKeyError as error:
                        LOGGER.info(error)
                        LOGGER.info('Error adding rental to database.')
                        error_rentals += 1
        except FileNotFoundError:
            LOGGER.info('Rental file not found')
            error_rentals += 1

        record_count = (products.count_documents({}), customers.count_documents({}),
                        rentals.count_documents({}))
        total_errors = (error_prod, error_cust, error_rentals)

        return record_count, total_errors

def show_available_products():
    """
    Return a python dictionary of products listed available based on a
    field 'quantity availalble' that stores an integrer count of
    products available.
    """
    mongo = MongoDBConnection()
    avail_prod = {}
    with mongo:
        db = mongo.connection.hp_norton
        for prod in db.products.find({'quantity_available': {'$gt': '0'}}):
            prod_info = {'description': prod['description'],
                         'product_type': prod['product_type'],
                         'quantity_available': prod['quantity_available']}
            avail_prod[prod['product_id']] = prod_info

    return avail_prod

def show_rentals(product_id):
    """
    Return a dictionary with user information from users that have
    rented products matching the product_id.
    """
    mongo = MongoDBConnection()
    rental_list = {}
    with mongo:
        db = mongo.connection.hp_norton
        for cust in db.rentals.find({'product_id': product_id}):
            for person in db.customers.find({'user_id': cust['user_id']}):
                entry = {'name': person['name'],
                         'address': person['address'],
                         'phone_number': person['phone_number'],
                         'email': person['email']}
                rental_list[person['user_id']] = entry

    return rental_list

def drop_all():
    """Clear all collections in database"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton
        LOGGER.info('Clearing database...')
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()
        LOGGER.info('Database Clear')
