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
        JSON formatted string representation of CSV file contents.
        Each string is a series of key/values pairs representing a row from
        the csv file (key = csv column header, value = row value)
    '''
    try:
        LOGGER.info(f'Reading file \'{csv_file}\'')
        with open(csv_file) as f:
            json_list = [json.loads(json.dumps(row)) for row in csv.DictReader(f)]
    except FileNotFoundError:
        LOGGER.error(f'{csv_file} not found. Check file path and/or name.')
        sys.exit()
    except IOError:
        LOGGER.error(f'Could not read {csv_file}, check file permissions.')
        sys.exit()
    return json_list

def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    This function takes a directory name three csv files as input, one with
    product data, one with customer data and the third one with rentals data
    and creates and populates a new MongoDB database with these data. It
    returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a
    count of any errors that occurred, in the same order.
    '''

    product_json = import_csv_to_json(os.path.join(directory_name, product_file))
    customer_json = import_csv_to_json(os.path.join(directory_name, customer_file))
    rental_json = import_csv_to_json(os.path.join(directory_name, rentals_file))

    print(product_json)
    print(customer_json)
    print(rental_json)

    # Create mongo database connection
    mongo = MongoDBConnection()

    try:
        with mongo:
            pass
    except ConnectionFailure as CF: # MongoDB connection issue
        pass

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
