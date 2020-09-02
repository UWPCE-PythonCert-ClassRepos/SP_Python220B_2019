'''
Advanced Programming in Python Lesson 7
Concurrency & Async

pylint disabled warnings: too-many-locals, logging-format-interpolation,

'''
import csv
import logging
import os
import time
#import queue
import threading
#from collections import OrderedDict
from pymongo import MongoClient
from pymongo import errors as mongoerr


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.WARNING)
CONSOLE_HANDLER.setFormatter(FORMATTER)


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.WARNING)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


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


def drop_collection():
    '''Drop all collections in database'''
    mongo = MongoDBConnection()

    with mongo:
        norton_db = mongo.connection.hp_norton
        LOGGER.info('Drop all collections in database')
        norton_db.rentals.drop()
        norton_db.products.drop()
        norton_db.customers.drop()


def create_dict(directory_name, input_file):
    '''
    import data from specified CSV files into mongo database
    '''
    input_err = 0
    new_data = []

    dir_path = os.path.join(os.getcwd(), directory_name)
    if os.path.exists(dir_path) is False:
        LOGGER.warning(f'directory path does not exist: {dir_path}')
    else: LOGGER.info(f"directory path for input files: {dir_path}")

    try:
        with open(os.path.join(dir_path, input_file)) as csv_data:
            reader = csv.reader(csv_data)
            header = next(reader)
            for row in reader:
                new_item = dict(zip(header[:], row[:]))
                new_data.append(new_item)
    except FileNotFoundError:
        LOGGER.warning(f'File {input_file} not found.')
        input_err += 1

    return new_data

def add_docs(collection, input_dict):
    '''
    adds data (dict) to specified collection in database
    '''
    add_err = 0

    try:
        collection.insert_many(input_dict)
    except FileNotFoundError:
        LOGGER.warning(f'Collection {collection} not found.')
        add_err += 1
    except mongoerr.BulkWriteError as err:
        LOGGER.warning(f'Error writing to db: {err}.')
        add_err += 1

def import_data(directory_name, product_file, customer_file, rental_file):
    '''
    use threads to add data to collections
    '''
    start_time = time.time()

    mongo = MongoDBConnection()
    with mongo:
        norton_db = mongo.connection.hp_norton

        cust_coll = norton_db['customers']
        prod_coll = norton_db['products']
        rent_coll = norton_db['rentals']

        cust_prior = cust_coll.count_documents({})
        prod_prior = prod_coll.count_documents({})

        cust_dict = create_dict(directory_name, customer_file)
        prod_dict = create_dict(directory_name, product_file)
        rent_dict = create_dict(directory_name, rental_file)

        cust_thread = threading.Thread(target=add_docs, args=(cust_coll, cust_dict))
        prod_thread = threading.Thread(target=add_docs, args=(prod_coll, prod_dict))
        rent_thread = threading.Thread(target=add_docs, args=(rent_coll, rent_dict))

        cust_thread.start()
        prod_thread.start()
        rent_thread.start()

        cust_thread.join()
        prod_thread.join()
        rent_thread.join()

        completion_time = float(time.time()-start_time)

        cust_added = len(cust_dict)
        prod_added = len(prod_dict)

        cust_after = cust_prior + cust_added
        prod_after = prod_prior + prod_added

        cust_tuple = (cust_added, cust_prior, cust_after, completion_time)
        prod_tuple = (prod_added, prod_prior, prod_after, completion_time)

    print(cust_tuple, prod_tuple)
    return cust_tuple, prod_tuple

def show_available_products():
    '''
    display products and quantity available for rent
    '''
    LOGGER.info("loop thru products collection for available product details")
    prod_dict = {}
    mongo = MongoDBConnection()
    with mongo:

        norton_db = mongo.connection.hp_norton

        for prod in norton_db.products.find({}, {'_id': 0, 'product_id': 1,
                                                 'description': 1, 'product_type': 1,
                                                 'quantity_available': 1}):
            prod_dict[prod['product_id']] = {'description':prod['description'],
                                             'product_type':prod['product_type'],
                                             'quantity_available':
                                             int(prod['quantity_available'])}
    return prod_dict


def show_rentals(product_id):
    '''
    display customer details for specific products
    '''
    LOGGER.info("loop thru products collection for available product details")
    rent_dict = {}
    mongo = MongoDBConnection()
    with mongo:

        norton_db = mongo.connection.hp_norton

        for rent in norton_db.rentals.find({'product_id': product_id}):
            for cust in norton_db.customers.find({'customer_id': rent['customer_id']}):
                rent_dict[cust['customer_id']] = {'name': cust['name'],
                                                  'address': cust['address'],
                                                  'phone number': cust['phone_number'],
                                                  'email': cust['email']}
        return rent_dict


if __name__ == '__main__':
#     #drop_collection()
    import_data('data_files', 'products.csv', 'customers.csv', 'rentals.csv')
