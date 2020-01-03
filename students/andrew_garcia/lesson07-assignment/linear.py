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


def import_data(directory_name, product_file, customer_file, rental_file):
    """ Takes directory name and three files, product data, customer data, and rentals data
    Creates a new Mongodb database with data

    Returns count of number of products, customers, and rentals added, and returns count of
    errors that happened
    """
    mongo = MongodbConnection()

    with mongo:
        LOGGER.info('Creating Database')
        db = mongo.connection.media
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()

        products = db['products']
        customers = db['customers']
        rentals = db['rentals']

        LOGGER.info('Adding Product file')
        product_start_time = time.time()
        product_file = os.path.join(directory_name, product_file)
        added_products = 0
        product_count_start = products.count_documents({})

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

        product_end_time = time.time()
        product_time = product_end_time - product_start_time
        product_count_end = products.count_documents({})
        product_details = (added_products, product_count_start, product_count_end, product_time)


        LOGGER.info('Adding Customer file')
        customer_start_time = time.time()
        customer_file = os.path.join(directory_name, customer_file)
        added_customers = 0
        customer_count_start = customers.count_documents({})

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
                    added_customers += 0

        except FileNotFoundError:
            LOGGER.error('File Not Found.')
            print('File %s Does Not Exist', customer_file)

        customer_end_time = time.time()
        customer_time = customer_end_time - customer_start_time
        customer_count_end = customers.count_documents({})
        customer_details = (added_customers, customer_count_start, customer_count_end,
                            customer_time)


        LOGGER.info('Adding Rental file')
        rental_start_time = time.time()
        rental_file = os.path.join(directory_name, rental_file)
        added_rentals = 0
        rental_count_start = rentals.count_documents({})

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

        rental_end_time = time.time()
        rental_time = rental_end_time - rental_start_time
        rental_count_end = rentals.count_documents({})
        rental_details = (added_rentals, rental_count_start, rental_count_end, rental_time)

        LOGGER.info('Getting Information about Imported Data')
        return product_details, customer_details, rental_details


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
