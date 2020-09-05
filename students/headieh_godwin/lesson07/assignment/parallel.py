#!/usr/bin/env python3
'''Adds csv file to a MongoDB database'''
#https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/
import logging
import csv
import time
import os
import threading
from queue import Queue
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

def import_products(directory_name, product_file):
    '''Populate MongoDB database '''
    product_error = 0
    product_file_path = os.path.join(directory_name, product_file)
    attempts = 0

    mongo = MongoDBConnection()
    with mongo:
        data_base = mongo.connection.hpn
        products = data_base['products']
        initial = data_base.products.count_documents({})

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
                except NameError:
                    LOGGER.info('Error adding product to database')
                    product_error += 1
    except FileNotFoundError:
        LOGGER.info('Product file not found.')
        product_error += 1

    p_end = time.time()
    p_time = (p_end-p_start)

    OUTPUT_QUEUE.put(
        (attempts, initial, data_base.products.count_documents({}), p_time),
        product_error, 'product_results')



def import_customers(directory_name, customer_file):
    '''Populate MongoDB database '''
    customer_error = 0
    customer_file_path = os.path.join(directory_name, customer_file)
    attempts = 0

    mongo = MongoDBConnection()
    with mongo:
        data_base = mongo.connection.hpn
        customers = data_base['customers']
        initial = data_base.customers.count_documents({})

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
                except NameError:
                    LOGGER.info('Error adding customer to database')
                    customer_error += 1
    except FileNotFoundError:
        LOGGER.info('Customer file not found.')
        customer_error += 1

    c_end = time.time()
    c_time = (c_end-c_start)

    OUTPUT_QUEUE.put(
        (attempts, initial, data_base.customers.count_documents({}), c_time),
        customer_error, 'customer_results')

def import_rentals(directory_name, rentals_file):
    '''Populate MongoDB database '''
    rental_error = 0
    rentals_file_path = os.path.join(directory_name, rentals_file)
    attempts = 0

    mongo = MongoDBConnection()
    with mongo:
        data_base = mongo.connection.hpn
        rentals = data_base['rentals']
        initial = data_base.rentals.count_documents({})

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
                    LOGGER.info('Rentals added!')
                except NameError:
                    LOGGER.info('Error adding rentals to database')
                    rental_error += 1
    except FileNotFoundError:
        LOGGER.info('Rentals file not found.')
        rental_error += 1
    r_end = time.time()
    r_time = (r_end-r_start)

    OUTPUT_QUEUE.put(
        (attempts, initial, data_base.rentals.count_documents({}), r_time),
        rental_error, 'rental_results')








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
    T_START = time.time()

    OUTPUT_QUEUE = Queue()
    THREADS = []

    THREADS.append(threading.Thread(target=import_products,
                                    args=(os.getcwd(), 'data/products.csv'), daemon=True))

    THREADS.append(threading.Thread(target=import_customers,
                                    args=(os.getcwd(), 'data/customers.csv'), daemon=True))

    THREADS.append(threading.Thread(target=import_rentals,
                                    args=(os.getcwd(), 'data/rentals.csv'), daemon=True))

    for thread in THREADS:
        thread.start()
    for thread in THREADS:
        thread.join()
    T_END = time.time()
    print(THREADS)
    print("total time")
    print(T_END - T_START)
