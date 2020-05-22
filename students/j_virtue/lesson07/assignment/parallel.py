'''Module to write csv filese to MongoDB'''
# Advanced Programming in Python -- Lesson 7 Assignment 1
# Jason Virtue
# Start Date 2/24/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name,too-few-public-methods,wrong-import-order,singleton-comparison,too-many-arguments,logging-format-interpolation,too-many-locals,no-else-return,unused-variable

from pymongo import MongoClient
from pymongo import errors as pyerror
import multiprocessing as mp
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
        logging.info(f'Number of rows in file {rows_read}')
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
    logging.info(f'Number of rows in collection {rows_insert}')
    return error_count, rows_insert

def run_import(product_file, customer_file, rental_file):
    '''Import module to run files in parallel'''
    logging.info("Reading CSV Files")
    csv_files = [product_file, customer_file, rental_file]
    results = []
    start_time = time.time()
    logging.info("Insertion method: Multiprocessing")
    pool = mp.Pool(mp.cpu_count())
    results = [pool.apply_async(import_data,
                                args=(data_file,
                                      data_file)) for data_file in csv_files]
    pool.close()

    end_time = time.time()
    execution_time = end_time - start_time

    stats = []
    for result in results:
        logging.info("RESULT: %s", result.get())
        stats.append(result.get())


    logging.info("Execution Time: %s", execution_time)

    return 'product', stats[0][1], stats[0][2], execution_time, 'customer', stats[1][1], \
     stats[1][2], execution_time

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
        rental_db.rentals.drop()
        rental_db.products.drop()
        rental_db.customers.drop()

def main():
    """ The main function for the program """
    print(run_import('products.csv',
                     'customers.csv',
                     'rentals.csv'))
    print("Done")


if __name__ == "__main__":
    drop_collection()
    main()
