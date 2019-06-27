"""
A module that inputs data into a MongoDB database without running in parallel.
"""

#pylint: disable=too-many-statements
#pylint: disable=invalid-name
#pylint: disable=too-many-locals

import logging
import csv
import os
import time
from pymongo import errors as pyerror
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

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

def import_products(directory_name, filename):
    prod_start = time.time()
    error_prod = 0
    file_path = os.path.join(directory_name, filename)
    num_attempts = 0

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton
        products = db['products']
        initial_num = db.products.count_documents({})

        try:
            with open(file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    num_attempts += 1
                    prod_add = {'_id': row['_id'],
                                'description': row['description'],
                                'product_type': row['product_type'],
                                'quantity_available': row['quantity_available']}
                    try:
                        products.insert_one(prod_add)
                        #LOGGER.info('Added product to the database.')
                    except pyerror.DuplicateKeyError as error:
                        #LOGGER.info(error)
                        #LOGGER.info('Error adding product to database.')
                        error_prod += 1
        except FileNotFoundError:
            LOGGER.info('Product file not found')
            error_prod += 1
    prod_end = time.time()

    return (num_attempts, initial_num, db.products.count_documents({}),
            prod_end-prod_start), error_prod


def import_customers(directory_name, filename):
    cust_start = time.time()
    error_cust = 0
    file_path = os.path.join(directory_name, filename)
    num_attempts = 0

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton
        customers = db['customers']
        initial_num = db.customers.count_documents({})

        try:
            with open(file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    num_attempts += 1
                    cust_add = {'_id': row['_id'],
                                'name': row['name'],
                                'address': row['address'],
                                'phone_number': row['phone_number'],
                                'email': row['email']}
                    try:
                        customers.insert_one(cust_add)
                        #LOGGER.info('Added customer to the database.')
                    except pyerror.DuplicateKeyError as error:
                        #LOGGER.info(error)
                        #LOGGER.info('Error adding customer to database.')
                        error_cust += 1
        except FileNotFoundError:
            LOGGER.info('Customer file not found')
            error_cust += 1
    cust_end = time.time()

    return (num_attempts, initial_num, db.customers.count_documents({}),
            cust_end-cust_start), error_cust

def import_rentals(directory_name, filename):
    rent_start = time.time()
    error_rent = 0
    file_path = os.path.join(directory_name, filename)
    num_attempts = 0

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton
        rentals = db['rentals']
        initial_num = db.rentals.count_documents({})

        try:
            with open(file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    num_attempts += 1
                    rental_add = {'_id': row['_id'],
                                  'product_id': row['product_id'],
                                  'user_id': row['user_id']}
                    try:
                        rentals.insert_one(rental_add)
                        #LOGGER.info('Added rental to the database.')
                    except pyerror.DuplicateKeyError as error:
                        #LOGGER.info(error)
                        #LOGGER.info('Error adding rental to database.')
                        error_rent += 1
        except FileNotFoundError:
            LOGGER.info('Rental file not found')
            error_rent += 1
    rent_end = time.time()

    return (num_attempts, initial_num, db.rentals.count_documents({}),
            rent_end-rent_start), error_rent

def show_available_products():
    """
    Return a python dictionary of products listed available based on a
    field 'quantity availalble' that stores an integrer count of
    products available.
    """
    mongo = MongoDBConnection()
    avail_prod = {}
    with mongo:
        db = mongo.connection.hp_norton
        for prod in db.products.find({'quantity_available': {'$gt': '0'}}):
            prod_info = {'description': prod['description'],
                         'product_type': prod['product_type'],
                         'quantity_available': prod['quantity_available']}
            avail_prod[prod['_id']] = prod_info

    return avail_prod

def show_rentals(product_id):
    """
    Return a dictionary with user information from users that have
    rented products matching the product_id.
    """
    mongo = MongoDBConnection()
    rental_list = {}
    with mongo:
        db = mongo.connection.hp_norton
        for cust in db.rentals.find({'product_id': product_id}):
            for person in db.customers.find({'_id': cust['user_id']}):
                entry = {'name': person['name'],
                         'address': person['address'],
                         'phone_number': person['phone_number'],
                         'email': person['email']}
                rental_list[person['_id']] = entry

    return rental_list

def drop_all():
    """Clear all collections in database"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton
        LOGGER.info('Clearing database...')
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()
        LOGGER.info('Database Clear')

if __name__ == '__main__':
    linear_start = time.time()
    path = ('C:\\users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\students\\'
            'chris_lombardi\\Lesson07\\assignment\\data')
    product_info = import_products(path, 'products.csv')
    customer_info = import_customers(path, 'customers.csv')
    #rental_info = import_rentals(path, 'rentals.csv')
    linear_end = time.time()

    print('---Product Data and Timing---')
    print(product_info)
    print('---Customer Data and Timing---')
    print(customer_info)
    print('Total Time =', linear_end-linear_start)
