'''Module to write csv filese to MongoDB'''
# Advanced Programming in Python -- Lesson 5 Assignment 1
# Jason Virtue
# Start Date 2/20/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name,too-few-public-methods,wrong-import-order,singleton-comparison,too-many-arguments,logging-format-interpolation,too-many-locals,no-else-return,unused-variable

from pymongo import MongoClient
from pymongo import errors as pyerror
import csv
import logging

# Set up log file
logging.basicConfig(filename="db.log", format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M %p', level=logging.INFO)


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """Connection String for windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def import_data(product_file, customer_file, rental_file):
    '''Function to load csv files into dictionary variables'''
    customer_dict = []
    product_dict = []
    rental_dict = []
    error_prod, error_cust, error_rentals = 0, 0, 0

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database; it all starts here
        rental_db = mongo.connection.rental
        logging.info('Create rental database in MongoDB')

    try:
        logging.info(f'Reading {customer_file} file into dictionary')
        with open(customer_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                customer_dict.append(line)
        logging.info(f'Finished reading {customer_file} file into dictionary')
    except FileNotFoundError:
        logging.info(f'{customer_file} not found')
        error_cust += 1

    try:
        logging.info(f'Reading {product_file} file into dictionary')
        with open(product_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                product_dict.append(line)
        logging.info(f'Finished reading {product_file} file into dictionary')
    except FileNotFoundError:
        logging.info(f'{product_file} not found')
        error_prod += 1

    try:
        logging.info(f'Reading {rental_file} file into dictionary')
        with open(rental_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                rental_dict.append(line)
        logging.info(f'Finished reading {rental_file} file into dictionary')
    except FileNotFoundError:
        logging.info(f'{rental_file} not found')
        error_rentals += 1

    total_file_errors = (error_prod, error_cust, error_rentals)
    sum_file_errors = error_prod + error_cust + error_rentals

    if sum_file_errors > 0:
        return total_file_errors
    else:
        insert_collection_many(rental_db, 'customer', customer_dict)
        insert_collection_many(rental_db, 'product', product_dict)
        insert_collection_many(rental_db, 'rental', rental_dict)

        return total_file_errors, sum_file_errors

def insert_collection_many(dbname, collection, dataset):
    '''Function to insert csv files into MongoDB'''
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database; it all starts here
        rental_db = mongo.connection.rental
        logging.info('Create rental database in MongoDB')

    error_count = 0
    table = dbname[collection]
    logging.info(f'Create {collection} table in database')

    try:
        table.insert_many(dataset)
        logging.info(f'Insert {collection} records into table')
    except pyerror.DuplicateKeyError as error:
        logging.info(error)
        logging.info(f'Failed to insert {collection} due to duplicate keys')
        error_count += 1
    return error_count

def show_available_products():
    '''Function to show quantity on hand'''
    # mongodb database; it all starts here
    mongo = MongoDBConnection()
    avail_product = {}
    logging.info('Querying inventory for products with quantity available')
    with mongo:
        db = mongo.connection.rental
        for product in db.product.find({'quantity_available': {'$gt' : '0'}}):
            product_info = {'description': product['description'],
                            'product_type': product['product_type'],
                            'quantity_available': product['quantity_available']}
            avail_product[product['product_id']] = product_info
    return avail_product

def show_rentals(product_id):
    '''Returns customers who have rented particular product'''
    mongo = MongoDBConnection()
    logging.info(f'Querying customers who rented specified {product_id}')
    with mongo:
        db = mongo.connection.rental
        rent_dict = {}
        rental_info = db.rental.find({'product_id': product_id})
        for item in rental_info:
            cust_info = db.customer.find_one({'customer_id': item['customer_id']})
            rent_dict[cust_info['customer_id']] = {'name': cust_info['name'],
                                                   'address': cust_info['address'],
                                                   'phone_number': cust_info['phone_number'],
                                                   'email_address': cust_info['email_address']
                                                  }
    return rent_dict

def drop_collection():
    '''Drop all collections in database'''
    mongo = MongoDBConnection()

    with mongo:
        rental_db = mongo.connection.rental
        logging.info('Drop all collections in database')
        rental_db.rental.drop()
        rental_db.product.drop()
        rental_db.customer.drop()
