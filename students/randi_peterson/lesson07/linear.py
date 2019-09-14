"""This file creates and manipulates the database for HP Norton
MODIFIED TO RUN IN PARALLEL
"""

import csv
import logging
import os
import timeit
import time
from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
LOG_FILE = 'parallel.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

#   File handler set up
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

#   Console handler set up
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

#   Get logger
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


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


def clear_database():
    """Clear database for a new run"""
    #   Set up Mongo
    mongo = MongoDBConnection()
    with mongo:
        my_db = mongo.connection.media
        my_db.customers.drop()
        my_db.products.drop()
        my_db.rentals.drop()
        LOGGER.info('Database was cleared')


def create_dict_from_csv(csv_file):
    """This function creates a dict out of a csv file"""
    my_dict_lst = []
    with open(csv_file) as my_file:
        reader = csv.reader(my_file)
        header = next(reader)
        for row in reader:
            my_dict = dict(zip(header[:], row[:]))
            my_dict_lst.append(my_dict)

    return my_dict_lst


def add_thing(thing_dict_lst, thing):
    """Writing customer/product/rental from csv to database"""
    try:
        LOGGER.info(f'thing_dict is {thing_dict_lst}')
        thing.insert_many(thing_dict_lst)

    except FileNotFoundError as my_error:
        LOGGER.error(my_error)


def import_data(directory_name, product_file, customer_file, rental_file):
    """This function creates a new MongoDB database"""

    start_time = time.time()

    #   Set up Mongo
    mongo = MongoDBConnection()
    with mongo:
        my_db = mongo.connection.media

        #   Set up the database categories
        customers = my_db['customers']
        products = my_db['products']
        rentals = my_db['rentals']

        customers_before = customers.count_documents({})
        products_before = products.count_documents({})
        #   rentals_before = products.count_documents({})

        #   Store file location of each csv
        customers_file = os.path.join(directory_name, customer_file)
        products_file = os.path.join(directory_name, product_file)
        rentals_file = os.path.join(directory_name, rental_file)

        cust_dict_lst = create_dict_from_csv(customers_file)
        prod_dict_lst = create_dict_from_csv(products_file)
        rent_dict_lst = create_dict_from_csv(rentals_file)

        # Add customers, products, rentals
        add_thing(cust_dict_lst, customers)
        add_thing(prod_dict_lst, products)
        add_thing(rent_dict_lst, rentals)

        customers_added = len(cust_dict_lst)
        products_added = len(prod_dict_lst)
        #   rentals_added = len(rent_dict_lst)

        run_time = time.time() - start_time

        customers_after = customers_before + customers_added
        products_after = products_before + products_added
        #   rentals_after = rentals_before + rentals_added

        customers_tuple = (customers_added, customers_before, customers_after, run_time)
        products_tuple = (products_added, products_before, products_after, run_time)
        return customers_tuple, products_tuple


def show_available_products():
    """Shows products available"""
    #   Set up Mongo
    mongo = MongoDBConnection()
    with mongo:
        my_db = mongo.connection.media
        products = my_db['products']
        display_product_dict = {}
        for items in products.find():
            display_product_dict[items['product_id']] = {'description': items['description'],
                                                         'product_type': items['product_type'],
                                                         'quantity_available':
                                                             items['quantity_available']}
        return display_product_dict


def show_rentals(product_id):
    """Returns a Python dictionary with information from users who have rented the product"""
    # Set up Mongo
    mongo = MongoDBConnection()
    rental_list = []
    rental_dict = {}
    with mongo:
        my_db = mongo.connection.media
        rentals = my_db['rentals']

        #   Find users who have rented the given product
        for rents in rentals.find():
            if rents['product_id'] == product_id:
                rental_list.append(rents['user_id'])
        customers = my_db['customers']

        #   Get info of these users
        for users in rental_list:
            for person in customers.find({'user_id': users}):
                rental_dict[person['user_id']] = {'name': person['name'],
                                                  'address': person['address'], 'phone':
                                                  person['phone'], 'email': person['email']}
    return rental_dict


def import_test_data():
    """This function gets my test data file location and prints the results of importing"""
    current_directory = os.getcwd()
    test_data = os.path.join(os.path.abspath(current_directory), "test_files")
    test_dump = import_data(test_data, 'products_test.csv', 'customers_test.csv',
                            'rentals_test.csv')
    print(test_dump)


if __name__ == "__main__":
    print(timeit.timeit("import_test_data()", setup="from __main__ import import_test_data",
                        number=3))
