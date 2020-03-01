'''Module to write csv filese to MongoDB'''
# Advanced Programming in Python -- Lesson 7 Assignment 1
# Jason Virtue
# Start Date 2/24/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name,too-few-public-methods,wrong-import-order,singleton-comparison,too-many-arguments,logging-format-interpolation,too-many-locals,no-else-return,unused-variable

from pymongo import MongoClient
from pymongo import errors as pyerror
import csv
import logging
import time

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

def import_data(data_file, collection):
    '''Function to load csv files into dictionary variables'''
    data_dict = []
    error_data = 0
    rows_read = 0
    collection = collection.split(".")[0]

    mongo = MongoDBConnection()

    with mongo:
        # mongodb database; it all starts here
        rental_db = mongo.connection.rental
        logging.info('Create rental database in MongoDB')

    try:
        logging.info(f'Reading {data_file} file into dictionary')
        with open(data_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                data_dict.append(line)
                rows_read += 1
        logging.info(f'Finished reading {data_file} file into dictionary')
    except FileNotFoundError:
        logging.info(f'{data_file} not found')
        error_data += 1

    total_file_errors = error_data

    if total_file_errors > 0:
        return total_file_errors
    else:
        rows_insert = insert_collection_many(rental_db, collection, data_dict)[1]

        return total_file_errors, rows_read, rows_insert


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

    rows_insert = 0
    rows_insert = table.find().count()

    return error_count, rows_insert

def run_import(product_file, customer_file, rental_file):
    '''Import module to run files sequentially'''
    customer_start_time = time.time()
    customer_results = import_data(customer_file, 'customer')
    customer_end_time = time.time()
    product_start_time = time.time()
    product_results = import_data(product_file, 'product')
    product_end_time = time.time()
    import_data(rental_file, 'rental')

    customer_execution_time = customer_end_time - customer_start_time
    product_execution_time = product_end_time - product_start_time
    total_execution_time = customer_execution_time + product_execution_time

    logging.info("RESULT: %s", customer_results)

    logging.info("Customer Execution Time: %s", customer_execution_time)

    logging.info("RESULT: %s", product_results)

    logging.info("Product Execution Time: %s", product_execution_time)

    logging.info("Total Execution Time: %s", total_execution_time)

    return 'customers', customer_results[1], customer_results[2], 'product', product_results[1], \
    product_results[2], total_execution_time

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

def main():
    """ The main function for the program """
    print(run_import('products.csv',
                     'customers.csv',
                     'rentals.csv'))
    print("Done")


if __name__ == "__main__":
    drop_collection()
    main()
