'''
    Assignment 5, MongoDB

    pylint Disable=too-many-locals, too-many-statements
'''
import csv
import os
import logging
from pymongo import MongoClient

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

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


def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
        This function takes a directory name three csv files as input, one with
        product data, one with customer data and the third one with rentals data
        and creates and populates a new MongoDB database with these data.

        It returns 2 tuples: the first with a record count of the number of
        products, customers and rentals added (in that order), the second with a
        count of any errors that occurred, in the same order.
    '''
    product_count = 0
    customer_count = 0
    rental_count = 0

    product_errors = 0
    customer_errors = 0
    rental_errors = 0

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        product_collection = database["Products"]
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   directory_name, product_file)) as csvfile:
                product_file = csv.reader(csvfile)

                for product in product_file:
                    product_info = {'product_id': product[0],
                                    'description': product[1],
                                    'product_type': product[2],
                                    'quantity_available': product[3]}
                    product_collection.insert_one(product_info)
                    product_count += 1

                    for data in product: #check for data omissions/'errors'
                        if data == '':
                            product_errors += 1
        except FileNotFoundError:
            LOGGER.error('Cannot find product_file')
            LOGGER.debug('Make sure directory and file name are entered correctly')
            product_errors += 1


        customer_collection = database["Customers"]
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   directory_name, customer_file)) as csvfile:
                customer_file = csv.reader(csvfile)

                for customer in customer_file:
                    customer_info = {'user_id': customer[0],
                                     'name': customer[1],
                                     'address': customer[2],
                                     'phone_number': customer[3],
                                     'email': customer[4]}
                    customer_collection.insert_one(customer_info)
                    customer_count += 1

                    for data in customer: #check for data omissions/'errors'
                        if data == '':
                            customer_errors += 1
        except FileNotFoundError:
            LOGGER.error('Cannot find customer_file')
            LOGGER.debug('Make sure directory and file name are entered correctly')
            customer_errors += 1


        rental_collection = database["Rentals"]
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   directory_name, rentals_file)) as csvfile:
                rentals_file = csv.reader(csvfile)

                for rental in rentals_file:
                    rental_info = {'user_id': rental[0],
                                   'name': rental[1],
                                   'rentals': rental[2]}
                    rental_collection.insert_one(rental_info)
                    rental_count += 1

                    for data in rental: #check for data omissions/'errors'
                        if data == '':
                            rental_errors += 1
        except FileNotFoundError:
            LOGGER.error('Cannot find rentals_file')
            LOGGER.debug('Make sure directory and file name are entered correctly')
            rental_errors += 1


    record_count = (product_count, customer_count, rental_count)
    errors_occurred = (product_errors, customer_errors, rental_errors)
    return record_count, errors_occurred


def show_available_products():
    '''
        Returns a Python dictionary of products listed as available with the
        following fields: product_id,
                          description,
                          product_type,
                          quantity_available
    '''
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        product_collection = database["Products"]
        py_dict = {}
        for product in product_collection.find():
            if product['quantity_available'] == '0':
                continue
            elif product['quantity_available'] == '':
                continue
            else:
                py_dict[product['product_id']] = dict([('description',
                                                        product['description']),
                                                       ('product_type',
                                                        product['product_type']),
                                                       ('quantity_available',
                                                        product['quantity_available'])])
        return py_dict


def show_rentals(product_id):
    '''
        Returns a Python dictionary with the following user information from
        users that have rented products matching product_id: user_id,
                                                             name,
                                                             address,
                                                             phone_number,
                                                             email
    '''
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        customer_collection = database["Customers"]
        rental_collection = database["Rentals"]
        py_dict = {}
        for renter in rental_collection.find():
            if product_id in renter['rentals']:
                for customer in customer_collection.find():
                    if renter['user_id'] == customer['user_id']:
                        py_dict[customer['user_id']] = dict([('name',
                                                              customer['name']),
                                                             ('address',
                                                              customer['address']),
                                                             ('phone_number',
                                                              customer['phone_number']),
                                                             ('email',
                                                              customer['email'])])
        return py_dict


def drop_dbs():
    '''deletes all entries made to the database'''
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        database["Customers"].drop()
        database["Products"].drop()
        database["Rentals"].drop()
    return 'Databases have been dropped'
