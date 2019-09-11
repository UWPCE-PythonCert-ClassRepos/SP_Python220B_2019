'''
This file contains functions for converting CSV data to a MongoDB database
The implementation is done in a linear fashion
'''
import os
import csv
import json
import logging
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

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

def drop_tables(tables):
    '''
    Drop selected tables from mongo DB

    Args:
        tables (list):
            List of table names to drop
    '''
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.HPNorton
        for table in tables:
            LOGGER.info('Dropping table {} from database'.format(table))
            db[table].drop()

def create_mongo_connection(host='127.0.0.1', port=27017):
    '''
    Method to create mongo DB connection, allows user to change host or port
    from default values
    '''
    return MongoDBConnection(host, port)

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
    start = time.time()
    LOGGER.info('Starting read of \'{}\''.format(csv_file))
    json_list = []
    try:
        with open(csv_file) as filex:
            json_list = [json.loads(json.dumps(row)) for row in csv.DictReader(filex)]
    except (FileNotFoundError, IOError) as ERR:
        LOGGER.error(f'Could not read {csv_file}. Check file existence and/or permissions.')
        LOGGER.error(f'Error message: {ERR}')
    end = time.time()
    LOGGER.info('Finishing read of \'{}\''.format(csv_file))
    return json_list, end-start

def add_json_to_mongodb(json_data, db_name, mongo=None):
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
    # Create mongo database connection if not provided
    start = time.time()
    if not mongo:
        mongo = create_mongo_connection()
    try:
        with mongo:
            LOGGER.info('Creating mongo connection')
            db = mongo.connection.HPNorton
            LOGGER.info(f'Creating {db_name} database and adding records')
            new_db = db[db_name]
            before_count = new_db.estimated_document_count()
            new_db.insert_many(json_data)
            collection_count = new_db.estimated_document_count()
    except (ConnectionFailure, ServerSelectionTimeoutError) as CF: # MongoDB connection issue
        LOGGER.error('Could not connect to MongoDB database.')
        LOGGER.error(f'Error message: {CF}')
        before_count = None
        collection_count = 0
    end = time.time()

    return before_count, collection_count, end-start

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
    product_json, product_csv_time = import_csv_to_json(
        os.path.join(directory_name, product_file))
    customer_json, customer_csv_time = import_csv_to_json(
        os.path.join(directory_name, customer_file))
    rentals_json, rentals_csv_time = import_csv_to_json(
        os.path.join(directory_name, rentals_file))

    # Add JSON data to mongo database
    product_count_before, product_count_after, product_db_time = \
    add_json_to_mongodb(product_json, 'products')
    customer_count_before, customer_count_after, customer_db_time = \
    add_json_to_mongodb(customer_json, 'customers')
    rentals_count_before, rentals_count_after, rentals_db_time = \
    add_json_to_mongodb(rentals_json, 'rentals')

    product_data = (len(product_json), product_count_before,
                    product_count_after, product_csv_time+product_db_time)
    customer_data = (len(customer_json), customer_count_before,
                     customer_count_after, customer_csv_time+customer_db_time)
    rentals_data = (len(rentals_json), rentals_count_before,
                    rentals_count_after, rentals_csv_time+rentals_db_time)

    return [product_data, customer_data, rentals_data]

def show_available_products(mongo=None):
    '''
    Method to return a nested python dictionary of available products. Products
    with a quantity_available value of 0 are considered not available

    Returns:
        product_dict (dict):
            Nested python dictionary with key = product_id,
            value = python dictionary with description, product_type, and
            quantity_available keys, and associated values from product database
    '''
    # Create mongo database connection
    if not mongo:
        mongo = create_mongo_connection()

    product_dict = {}
    try:
        with mongo:
            LOGGER.info('Creating mongo connection')
            db = mongo.connection.HPNorton
            LOGGER.info(f'Querying product database for available products')
            # Filter query to return products with non-zero quanitity
            query = db['product'].find({'quantity_available': {'$ne':'0'}})
            for item in query:
                # Populate product dictionary
                product_dict[item['product_id']] = {'description':
                                                    item['description'],
                                                    'product_type':
                                                    item['product_type'],
                                                    'quantity_available':
                                                    item['quantity_available']}
    except (ConnectionFailure, ServerSelectionTimeoutError) as CF: # MongoDB connection issue
        LOGGER.error('Could not connect to MongoDB database.')
        LOGGER.error(f'Error message: {CF}')

    return product_dict

def show_rentals(product_id, mongo=None):
    '''
    Method to return data for customers that have rented products matching product_id

    Args:
        product_id (str):
            Product ID of interest

    Returns:
        rentals_dict (dict):
            Nested python dictionary with key = customer_id,
            value = python dictionary with name, address, phone_number and
            email keys, and associated values from customer database
    '''
    # Create mongo database connection
    if not mongo:
        mongo = create_mongo_connection()

    customers = []
    rentals_dict = {}
    try:
        with mongo:
            LOGGER.info('Creating mongo connection')
            db = mongo.connection.HPNorton
            LOGGER.info(f'Querying rentals database for customers renting product {product_id}')
            # Filter query to return customers who rented specific product
            query = db['rentals'].find({'product_id': {'$eq':product_id}})
            customers = [item['customer_id'] for item in query]
            customers.sort()
            # Filter query results to find relevant customer details
            query = db['customer'].find({'user_id': {'$in':customers}})
            for item in query:
                rentals_dict[item['user_id']] = {'name': item['name'],
                                                 'address': item['address'],
                                                 'phone_number': item['phone_number'],
                                                 'email': item['email']}
    except (ConnectionFailure, ServerSelectionTimeoutError) as CF: # MongoDB connection issue
        LOGGER.error('Could not connect to MongoDB database.')
        LOGGER.error(f'Error message: {CF}')

    return rentals_dict

if __name__ == "__main__":
    directory = 'sample_csv_files'
    product_csv = 'products.csv'
    customer_csv = 'customers.csv'
    rentals_csv = 'rentals.csv'
    files = [string.split('.')[0] for string in [product_csv, customer_csv, rentals_csv]]
    # Drop tables before loading new data
    drop_tables(files)
    data = import_data(directory, product_csv, customer_csv, rentals_csv)
    for index, result in enumerate(data):
        print('{}: {}'.format(files[index], result))
