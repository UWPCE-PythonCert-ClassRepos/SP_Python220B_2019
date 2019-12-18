""""
script for testing the performance of the functions.  Uses a wrapper to time.
"""

import csv
import logging
import json
from os import path
import os
import time
from pymongo import MongoClient
from csv_gen import csv_gen

# Engage the logging
if os.path.isfile('timings.txt'):
    os.remove('timings.txt')
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.FileHandler('timings.txt'))


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


def wrapper(function):
    """wrapper for the timing function"""
    def func(*args, **kwargs):
        """times the function and logs results"""
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        time_result = round(end - start, 3)
        LOGGER.info("%s seconds for %s to run", time_result, function.__name__)
        return result
    return func


def drop_collections():
    """Drop all the collections"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.myDB
        for collection in database.list_collection_names():
            database[collection].drop()


@wrapper
def import_csv(file_path):
    """Do you like json?  Do you hate csvs? Well I have a function for you!"""
    data = []
    err_count = 0
    if path.exists(file_path):
        with open(file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                try:
                    data.append(json.loads(json.dumps(row)))
                except AttributeError:
                    LOGGER.info("inserted file has missing values")
                    err_count += 1

            return {'data': data, 'errors': err_count}
    else:
        LOGGER.info("file DNE! path: %s", file_path)
        return {'data': [], 'errors': 0}


@wrapper
def insert_into_table(table_name, data):
    """takes an iterable with dictionaries and inserts them to a table"""
    err_count = 0
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.myDB
        table = database[table_name]

        for dictionary in data:
            try:
                table.insert_one(dictionary)
            except MongoClient.error.OperationFailure:
                err_count += 1
                LOGGER.info("error when inserting: %s", dictionary)
        return err_count


@wrapper
def import_data(directory_name, product_file, customer_file, rentals_file):
    """This function takes a directory name three csv files as input,
    one with product data, one with customer data and the third one with rentals data
     and creates and populates a new MongoDB database with these data.
     It returns 2 tuples: the first with a record count of the number of"""

    product_err = 0
    import_product = import_csv(directory_name + product_file)
    product_err += import_product['errors']
    product_err += insert_into_table('product', import_product['data'])

    customer_err = 0
    import_customer = import_csv(directory_name + customer_file)
    customer_err += import_customer['errors']
    customer_err += insert_into_table('customer', import_customer['data'])

    rental_err = 0
    import_rentals = import_csv(directory_name + rentals_file)
    rental_err += import_rentals['errors']
    rental_err += insert_into_table('rentals', import_rentals['data'])

    return ((len(import_product['data']), len(import_customer['data']),
             len(import_rentals['data'])), (product_err, customer_err, rental_err))


@wrapper
def show_available_products():
    """Returns a Python dictionary of products listed as available"""

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.myDB

        products = database.product.find(filter={"quantity_available": {"$gte": 0}},
                                         projection={'_id': False})

        return {product.pop('product_id'): product for product in products}


@wrapper
def show_rentals(product_id):
    """Returns a Python dictionary with the following user information
     from users that have rented products matching product_id"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.myDB

        rentals = database.rentals.find(filter={"product_id": product_id},
                                        projection={'_id': False})

        customers = database.customer.find(filter={'user_id': \
                                                       {'$in': [rental["customer_id"] \
                                                                for rental in rentals]}},
                                           projection={'_id': False})

        return {customer.pop('user_id'): customer for customer in customers}


if __name__ == '__main__':
    WD = os.getcwd() + '\\'
    for i in range(1000, 11000, 1000):
        LOGGER.info('Changing process size to %s records', i)
        drop_collections()
        csv_gen(i, 'products.csv', 'customers.csv', 'rentals.csv')
        import_data(WD, 'products.csv', 'customers.csv', 'rentals.csv')
        show_available_products()
        show_rentals('prd' + str(i))
