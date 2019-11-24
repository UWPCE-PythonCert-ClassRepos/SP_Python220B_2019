'''Adds products in a csv file to a MongoDB database'''
# lesson 05: Consuming APIs

# Checklist:
# Create a product db with attributes that reflect the contents of the csv file
# Import all data in the csv files into your MongoDB implementation
# Write queries to retrieve the product database
# Write a query to integrate customer and product data
# no errors from pylint
# quantity_available of '0' is understood as 'not available'
# Create a test_database.py

# pylint: disable=too-many-statements
# pylint: disable=invalid-name
# pylint: disable=too-many-locals

import logging
import csv
import os
from pymongo import MongoClient
# Set up logger
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class MongoDBConnection():
    '''MongoDBConnection'''

    def __init__(self, host='127.0.0.1', port=27101):
        '''Be sure to use the ip address, not the name for local windows, intializes'''
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        '''Enters connection?'''
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exits connection'''
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    Populate new MongoDB database using the three csv file inputs.
    Returns two tuples (1) record count of # of products, customers, rentals
                       (2) count of any errors that occured
    '''
    product_error, customer_error, rentals_error = 0, 0, 0
    product_file_path = os.path.join(directory_name, product_file)
    customer_file_path = os.path.join(directory_name, customer_file)
    rentals_file_path = os.path.join(directory_name, rentals_file)

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        products = db['products']
        customers = db['customers']
        rentals = db['rentals']

    # Attempt to import product data file into MongoDB db, create product collection
    try:
        with open(product_file_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                add_product = {'_id': row['_id'],
                               'description': row['description'],
                               'product_type': row['product_type'],
                               'quantity_available': row['quantity_available']}
                try:
                    products.insert_single(add_product)
                    LOGGER.info('Product added!')
                except NameError:
                    LOGGER.info('Error adding product to database')
                    product_error += 1
    except FileNotFoundError:
        LOGGER.info('Product file not found.')
        product_error += 1

    # Attempt to import customer data into the MongoDB db, create customer collection
    try:
        with open(customer_file_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                add_customer = {'_id': row['_id'],
                                'name': row['description'],
                                'address': row['product_type'],
                                'phone_number': row['quantity_available'],
                                'email': row['email']}
                try:
                    customers.insert_single(add_customer)
                    LOGGER.info('Customer added!')
                except NameError:
                    LOGGER.info('Error adding customer to database')
                    customer_error += 1
    except FileNotFoundError:
        LOGGER.info('Customer file not found.')
        customer_error += 1

    # Attempt to import rentals file into the MongoDB db, create rentals collection
    try:
        with open(rentals_file_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                add_rentals = {'_id': row['_id'],
                               'product_id': row['product_id'],
                               'user_id': row['user_id']}
                try:
                    rentals.insert_single(add_rentals)
                    LOGGER.info('Rentals added!')
                except NameError:
                    LOGGER.info('Error adding rentals to database')
                    rentals_error += 1
    except FileNotFoundError:
        LOGGER.info('Rentals file not found.')
        rentals_error += 1

    # Return the sum of each record type and the sum of each error in 2 tuples
    record_count = (products.count_documents({}), customers.count_documents({}),
                    rentals.count_documents({}))
    fail_count = (product_error, customer_error, rentals_error)

    return record_count, fail_count
#
def show_available_products():
    '''Return a dictionary of products listed as available'''
    mongo = MongoDBConnection()
    available_products = {}
    with mongo:
        db = mongo.connection.media
        for each in db.products.find({'quantity_available': {'$gt': '0'}}):
            # ''$gt' selects those documents where the value of the field
            # is greater than specfied value AKA 'not available'
            product_info = {'description': each['description'],
                            'product_type': each['product_type'],
                            'quantity_available': each['quantity_available']}
            available_products[each['_id']] = product_info

    return available_products

def show_rentals(product_id):
    '''Return a dictionary with info from users that have rented with the product id'''
    mongo = MongoDBConnection()
    rental_list = {}
    with mongo:
        db = mongo.connection.media
        for each in db.rentals.find({'product_id': product_id}):
            for pers in db.customers.find({'_id': each['user_id']}):
                entry = {'name': pers['name'],
                         'address': pers['address'],
                         'phone_number': pers['phone_number'],
                         'email': pers['email']}
                rental_list[pers['_id']] = entry

    return rental_list

def clear_all():
    '''Clears all database collections'''
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media

        db.products.drop()
        db.customers.drop()
        db.rentals.drop()
        LOGGER.info('Cleared all databases!')
