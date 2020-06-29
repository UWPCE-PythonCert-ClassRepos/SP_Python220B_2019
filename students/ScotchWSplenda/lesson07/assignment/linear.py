'''
code fails if there are extra commas in the data
'''
import csv
from pymongo import MongoClient
import logging
import time

# Set up logger
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


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


def import_customer_file(directory_name,  customer_file):
    '''import_customer_file'''
    # setting up method variables
    customer_file_start = time.time()
    customer_file_error = 0
    customer_file_attempts = 0

    mongo = MongoDBConnection()
    # why does this need a 'with'
    with mongo:
        # create/point to the DB
        db = mongo.connection.norton
        # create/point to the tables/collections
        customer_file_table = db['customers']
        initial_num = db.customers.count()

    try:
        with open(f'{directory_name}/{customer_file}', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                customer_file_attempts += 1
                try:
                    customer_file_table.insert_one(row)
                    LOGGER.info('customer_file added')
                except NameError:
                    customer_file_error += 1
                    LOGGER.info('customer_file has errors')
    except FileNotFoundError:
        LOGGER.info('customer_file not found.')
        customer_file_error += 1

    customer_file_end = time.time()
    product_time = customer_file_end - customer_file_start

    return (customer_file_attempts, initial_num, db.customers.count(),
            product_time, customer_file_error)


def import_product_file(directory_name,  product_file):
    '''import_product_file'''
    # setting up method variables
    product_file_start = time.time()
    product_file_error = 0
    product_file_attempts = 0

    mongo = MongoDBConnection()
    # why does this need a 'with'
    with mongo:
        # create/point to the DB
        db = mongo.connection.norton
        # create/point to the tables/collections
        product_file_table = db['products']
        initial_num = db.products.count()

    try:
        with open(f'{directory_name}/{product_file}', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                product_file_attempts += 1
                try:
                    product_file_table.insert_one(row)
                    LOGGER.info('product_file added')
                except NameError:
                    product_file_error += 1
                    LOGGER.info('product_file has errors')
    except FileNotFoundError:
        LOGGER.info('product_file not found.')
        product_file_error += 1

    product_file_end = time.time()
    product_time = product_file_end - product_file_start

    return (product_file_attempts, initial_num, db.products.count(),
            product_time, product_file_error)


def import_rental_file(directory_name,  rental_file):
    '''import_rental_file'''
    # setting up method variables
    rental_file_start = time.time()
    rental_file_error = 0
    rental_file_attempts = 0

    mongo = MongoDBConnection()
    # why does this need a 'with'
    with mongo:
        # create/point to the DB
        db = mongo.connection.norton
        # create/point to the tables/collections
        rental_file_table = db['rentals']
        initial_num = db.rentals.count()

    try:
        with open(f'{directory_name}/{rental_file}', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                rental_file_attempts += 1
                try:
                    rental_file_table.insert_one(row)
                    LOGGER.info('rental_file added')
                except NameError:
                    rental_file_error += 1
                    LOGGER.info('rental_file has errors')
    except FileNotFoundError:
        LOGGER.info('rental_file not found.')
        rental_file_error += 1

    rental_file_end = time.time()
    product_time = rental_file_end - rental_file_start

    return (rental_file_attempts, initial_num, db.rentals.count(),
            product_time, rental_file_error)


def drop_tables():
    '''jh'''
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.norton
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()
        LOGGER.info('Cleared all databases!')


def count_records():
    '''jh'''
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.norton
    return (db.products.count()+db.customers.count()+db.rentals.count())


if __name__ == '__main__':
    linear_start = time.time()
    drop_tables()
    begin_records = count_records()
    path = ('C:\\Users\\v-ollock\\github\\SP_Python220B_2019\\students\\ScotchWSplenda\\lesson07\\assignment\\csv_files')
    product_info = import_product_file(path, 'products.csv')
    rental_info = import_rental_file(path, 'rentals.csv')
    customer_info = import_customer_file(path, 'customers.csv')
    linear_end = time.time()
    end_records = count_records()
    print('-----Total Parallel Time-----')
    print(f'{end_records-begin_records},{begin_records}, {end_records},{linear_end-linear_start}')
