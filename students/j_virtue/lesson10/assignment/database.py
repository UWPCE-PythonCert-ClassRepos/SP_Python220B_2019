'''Module to write csv filese to MongoDB'''
# Advanced Programming in Python -- Lesson 10 Assignment 1
# Jason Virtue
# Start Date 3/10/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name,too-few-public-methods,wrong-import-order,singleton-comparison,too-many-arguments,logging-format-interpolation,too-many-locals,no-else-return,unused-variable,redefined-outer-name

from pymongo import MongoClient
from pymongo import errors as pyerror
import csv
import logging
import time

# Set up log file
logging.basicConfig(filename="timings.txt", format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M %p', level=logging.INFO)


def function_performance(func):
    '''Captures from each function name, row count and processing time'''
    def inner(*args, **kwargs):
        start = time.time()
        func_return = func(*args, **kwargs)
        stop = time.time()
        if func.__name__ == "import_data":
            records_processed = func_return[0]
        else:
            records_processed = "No records loaded."
        logging.info('Function: %s\tTime taken: %s\tRecords processed: %s',
                     func.__name__, stop-start, records_processed)
        return func_return
    return inner


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

@function_performance
def import_data(file):
    '''Function to load csv files into dictionary variables'''
    data_dict = []
    error = 0
    insert = 0

    try:
        with open(file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                data_dict.append(line)
                insert += 1
        logging.info(f'Finished reading {file} file into dictionary')
    except FileNotFoundError:
        logging.info(f'{file} not found')
        error += 1

    return insert, error, data_dict

@function_performance
def insert_collection_many(dbname, collection, dataset):
    '''Function to insert csv files into MongoDB'''
    mongo = MongoDBConnection()

    with mongo:
        # mongodb database; it all starts here
        rental_db = mongo.connection.rental

    error_count = 0
    table = dbname[collection]

    try:
        table.insert_many(dataset)
    except pyerror.DuplicateKeyError as error:
        logging.info(error)
        logging.info(f'Failed to insert {collection} due to duplicate keys')
        error_count += 1
    return error_count

@function_performance
def show_available_products():
    '''Function to show quantity on hand'''
    # mongodb database; it all starts here
    mongo = MongoDBConnection()
    avail_product = {}
    #logging.info('Querying inventory for products with quantity available')
    with mongo:
        db = mongo.connection.rental
        for product in db.product.find({'quantity_available': {'$gt' : '0'}}):
            product_info = {'description': product['description'],
                            'product_type': product['product_type'],
                            'quantity_available': product['quantity_available']}
            avail_product[product['product_id']] = product_info
    return avail_product

@function_performance
def show_rentals(product_id):
    '''Returns customers who have rented particular product'''
    mongo = MongoDBConnection()
    #logging.info(f'Querying customers who rented specified {product_id}')
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
        #logging.info('Drop all collections in database')
        rental_db.rental.drop()
        rental_db.product.drop()
        rental_db.customer.drop()


if __name__ == '__main__':
    drop_collection()
    mongo = MongoDBConnection()
    with mongo:
        rental_db = mongo.connection.rental
    logging.info('Small Data set files')
    product_dict = import_data('products.csv')[2]
    insert_collection_many(rental_db, 'product', product_dict)
    customer_dict = import_data('customers.csv')[2]
    insert_collection_many(rental_db, 'customer', customer_dict)
    rental_dict = import_data('rentals.csv')[2]
    insert_collection_many(rental_db, 'rental', rental_dict)
    logging.info('Medium Data set files')
    product_dict = import_data('products_medium.csv')[2]
    insert_collection_many(rental_db, 'product', product_dict)
    customer_dict = import_data('customers_medium.csv')[2]
    insert_collection_many(rental_db, 'customer', customer_dict)
    rental_dict = import_data('rentals_medium.csv')[2]
    insert_collection_many(rental_db, 'rental', rental_dict)
    logging.info('Large Data set files')
    product_dict = import_data('products_large.csv')[2]
    insert_collection_many(rental_db, 'product', product_dict)
    customer_dict = import_data('customers_large.csv')[2]
    insert_collection_many(rental_db, 'customer', customer_dict)
    rental_dict = import_data('rentals_large.csv')[2]
    insert_collection_many(rental_db, 'rental', rental_dict)
    show_available_products()
    show_rentals('prd50')
