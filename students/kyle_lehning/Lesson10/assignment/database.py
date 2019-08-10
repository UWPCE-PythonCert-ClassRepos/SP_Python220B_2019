#!/usr/bin/env python3
"""Migration of product data from csv into MongoDB"""
import logging
import datetime
import time
import os
from pymongo import MongoClient


class MongoDBConnection:
    """MongoDB Connection"""
    @staticmethod
    def set_collection_names():
        """Set names with function so that this can be mocked for testing"""
        return ['products', 'customers', 'rentals']

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        self.db = None  # pylint: disable=C0103
        self.products = None
        self.customers = None
        self.rentals = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        self.db = self.connection.media  # pylint: disable=C0103
        db_names = self.set_collection_names()
        self.products = self.db[db_names[0]]
        self.customers = self.db[db_names[1]]
        self.rentals = self.db[db_names[2]]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def __setup_logger(name, log_file, level=logging.WARNING, stream=True):
    """
    This function sets up loggers.
    """
    log_format = logging.Formatter("%(asctime)s%(filename)s:%(lineno)-3d %(levelname)s %(message)s")
    handler = logging.FileHandler(log_file)
    handler.setFormatter(log_format)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    if stream is True:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)
        logger.addHandler(stream_handler)
    return logger


MONGO = MongoDBConnection()
LOG_FILE = 'timings' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
LOGGER = __setup_logger('database_logger', LOG_FILE, logging.INFO)


def time_decorator(func):
    """decorator to time functions and report it to log file"""
    def wrapper(*args, **kwargs):
        """wrapper for time_decorator"""
        start_time = time.perf_counter()  # this is ran before the function is called
        value = func(*args, **kwargs)  # calls the passed function
        end_time = time.perf_counter()
        total_time = end_time - start_time
        LOGGER.info('%s took %s seconds to run', func.__name__, total_time)
        return value
    return wrapper


@time_decorator
def import_data(directory_name, product_file, customer_file, rental_file):  # pylint: disable=R0914
    """
    This function takes a directory name and three csv files as input, one with product data,
    one with customer data, and the third one with rentals data. It creates and populates a new
    MongoDB database with these data. It returns 2 tuples: the first with a record count of the
    number of products, customers, and rentals added (in that order), the second with a count
    of any errors that occurred, in the same order
    """
    with MONGO:
        # mongodb database
        product_error = 0
        customer_error = 0
        rental_error = 0
        try:
            product_list = __read_csv(os.path.join(directory_name, product_file))
            product_dict = __make_mongo_dictionary(product_list)
            product_result = MONGO.products.insert_many(product_dict)
            product_count = len(product_result.inserted_ids)
        except FileNotFoundError:
            product_error += 1
            product_count = 0
        try:
            customer_list = __read_csv(os.path.join(directory_name, customer_file))
            customer_dict = __make_mongo_dictionary(customer_list)
            customer_result = MONGO.customers.insert_many(customer_dict)
            customer_count = len(customer_result.inserted_ids)
        except FileNotFoundError:
            customer_error += 1
            customer_count = 0
        try:
            rental_list = __read_csv(os.path.join(directory_name, rental_file))
            rental_dict = __make_mongo_dictionary(rental_list)
            rental_result = MONGO.rentals.insert_many(rental_dict)
            rental_count = len(rental_result.inserted_ids)
        except FileNotFoundError:
            rental_error += 1
            rental_count = 0
        count_tuple = (product_count, customer_count, rental_count)
        error_tuple = (product_error, customer_error, rental_error)
        return_list = [count_tuple, error_tuple]
        return return_list


@time_decorator
def __make_mongo_dictionary(passed_list):
    """Makes a dictionary from a list who's first item is keys"""
    keys = passed_list.pop(0)
    return_dictionary = []
    for line in passed_list:
        return_dictionary.append(dict(zip(keys, line)))
    return return_dictionary


@time_decorator
def __read_csv(passed_file):
    """Make a list from a csv file"""
    return_list = []
    with open(passed_file) as passed_csv:
        for line in passed_csv:
            data_line = line.rstrip().split(',')
            return_list.append(data_line)
    return return_list


@time_decorator
def show_available_products():
    """
    Returns a python dictionary of products listed as available with the following fields:
    product_id
    description
    product_type
    quantity_available
    """
    with MONGO:
        # mongodb database
        available_dict = {}
        for doc in MONGO.products.find({'quantity_available': {"$gt": '0'}}):
            product = {'description': doc['description'],
                       'product_type': doc['product_type'],
                       'quantity_available': doc['quantity_available']}
            available_dict[doc['product_id']] = product
        return available_dict


@time_decorator
def show_rentals(product_id):
    """
    This function returns a python dictionary with the following user information from users that
    have rented products matching product_id:
    user_id
    name
    address
    phone_number
    email
    """
    with MONGO:
        customer_dict = {}
        for rental in MONGO.rentals.find({'product_id': product_id}):
            query = {"user_id": rental["user_id"]}
            for customer in MONGO.customers.find(query):
                customer_info = {'name': customer['name'],
                                 'address': customer['address'],
                                 'phone_number': customer['phone_number'],
                                 'email': customer['email']}
                customer_dict[customer["user_id"]] = customer_info
        LOGGER.debug(customer_dict)
        return customer_dict


if __name__ == '__main__':
    my_import_data = import_data('', 'Products.csv', 'Customers.csv', 'Rentals.csv')
    available_prods = show_available_products()
    rental = show_rentals('prd00001')
    with MONGO:
        db = MONGO.connection.media  # pylint: disable=C0103
        db['products'].drop()
        db['customers'].drop()
        db['rentals'].drop()
    my_import_data2 = import_data('', 'Products_big.csv', 'Customers_big.csv', 'Rentals_big.csv')
    available_prods2 = show_available_products()
    rental2 = show_rentals('prd00001')
    with MONGO:
        db = MONGO.connection.media  # pylint: disable=C0103
        db['products'].drop()
        db['customers'].drop()
        db['rentals'].drop()
