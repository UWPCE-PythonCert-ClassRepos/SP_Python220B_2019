'''Converting CSV Files and Putting Them Into a Database'''

import csv
import os
import logging

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

        LOGGER.info('Finding CSV Files')
        product_file = os.path.join(directory_name, product_file)
        customer_file = os.path.join(directory_name, customer_file)
        rental_file = os.path.join(directory_name, rental_file)

        LOGGER.info('Adding Product file')
        product_errors = 0
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

        except FileNotFoundError:
            LOGGER.error('File Not Found.')
            product_errors += 1
            print('File %s Does Not Exist', product_file)

        LOGGER.info('Adding Customer file')
        customer_errors = 0
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

        except FileNotFoundError:
            LOGGER.error('File Not Found.')
            customer_errors += 1
            print('File %s Does Not Exist', customer_file)

        LOGGER.info('Adding Rental file')
        rental_errors = 0
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

        except FileNotFoundError:
            LOGGER.error('File Not Found.')
            rental_errors += 1
            print('File %s Does Not Exist', rental_file)

        LOGGER.info('Counting Added Items and Failed Items')
        total_count = (products.count_documents({}), customers.count_documents({}),
                       rentals.count_documents({}))

        total_errors = (product_errors, customer_errors, rental_errors)

        total = total_count, total_errors
        return total


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
