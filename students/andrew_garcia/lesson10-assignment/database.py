'''Converting CSV Files and Putting Them Into a Database'''

import csv
import os
import logging
import time

from pymongo import MongoClient

# pylint: disable=invalid-name
# pylint: disable=too-many-statements
# pylint: disable=too-many-locals

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class MongodbConnection():
    """ Connects to Mongodb """
    LOGGER.info('Connecting to Mongo')
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.close()


def time_function(func):
    """ Times how long a function will take """
    def function_time(*args, **kwargs):
        LOGGER.info('Timing Function...')
        start_time = time.process_time()
        action = func(*args, **kwargs)
        end_time = time.process_time()
        process_time = end_time - start_time
        result = "{} took {} to process.".format(func.__name__, process_time)
        with open('timings.txt', 'a+') as file:
            file.write(result + '\n')
        return action
    return function_time


@time_function
def import_products(directory_name, product_file):
    """ Imports Products CSV File """
    mongo = MongodbConnection()

    with mongo:
        LOGGER.info('Creating Products Database')
        db = mongo.connection.media
        db.products.drop()
        products = db['products']

        LOGGER.info('Adding Product file')
        #product_start_time = time.time()
        product_file = os.path.join(directory_name, product_file)
        added_products = 0
        try:
            LOGGER.info('Converting Product CSV File to Dictionary')
            with open(product_file, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for item in reader:
                    csv_item = {'product_id': item['product_id'],
                                'description': item['description'],
                                'product_type': item['product_type'],
                                'quantity_available': item['quantity_available']}
                    LOGGER.info('Products Added')
                    products.insert_one(csv_item)
                    added_products += 1

        except FileNotFoundError:
            LOGGER.error('File Not Found.')
            print('File %s Does Not Exist', product_file)

        #product_end_time = time.time()
        #product_time = product_end_time - product_start_time
        product_details = ('Products', added_products)

        return product_details


@time_function
def import_customers(directory_name, customer_file):
    """ Imports Customer CSV File """
    mongo = MongodbConnection()

    with mongo:
        LOGGER.info('Creating Customers Database')
        db = mongo.connection.media
        db.customers.drop()
        customers = db['customers']

        LOGGER.info('Adding Customer file')
        #customer_start_time = time.time()
        customer_file = os.path.join(directory_name, customer_file)
        added_customers = 0
        try:
            LOGGER.info('Converting Customer CSV File to Dictionary')
            with open(customer_file, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for item in reader:
                    csv_item = {'user_id': item['user_id'], 'name': item['name'],
                                'address': item['address'],
                                'phone_number': item['phone_number'], 'email': item['email']}
                    LOGGER.info('Customers Added')
                    customers.insert_one(csv_item)
                    added_customers += 1

        except FileNotFoundError:
            LOGGER.error('File Not Found.')
            print('File %s Does Not Exist', customer_file)

        #customer_end_time = time.time()
        #customer_time = customer_end_time - customer_start_time
        customer_details = ('Customers', added_customers)

        return customer_details


@time_function
def import_rentals(directory_name, rental_file):
    """ Imports Rental CSV File """
    mongo = MongodbConnection()

    with mongo:
        LOGGER.info('Creating Rentals Database')
        db = mongo.connection.media
        db.rentals.drop()
        rentals = db['rentals']

        LOGGER.info('Adding Rental file')
        #rental_start_time = time.time()
        rental_file = os.path.join(directory_name, rental_file)
        added_rentals = 0
        try:
            LOGGER.info('Converting Rental CSV File to Dictionary')
            with open(rental_file, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for item in reader:
                    csv_item = {'rental_id': item['rental_id'], 'product_id': item['product_id'],
                                'user_id': item['user_id'], 'name': item['name'],
                                'address': item['address'],
                                'phone_number': item['phone_number'], 'email': item['email']}
                    LOGGER.info('Rentals Added')
                    rentals.insert_one(csv_item)
                    added_rentals += 1

        except FileNotFoundError:
            LOGGER.error('File Not Found.')
            print('File %s Does Not Exist', rental_file)

        #rental_end_time = time.time()
        #rental_time = rental_end_time - rental_start_time
        rental_details = ('Rentals', added_rentals)

        return rental_details


def show_available_products():
    """ Returns dictionary of products listed as available with product id, description,
    product type, quantity available, """
    mongo = MongodbConnection()

    with mongo:
        LOGGER.info('Connecting to Database')
        db = mongo.connection.media
        available_products = {}
        LOGGER.info('Finding Available Products')
        for item in db.products.find():
            product_info = {'product_id': item['product_id'], 'description': item['description'],
                            'product_type': item['product_type'],
                            'quantity_available': item['quantity_available']}
            available_products[item['product_id']] = product_info
        return available_products


def show_rentals(product_id):
    """ Returns dictionary with user id, name, address, phone number, and email who are renting a
    certain product"""
    mongo = MongodbConnection()

    with mongo:
        LOGGER.info('Connecting to Database')
        db = mongo.connection.media
        rental_data = {}
        LOGGER.info('Finding Rentals for Product')
        for item in db.rentals.find({'product_id': product_id}):
            rental_info = {'name': item['name'], 'rental_id': item['rental_id'],
                           'address': item['address'], 'phone_number': item['phone_number'],
                           'email': item['email']}
            rental_data[item['user_id']] = rental_info
        return rental_data


def clear_data():
    """ Clears Entire Database """
    mongo = MongodbConnection()

    with mongo:
        LOGGER.info('Connecting to Database')
        db = mongo.connection.media
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()


if __name__ == '__main__':
    clear_data()
    import_products('D:\\UW\\PY220\\Assignments\\lesson10', 'products.csv')
    import_customers('D:\\UW\\PY220\\Assignments\\lesson10', 'customers.csv')
    import_rentals('D:\\UW\\PY220\\Assignments\\lesson10', 'rentals.csv')
