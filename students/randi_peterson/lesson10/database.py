"""This file creates and manipulates the database for HP Norton"""

import csv
import logging
import os
import time
from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
LOG_FILE = 'timings.txt'

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


def timer(func):
    """Decorator used to time all functions"""
    def timer_wrapper(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)  # Calls the function
        end_time = time.time()
        time_result = end_time - start_time
        if func.__name__ == "import_data":
            records = sum(value[0])
        else:
            records = "N/A"
        logging.info("The function {} ran for {} seconds to process {} records".format(
            func.__name__, time_result, records))
        return value
    return timer_wrapper

@timer
def clear_database():
    """Clear database for a new run"""
    #   Set up Mongo
    mongo = MongoDBConnection()
    with mongo:
        my_db = mongo.connection.media
        my_db.customers.drop()
        my_db.products.drop()
        my_db.rentals.drop()

@timer
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

@timer
def import_data(directory_name, product_file, customer_file, rental_file):
    """This function creates a new MongoDB database"""

    #   Set up Mongo
    mongo = MongoDBConnection()
    with mongo:
        my_db = mongo.connection.media

        #   Set up the database categories
        customers = my_db['customers']
        products = my_db['products']
        rentals = my_db['rentals']

        #   Store file location of each csv
        customers_file = os.path.join(directory_name, customer_file)
        products_file = os.path.join(directory_name, product_file)
        rentals_file = os.path.join(directory_name, rental_file)

        #   Declare initial values as zero
        products_added = 0
        customers_added = 0
        rentals_added = 0

        customers_errors = 0
        products_errors = 0
        rentals_errors = 0

        #   Writing customer from csv to database
        try:
            customer_dict_lst = create_dict_from_csv(customers_file)
            customers.insert_many(customer_dict_lst)
            customers_added = len(customer_dict_lst)

        except FileNotFoundError as my_error:
            customers_errors += 1

        #   Writing products from csv to database
        try:
            products_dict_lst = create_dict_from_csv(products_file)
            products.insert_many(products_dict_lst)
            products_added = len(products_dict_lst)

        except FileNotFoundError as my_error:
            products_errors += 1

        #   Writing rentals from csv to database
        try:
            rentals_dict_lst = create_dict_from_csv(rentals_file)
            rentals.insert_many(rentals_dict_lst)
            rentals_added = len(rentals_dict_lst)

        except FileNotFoundError as my_error:
            rentals_errors += 1

    return (products_added, customers_added, rentals_added), \
           (products_errors, customers_errors, rentals_errors)

@timer
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

@timer
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


if __name__ == "__main__":
    clear_database()
    import_data('', 'products_test.ccv', 'customers_test.csv', 'rentals_test.csv')
    show_available_products()
    show_rentals('prod1')
    clear_database()
    import_data('', 'products_test_long.ccv', 'customers_test_long.csv', 'rentals_test_long.csv')
    show_available_products()
    show_rentals('prod1')
