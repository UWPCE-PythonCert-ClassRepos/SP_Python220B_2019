'''
Advanced Programming in Python Lesson 7
Concurrency & Async

pylint disabled warnings: too-many-locals, logging-format-interpolation,
    too-many-statements
'''
import csv
import logging
import os
import time
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


def import_data(directory_name, product_file, customer_file, rental_file):
    '''
    import data from specified CSV files into mongo database
    '''

    prod_quant = 0
    cust_quant = 0
    rent_quant = 0

    cust_err = 0
    prod_err = 0
    rent_err = 0

    mongo = MongoDBConnection()
    with mongo:

        # mongodb database; it all starts here
        norton_db = mongo.connection.hp_norton

        cust_prior = norton_db.customers.count_documents({})
        prod_prior = norton_db.products.count_documents({})

        dir_path = os.path.join(os.getcwd(), directory_name)
        if os.path.exists(dir_path) is False:
            LOGGER.warning(f'directory path does not exist: {dir_path}')
        else: LOGGER.info(f"directory path for input files: {dir_path}")

        cust_start = time.time()
        try:
            with open(os.path.join(dir_path, customer_file), 'r') as cust_input:
                reader = csv.reader(cust_input)
                lines = len(list(reader))
            with open(os.path.join(dir_path, customer_file), 'r') as cust_input:
                LOGGER.info(f"reading {customer_file}")
                cust_dict = csv.DictReader(cust_input)
                cust_result = norton_db["customers"].insert_many(cust_dict)
                cust_quant = len(cust_result.inserted_ids)
                LOGGER.info(f'Inserted {cust_quant} customer ids')

        except FileNotFoundError:
            LOGGER.warning(f'File {customer_file} not found.')
            cust_err += 1
        except mongoerr.BulkWriteError as err:
            LOGGER.warning(f'Error writing to db: {err}.')
            cust_err += 1
        cust_finish = float(time.time()-cust_start)

        prod_start = time.time()
        try:
            with open(os.path.join(dir_path, customer_file), 'r') as prod_input:
                reader = csv.reader(prod_input)
                lines = len(list(reader))
            with open(os.path.join(dir_path, product_file), 'r') as prod_input:
                LOGGER.info(f"reading {product_file}")
                prod_dict = csv.DictReader(prod_input)
                prod_result = norton_db["products"].insert_many(prod_dict)
                prod_quant = len(prod_result.inserted_ids)
                LOGGER.info(f'Inserted {prod_quant} product ids')
        except FileNotFoundError:
            LOGGER.warning(f'File {product_file} not found.')
            prod_err += 1
        except mongoerr.BulkWriteError as err:
            LOGGER.warning(f'BulkWriteError writing to db: {err}.')
            prod_err += 1
        prod_finish = float(time.time()-prod_start)

        try:
            with open(os.path.join(dir_path, rental_file), 'r') as rent_input:
                LOGGER.info(f"reading {rental_file}")
                rent_dict = csv.DictReader(rent_input)
                rent_result = norton_db["rentals"].insert_many(rent_dict)
                rent_quant = len(rent_result.inserted_ids)
                LOGGER.info(f'Inserted {rent_quant} rental ids')
        except FileNotFoundError:
            LOGGER.warning(f'File {rental_file} not found.')
            rent_err += 1
        except mongoerr.BulkWriteError as err:
            LOGGER.warning(f'BulkWriteError writing to db: {err}.')
            rent_err += 1

        cust_total = norton_db.customers.count_documents({})
        prod_total = norton_db.products.count_documents({})

    #records processed, prior, total now, time
    cust_tuple = (cust_quant, cust_prior, cust_total, cust_finish)
    prod_tuple = (prod_quant, prod_prior, prod_total, prod_finish)

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
    #drop_collection()
    import_data('data_files', 'products.csv', 'customers.csv', 'rentals.csv')
