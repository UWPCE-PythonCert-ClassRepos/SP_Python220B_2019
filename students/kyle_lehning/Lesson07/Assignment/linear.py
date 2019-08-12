#!/usr/bin/env python3
"""Migration of product data from csv into MongoDB"""
import logging
import datetime
import time
import os
from timeit import timeit as timer
from pymongo import MongoClient


class MongoDBConnection:
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
LOG_FILE = 'linear' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
LOGGER = __setup_logger('database_logger', LOG_FILE, logging.DEBUG)


def import_data(directory_name, product_file, customer_file, rental_file):  # pylint: disable=R0914, R0915
    """
    This function takes a directory name and three csv files as input, one with product data,
    one with customer data, and the third one with rentals data. It creates and populates a new
    MongoDB database with these data. It returns a list with 3 tuples for customers, products, and
    rentals. Each tuple will contain 4 values: the number of records processed (int), the record
    count in the database prior to running (int), the record count after running (int), and the time
    taken to run the module (float)
    """
    db_names = __set_collection_names()
    with MONGO:
        # mongodb database
        db = MONGO.connection.media  # pylint: disable=C0103
        product_error = 0
        customer_error = 0
        rental_error = 0
        product_start = time.time()
        products = db[db_names[0]]
        product_start_count = products.count_documents({})
        try:
            product_list = __read_csv(os.path.join(directory_name, product_file))
            product_dict = __make_mongo_dictionary(product_list)
            product_result = products.insert_many(product_dict)
            product_count = len(product_result.inserted_ids)
        except FileNotFoundError:
            product_error += 1
            product_count = 0
        product_final_count = products.count_documents({})
        product_end = time.time()
        product_time = product_end - product_start
        customer_start = time.time()
        customers = db[db_names[1]]
        customer_start_count = customers.count_documents({})
        try:
            customer_list = __read_csv(os.path.join(directory_name, customer_file))
            customer_dict = __make_mongo_dictionary(customer_list)
            customer_result = customers.insert_many(customer_dict)
            customer_count = len(customer_result.inserted_ids)
        except FileNotFoundError:
            customer_error += 1
            customer_count = 0
        customer_final_count = customers.count_documents({})
        customer_end = time.time()
        customer_time = customer_end - customer_start
        rental_start = time.time()
        rentals = db[db_names[2]]
        rental_start_count = rentals.count_documents({})
        try:
            rental_list = __read_csv(os.path.join(directory_name, rental_file))
            rental_dict = __make_mongo_dictionary(rental_list)
            rental_result = rentals.insert_many(rental_dict)
            rental_count = len(rental_result.inserted_ids)
        except FileNotFoundError:
            rental_error += 1
            rental_count = 0
        rental_final_count = rentals.count_documents({})
        rental_end = time.time()
        rental_time = rental_end - rental_start
        customer_tuple = (customer_count, customer_start_count, customer_final_count, customer_time)
        product_tuple = (product_count, product_start_count, product_final_count, product_time)
        rental_tuple = (rental_count, rental_start_count, rental_final_count, rental_time)
        return_list = [customer_tuple, product_tuple, rental_tuple]
        LOGGER.info("Returned: %s", return_list)
        return return_list


def __make_mongo_dictionary(passed_list):
    """Makes a dictionary from a list who's first item is keys"""
    keys = passed_list.pop(0)
    return_dictionary = []
    for line in passed_list:
        return_dictionary.append(dict(zip(keys, line)))
    return return_dictionary


def __read_csv(passed_file):
    """Make a list from a csv file"""
    return_list = []
    with open(passed_file) as passed_csv:
        for line in passed_csv:
            data_line = line.rstrip().split(',')
            return_list.append(data_line)
    return return_list


def __set_collection_names():
    """Set names with function so that this can be mocked for testing"""
    return ['products', 'customers', 'rentals']


if __name__ == '__main__':
    LOGGER.info('timeit run: %s', timer("import_data('', 'Products.csv', 'Customers.csv', "
                                        "'Rentals.csv')", globals=globals(), number=10))
    erase_db_names = __set_collection_names()  # pylint: disable=C0103
    with MONGO:
        erase_db = MONGO.connection.media  # pylint: disable=C0103
        erase_db[erase_db_names[0]].drop()
        erase_db[erase_db_names[1]].drop()
        erase_db[erase_db_names[2]].drop()
