'''Imports csv file to MongoDb'''

import csv
import os
import logging
import datetime
from pymongo import MongoClient
from pymongo import errors as pyerror

# Though rentals wasn't required as an output, it also wasn't removed as an input arg
# pylint disabled: W0612 :51 Unused variable 'rent_tuple' (unused-variable)

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

    def __enter__(self):
        '''Connects to the database client'''
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exits the connection'''
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    This function takes a directory name three csv files as input (product data,
    customer data, and rentals data). It returns 2 tuples with the number of records
    processed, the initial records count, the final records count, and the elapse time
    each file (product, customer).
    '''
    LOGGER.debug('Importing csv file')
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton

         # Create collections
        products = database[product_file]
        customers = database[customer_file]
        rentals = database[rentals_file]

        prod_tuple = import_csv(directory_name, product_file, products)
        cust_tuple = import_csv(directory_name, customer_file, customers)
        rent_tuple = import_csv(directory_name, rentals_file, rentals)

    return prod_tuple, cust_tuple

def import_csv(directory_name, file_name, database):
    '''Returns the number of files processed, start count, end count, elapse time'''
    LOGGER.debug('Importing %s', file_name)
    start_time = datetime.datetime.now()
    start_count = database.count_documents({})
    try:
        file_csv = f'{file_name}.csv'
        with open(os.path.join(directory_name, file_csv)) as file:
            len(database.insert_many(csv.DictReader(file)).inserted_ids)
    except (pyerror.InvalidOperation, FileNotFoundError) as error:
        LOGGER.warning('Oops! something went wrong while reading %s: %s', file_csv, error)

    end_count = database.count_documents({})
    elapse_time = datetime.datetime.now().timestamp() - start_time.timestamp()

    return end_count - start_count, start_count, end_count, elapse_time

def show_available_products():
    '''Returns a Python dictionary of products listed as available'''
    results = {}
    mongo = MongoDBConnection()
    with mongo:
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
    mongo = MongoDBConnection()
    with mongo:
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

def drop_all():
    '''Clears database from Memory'''
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        database.products.drop()
        database.customers.drop()
        database.rentals.drop()
        LOGGER.info('Databases Cleared')
