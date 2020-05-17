#database.py
""" This module defines all the functions for HP Norton MongoDB database"""
import time
import os
import sys
import csv
import logging
from pymongo import MongoClient

# set logging configuration
LOG_FORMAT = "%(levelname)s %(filename)s %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class Counter():
    """ This class define a counter """
    def __init__(self, start=0):
        self.value = start

    def increment(self):
        self.value += 1

# using a context manager class to define the connection to a database.
class MongoDBConnection():
    """ This class defines the connetion to MongoDB."""
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def read_thousand_csv_file(dir_name, csv_file, collection, counter):
    processed_records = 0
    try:
        filename = os.path.join(dir_name, csv_file)
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            # create the document for products collection
            for row in csv_reader:
                collection.insert_one(row)
                processed_records += 1
                counter.increment()
    except FileNotFoundError:
        LOGGER.info('FileNotFoundError')
        sys.exit()
    except Exception as error:
        LOGGER.info('Exception:')
        LOGGER.info(error)
        sys.exit()
    return processed_records

def read_csv_file(dir_name, csv_file, collection, error_list):
    """ This function read a csv file into MongoDB database
        The input csv file is stricted to only one field one element, can't
        process list, dictionary fields, can't read in int or float numbers.
    """
    count = 0
    try:
        filename = os.path.join(dir_name, csv_file)
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            # create the document for products collection
            for row in csv_reader:
                collection.insert_one(row)
    except FileNotFoundError:
        LOGGER.info('FileNotFoundError')
        count += 1
    except Exception as error:
        count += 1
        LOGGER.info('Exception:')
        LOGGER.info(error)
    error_list.append(count)


def import_data(dir_name, product_file, customer_file, rentals_file):
    """ This function takes a directory name three csv files as input, one with
        product data, one with customer data and the third one with rentals
        data and creates and populates a new MongoDB database with these data.
        It returns 2 tuples: the first with a record count of the number of
        products, customers and rentals added (in that order), the second with
        a count of any errors that occurred, in the same order.
    """
    client = MongoDBConnection()
    with client:
        LOGGER.info('Create A MongoDB database')
        hp_norton_db = client.connection.rental
        hp_norton_db.products.drop()
        hp_norton_db.customers.drop()
        hp_norton_db.rentals.drop()

        # create three collections.
        LOGGER.info('Create three collections')
        products = hp_norton_db['products']
        customers = hp_norton_db['customers']
        rentals = hp_norton_db['rentals']
        error_list = []

        # 1. load the products collection
        #LOGGER.info('Load the products collection')
        read_csv_file(dir_name, product_file, products, error_list)
        for doc in products.find():
            LOGGER.debug(f'-- products:{doc}.')
        LOGGER.debug(f'Error_list:{error_list}')

        # 2. load the customers collection
        #LOGGER.info('Load the customers collection')
        read_csv_file(dir_name, customer_file, customers, error_list)
        for doc in customers.find():
            LOGGER.debug(f'-- cusotmers:{doc}.')
        LOGGER.debug(f'Error_list:{error_list}')

        # 3. load the rentals collection
        #LOGGER.info('Load the rentals collection')
        read_csv_file(dir_name, rentals_file, rentals, error_list)
        for doc in rentals.find():
            LOGGER.debug(f'-- rentals:{doc}.')
        LOGGER.debug(f'Error_list:{error_list}')
        for i in error_list:
            if i == 1:
                LOGGER.debug('!!! Error in importing csv files')
    LOGGER.info('Finish import three csv files')
    return [(products.count(), customers.count(), rentals.count()),
            tuple(error_list)]


def import_thousand_data(dir_name, product_file, customer_file, rentals_file):
    """ This function takes a directory name three csv files as input, one with
        product data, one with customer data and the third one with rentals
        data and creates and populates a new MongoDB database with these data.
        It returns a list of tuples, one tuple for customer & one for products.
        Each tuple will contain 4 values: the number of records processed (int),
        the record count in the database prior to running (int), the record
        count after running (int), and the time taken to run the module (float).
    """
    counter = Counter()
    client = MongoDBConnection()
    with client:
        hp_norton_db = client.connection.rental
        products = hp_norton_db['products']
        customers = hp_norton_db['customers']
        rentals = hp_norton_db['rentals']
        exist_products = products.count()
        exist_customers = customers.count()
        exist_rentals = rentals.count()

        # 1. load the products collection
        start = time.time()
        LOGGER.info('Load the products collection')
        processed_records = read_thousand_csv_file(dir_name, product_file,
                                                   products, counter)
        product_tuple = (processed_records, exist_products, products.count(),
                         time.time() - start)
        # 2. load the customers collection
        start = time.time()
        LOGGER.info('Load the customers collection')
        processed_records = read_thousand_csv_file(dir_name, customer_file,
                                                   customers, counter)
        customer_tuple = (processed_records, exist_customers, customers.count(),
                          time.time() - start)
        # 3. load the rentals collection
        start = time.time()
        LOGGER.info('Load the rentals collection')
        processed_records = read_thousand_csv_file(dir_name, rentals_file,
                                                   rentals, counter)
        rental_tuple = (processed_records, exist_rentals, rentals.count(),
                        time.time() - start)
        LOGGER.info(f'Return product tuple {product_tuple}')
        LOGGER.info(f'Return customer tuple {customer_tuple}')
        LOGGER.info(f'Return rental tuple {rental_tuple}')
        LOGGER.info('Total record prcessed for all three files:'
                    f'{counter.value}')
        return [product_tuple, customer_tuple]
