#!/usr/bin/env python3
'''Adds csv file to a MongoDB database'''
#https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/
import logging
import csv
import time
import os
from pymongo import MongoClient

#too-many-locals,
#too-many-statements

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class MongoDBConnection():
    '''MongoDBConnection'''

    def __init__(self, host='127.0.0.1', port=27017):
        ''' be sure to use the ip address not name for local windows '''
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        '''Enters connection'''
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exits connection'''
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    Populate new MongoDB database using the three csv file inputs.
    Returns record count of (# of products, customers, rentals) and
    count of (# of product errors, customers errors, rentals errors)
    '''
    product_error, customer_error, rental_error, product_count, customer_count,\
    rental_count = 0, 0, 0, 0, 0, 0
    product_file_path = os.path.join(directory_name, product_file)
    customer_file_path = os.path.join(directory_name, customer_file)
    rentals_file_path = os.path.join(directory_name, rentals_file)

    mongo = MongoDBConnection()
    with mongo:
        data_base = mongo.connection.hpn
        # Create collections
        products = data_base['products']
        customers = data_base['customers']
        rentals = data_base['rentals']

    # Attempt to import product data file into MongoDB db, create product collection
    p_start = time.time()
    try:
        with open(product_file_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                add_product = {'product_id': row['product_id'],
                               'description': row['description'],
                               'product_type': row['product_type'],
                               'quantity_available': row['quantity_available']}
                try:
                    products.insert_one(add_product) # Fixed to use correct method
                    LOGGER.info('Product added!')
                    product_count += 1
                except NameError:
                    LOGGER.info('Error adding product to database')
                    product_error += 1
    except FileNotFoundError:
        LOGGER.info('Product file not found.')
        product_error += 1
    p_end = time.time()

    # Attempt to import customer data into the MongoDB db, create customer collection
    c_start = time.time()
    try:
        with open(customer_file_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                add_customer = {'customer_id': row['customer_id'],
                                'firstname': row['firstname'],
                                'lastname': row['lastname'],
                                'address': row['address'],
                                'phone_number': row['phone_number'],
                                'email': row['email']}
                try:
                    customers.insert_one(add_customer)
                    LOGGER.info('Customer added!')
                    customer_count += 1
                except NameError:
                    LOGGER.info('Error adding customer to database')
                    customer_error += 1
    except FileNotFoundError:
        LOGGER.info('Customer file not found.')
        customer_error += 1
    c_end = time.time()

    # Attempt to import rentals file into the MongoDB db, create rentals collection
    r_start = time.time()
    try:
        with open(rentals_file_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                add_rentals = {'rental_id': row['rental_id'],
                               'product_id': row['product_id'],
                               'customer_id': row['customer_id']}
                try:
                    rentals.insert_one(add_rentals)
                    rental_count += 1
                    LOGGER.info('Rentals added!')
                except NameError:
                    LOGGER.info('Error adding rentals to database')
                    rental_error += 1
    except FileNotFoundError:
        LOGGER.info('Rentals file not found.')
        rental_error += 1
    r_end = time.time()

    # Return the sum of each record type and the sum of each error in 2 tuples
    record_time = (p_end - p_start, c_end - c_start, r_end - r_start)
    record_count = (product_count, customer_count, rental_count)
    error_count = (product_error, customer_error, rental_error)

    return record_count, error_count, record_time
#
def show_available_products():
    '''Return a dictionary of products listed as available'''
    mongo = MongoDBConnection()
    available_products = {}
    with mongo:
        data_base = mongo.connection.hpn
        for each in data_base.products.find({'quantity_available': {'$gt': '0'}}):
            # ''$gt' selects those documents where the value of the field
            # is greater than specfied value ie 'not available'
            product_info = {'description': each['description'],
                            'product_type': each['product_type'],
                            'quantity_available': each['quantity_available']}
            available_products[each['product_id']] = product_info

    return available_products

def show_rentals(product_id):
    '''Return a dictionary with info from users that have rented with the product id'''
    mongo = MongoDBConnection()
    rental_list = {}
    with mongo:
        data_base = mongo.connection.hpn
        for each in data_base.rentals.find({'product_id': product_id}):
            for pers in data_base.customers.find({'customer_id': each['customer_id']}):
                rental_list[pers['customer_id']] = {'firstname': pers['firstname'],
                                                    'lastname': pers['lastname'],
                                                    'address': pers['address'],
                                                    'phone_number': pers['phone_number'],
                                                    'email': pers['email']}


    return rental_list

def clear_all():
    '''Clears all database collections'''
    mongo = MongoDBConnection()
    with mongo:
        data_base = mongo.connection.hpn

        data_base.products.drop()
        data_base.customers.drop()
        data_base.rentals.drop()
        LOGGER.info('Cleared all databases!')

if __name__ == '__main__':
    clear_all()
    t_start = time.time()
    data = import_data(os.getcwd(), 'data/products.csv', 'data/customers.csv', 'data/rentals.csv')
    t_end = time.time()
    print(data)
    print("total time")
    print(t_end - t_start)
