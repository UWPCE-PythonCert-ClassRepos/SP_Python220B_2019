'''
This file contains functions for converting CSV data to a MongoDB database
'''
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import sys
import csv
import json
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
FORMATTER = logging.Formatter(LOG_FORMAT)

# Create log file for warning and error messages
LOG_FILE = 'db.log'
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)
# Add handlers to logger
LOGGER.addHandler(FILE_HANDLER)

class MongoDBConnection(object):
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

def import_csv_to_json(csv_file):
    '''
    Method to convert a csv file to a JSON string object

    Args:
        csv_file (string):
            CSV file to read

    Returns:
        json_list (JSON):
            JSON formatted string representation of CSV file contents.
            Each string is a series of key/values pairs representing a row
            from the csv file (key = csv column header, value = row value)
        errors (int):
            Number of errors encountered during CSV read
    '''
    json_list = []
    errors = 0
    try:
        LOGGER.info(f'Reading file \'{csv_file}\'')
        with open(csv_file) as f:
            json_list = [json.loads(json.dumps(row)) for row in csv.DictReader(f)]
    except FileNotFoundError:
        LOGGER.error(f'{csv_file} not found. Check file path and/or name.')
        errors += 1
    except IOError:
        LOGGER.error(f'Could not read {csv_file}, check file permissions.')
        errors += 1
    return json_list, errors

def add_json_to_mongodb(json_data, db_name):
    '''
    Method to add JSON formatted data to a mongo database

    Args:
        json_data (JSON):
            A list of JSON formatted data
        db_name (str):
            Mongo database name

    Returns:
        collection_count (int):
            Count of documents added to the database
        error_count (int):
            Count of errors generated during document add
    '''
    # Create mongo database connection
    mongo = MongoDBConnection()

    errors = 0
    try:
        with mongo:
            LOGGER.info('Creating mongo connection')
            db = mongo.connection.HPNorton
            LOGGER.info(f'Creating {db_name} database and adding records')
            new_db = db[db_name]
            new_db.insert_many(json_data)
    except ConnectionFailure as CF: # MongoDB connection issue
        LOGGER.error('Could not connect to MongoDB database.')
        LOGGER.error(f'Error message: {CF}')
        errors += 1

    collection_count = new_db.estimated_document_count()

    return collection_count, errors

def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    Method to import CSV data and add to a mongo database

    Args:
        directory_name (str):
            Directory where CSV files are located
            Pass empty string if files in current directory
        product_file (str):
            Name of CSV file containing product data
        customer_file (str):
            Name of CSV file containing customer data
        rentals_file (str):
            Name of CSV file containing rentals data

    Returns:
        counts (tuple):
            Count of documents added for the product, customer, and rentals
            database, in that order
        errors (tuple):
            Count of errors encountered while adding documents for the product,
            customer, and rentals database, in that order
    '''

    # Convert csv files to JSON data
    product_json, product_csv_errors = import_csv_to_json(os.path.join(directory_name, product_file))
    customer_json, customer_errors = import_csv_to_json(os.path.join(directory_name, customer_file))
    rentals_json, rentals_errors = import_csv_to_json(os.path.join(directory_name, rentals_file))

    # Add JSON data to mongo database
    product_count, product_db_errors = add_json_to_mongodb(product_json, 'product')
    customer_count, customer_db_errors = add_json_to_mongodb(customer_json, 'customer')
    rentals_count, rentals_db_errors = add_json_to_mongodb(rentals_json, 'rentals')

    counts = (product_count, customer_count, rentals_count)
    errors = (product_csv_errors + product_db_errors,
              customer_errors + customer_db_errors,
              rentals_errors + rentals_db_errors)

    return counts, errors

def show_available_products():
    '''
    Returns a Python dictionary of products listed as available with the following fields:
        product_id.
        description.
        product_type.
        quantity_available.

        {
        ‘prd001’:
            {‘description’:‘60-inch TV stand’,
            ’product_type’:’livingroom’,
            ’quantity_available’:‘3’},
        ’prd002’:
            {‘description’:’L-shaped sofa’,
            ’product_type’:’livingroom’,
            ’quantity_available’:‘1’}
        }
    '''
    pass

def show_rentals(product_id):
    '''
    Returns a Python dictionary with the following user information from users that have rented products matching product_id:
        user_id.
        name.
        address.
        phone_number.
        email.

        {
        ‘user001’:
            {‘name’:’Elisa Miles’,
            ’address’:‘4490 Union Street’,
            ’phone_number’:‘206-922-0882’,
            ’email’:’elisa.miles@yahoo.com’},
        ’user002’:
            {‘name’:’Maya Data’,
            ’address’:‘4936 Elliot Avenue’,
            ’phone_number’:‘206-777-1927’,
            ’email’:’mdata@uw.edu’}}
    '''
    pass
