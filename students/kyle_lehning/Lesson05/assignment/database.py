#!/usr/bin/env python3
"""Migration of product data from csv into MongoDB"""
from pymongo import MongoClient
import logging
import datetime


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
LOG_FILE = 'database' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
LOGGER = __setup_logger('database_logger', LOG_FILE, logging.DEBUG)


def main():
    pass


def print_mbd_collection(collection_name):
    for doc in collection_name.find():
        print(doc)


def import_data(directory_name, product_file, customer_file, rental_file):
    """
    This function takes a directory name and three csv files as input, one with product data,
    one with customer data, and the third one with rentals data. It creates and populates a new
    MongoDB database with these data. It returns 2 tuples: the first with a record count of the
    number of products, customers, and rentals added (in that order), the second with a count
    of any errors that occurred, in the same order
    """
    db_names = __set_db_names()
    with MONGO:
        # mongodb database
        db = MONGO.connection.media
        products = db[db_names[0]]
        customers = db[db_names[1]]
        rentals = db[db_names[2]]
        product_error = 0
        customer_error = 0
        rental_error = 0
        try:
            product_list = __read_csv(product_file)
            product_dict = __make_mongo_dictionary(product_list)
            product_result = products.insert_many(product_dict)
        except FileNotFoundError:
            product_error += 1
        try:
            customer_list = __read_csv(customer_file)
            customer_dict = __make_mongo_dictionary(customer_list)
            customer_result = customers.insert_many(customer_dict)
        except FileNotFoundError:
            customer_error += 1
        try:
            rental_list = __read_csv(rental_file)
            rental_dict = __make_mongo_dictionary(rental_list)
            rental_result = rentals.insert_many(rental_dict)
        except FileNotFoundError:
            rental_error += 1
        product_count = len(product_result.inserted_ids)
        customer_count = len(customer_result.inserted_ids)
        rental_count = len(rental_result.inserted_ids)
        count_tuple = (product_count, customer_count, rental_count)
        error_tuple = (product_error, customer_error, rental_error)
        return_list = [count_tuple, error_tuple]
        LOGGER.debug(return_list)
        return return_list


def __make_mongo_dictionary(passed_list):
    keys = passed_list.pop(0)
    return_dictionary = []
    for line in passed_list:
        return_dictionary.append(dict(zip(keys, line)))
    return return_dictionary


def __read_csv(passed_file):
    return_list = []
    with open(passed_file) as passed_csv:
        for line in passed_csv:
            data_line = line.rstrip().split(',')
            return_list.append(data_line)
    return return_list


def __set_db_names():
    """Set names with function so that this can be mocked for testing"""
    return ['products', 'customers', 'rentals']

def show_available_products():
    """
    Returns a python dictionary of products listed as available with the following fields:
    product_id
    description
    product_type
    quantity_available
    """
    pass


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
    pass


if __name__ == "__main__":
    main()
