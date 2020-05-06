'''Imports csv file to MongoDb'''

import csv
import os
import logging
from pymongo import MongoClient
from pymongo import errors as pyerror

logging.basicConfig(filename="db.log", filemode="w", level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class MongoDBConnection():
    '''MongoDB Connection'''
    def __init__(self, host='127.0.0.1', port=27017):
        '''Initiates the connection protocol'''
        self.host = host
        self.port = port
        self.connection = None
        LOGGER.info('MongoDBConnection.__init__ Host: %s Port: %s', host, port)

    def __enter__(self):
        '''Connects to the database client'''
        self.connection = MongoClient(self.host, self.port)
        LOGGER.info('MongoDBConnection.__enter__ Database: %s',
                    self.connection.list_database_names())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exits the connection'''
        self.connection.close()
        LOGGER.info('MongoDBConnection.__exit__ Connection Closed')

def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    This function takes a directory name three csv files as input (product data,
    customer data, and rentals data). It returns 2 tuples with a record count of the
    number of data and errors for each file (product, customer, rentals).
    '''
    LOGGER.debug('Importing csv file')
    with MongoDBConnection() as mongo:
        database = mongo.connection.hp_norton
        database[product_file].drop()
        database[customer_file].drop()
        database[rentals_file].drop()

         # Create collections
        products = database[product_file]
        customers = database[customer_file]
        rentals = database[rentals_file]

        prod_count, prod_errors = import_csv(directory_name, product_file, products)
        cust_count, cust_errors = import_csv(directory_name, customer_file, customers)
        rent_count, rent_errors = import_csv(directory_name, rentals_file, rentals)
    return((prod_count, cust_count, rent_count), (prod_errors, cust_errors, rent_errors))

def import_csv(directory_name, file_name, database):
    '''
    Creates and populates a new MongoDB database with data,
    returns the number of files and errors
    '''
    LOGGER.debug('Importing %s', file_name)
    errors = 0
    count = 0
    try:
        file_csv = f'{file_name}.csv'
        with open(os.path.join(directory_name, file_csv)) as file:
            count = len(database.insert_many(csv.DictReader(file)).inserted_ids)
    except (pyerror.InvalidOperation, FileNotFoundError) as error:
        LOGGER.warning('Oops! something went wrong while reading %s: %s', file_csv, error)
        errors += 1
    return count, errors

def show_available_products():
    '''Returns a Python dictionary of products listed as available'''
    results = {}
    with MongoDBConnection() as mongo:
        database = mongo.connection.hp_norton
        LOGGER.info('Searching for available products')
        for product in database['products'].find({'quantity_available': {'$gt': '0'}}):
            results[product['product_id']] = {
                'description': product['description'],
                'product_type': product['product_type'],
                'quantity_available': product['quantity_available']}
    return results

def show_rentals(product_id):
    '''
    Returns a Python dictionary with the following user information from users that have
    rented products matching the product id
    '''
    results = {}
    with MongoDBConnection() as mongo:
        database = mongo.connection.hp_norton
        LOGGER.info('Searching for rental product_id: %s', product_id)
        for rental in database['rentals'].find({'product_id': product_id}):
            for customer in database['customers'].find({'user_id': rental['user_id']}):
                results[customer['user_id']] = {
                    'name': customer['name'],
                    'address': customer['address'],
                    'phone_number': customer['phone_number'],
                    'email': customer['email']}
        return results
