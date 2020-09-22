'''
Advanced Programming in Python Lesson 9
Advance Language Constructs; logger context manager

pylint disabled warnings:
'''
import csv
import logging
import os
from pymongo import MongoClient
from pymongo import errors as mongoerr


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.INFO)
CONSOLE_HANDLER.setFormatter(FORMATTER)


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


class MongoDBConnection():
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

class db_context():
    '''context manager for repetition'''
    def __init__(self, handle_error=False):
        self.handle_error = handle_error
        self.mongo = MongoDBConnection()


    def __enter__(self):
        with self.mongo:
            norton_db = self.mongo.connection.hp_norton
            self.rentals = norton_db.rentals
            self.products = norton_db.products
            self.customers = norton_db.customers
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.handle_error


def drop_collection():
    '''Drop all collections in database'''
    with db_context() as norton_db:
        norton_db.rentals.drop()
        norton_db.products.drop()
        norton_db.customers.drop()
        LOGGER.info('Dropped all collections in database')


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


    with db_context() as norton_db:

        dir_path = os.path.join(os.getcwd(), directory_name)
        if os.path.exists(dir_path) is False:
            LOGGER.warning(f'directory path does not exist: {dir_path}')
        else: LOGGER.info(f"directory path for input files: {dir_path}")

        try:
            with open(os.path.join(dir_path, customer_file), 'r') as cust_input:
                LOGGER.info(f"reading {customer_file}")
                cust_dict = csv.DictReader(cust_input)
                cust_result = norton_db.customers.insert_many(cust_dict)
                cust_quant = len(cust_result.inserted_ids)
                LOGGER.info(f'Inserted {cust_quant} customer ids')
        except FileNotFoundError:
            LOGGER.warning(f'File {customer_file} not found.')
            cust_err += 1
        except mongoerr.BulkWriteError as err:
            LOGGER.warning(f'Error writing to db: {err}.')
            cust_err += 1

        try:
            with open(os.path.join(dir_path, product_file), 'r') as prod_input:
                LOGGER.info(f"reading {product_file}")
                prod_dict = csv.DictReader(prod_input)
                prod_result = norton_db.products.insert_many(prod_dict)
                prod_quant = len(prod_result.inserted_ids)
                LOGGER.info(f'Inserted {prod_quant} product ids')
        except FileNotFoundError:
            LOGGER.warning(f'File {product_file} not found.')
            prod_err += 1
        except mongoerr.BulkWriteError as err:
            LOGGER.warning(f'BulkWriteError writing to db: {err}.')
            prod_err += 1

        try:
            with open(os.path.join(dir_path, rental_file), 'r') as rent_input:
                LOGGER.info(f"reading {rental_file}")
                rent_dict = csv.DictReader(rent_input)
                rent_result = norton_db.rentals.insert_many(rent_dict)
                rent_quant = len(rent_result.inserted_ids)
                LOGGER.info(f'Inserted {rent_quant} rental ids')
        except FileNotFoundError:
            LOGGER.warning(f'File {rental_file} not found.')
            rent_err += 1
        except mongoerr.BulkWriteError as err:
            LOGGER.warning(f'BulkWriteError writing to db: {err}.')
            rent_err += 1

    return ((prod_quant, cust_quant, rent_quant),
            (prod_err, cust_err, rent_err))


def show_available_products():
    '''
    display products and quantity available for rent
    '''
    LOGGER.info("loop thru products collection for available product details")
    prod_dict = {}

    with db_context() as norton_db:
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
    LOGGER.info("loop thru products collection for rented product details")
    rent_dict = {}

    with db_context() as norton_db:
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