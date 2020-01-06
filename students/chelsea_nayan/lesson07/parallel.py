'''A module that inputs csv file data into MongoDB in parallel'''

# Return a list of tuples, one for customer and one for products
# Each tuple has 4 values:
# - The number of records processed (int)
# - The record count in the database prior to runnint (int)
# the record count after running (int)
# The time taken to run the module (float)

# pylint: disable=too-many-statements
# pylint: disable=invalid-name
# pylint: disable=too-many-locals

import logging
import csv
import os
import time
import threading
from queue import Queue
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

def import_products(directory_name, product_file):
    '''Populate MongoDB database '''
    p_start = time.time()
    product_error = 0
    product_file_path = os.path.join(directory_name, product_file)
    attempts = 0

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        products = db['products']
        initial_num = db.products.count_documents({})

    # Attempt to import product data file into MongoDB db, create product collection
    try:
        with open(product_file_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                attempts += 1
                add_product = {'p_id': row['p_id'],
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
    p_overall_time = p_end - p_start

    # print('-----Product Data Import Timing-----')
    # print(p_overall_time)

    output_queue.put((attempts, initial_num, db.products.count_documents({}),
                      p_overall_time), product_error, 'product_results')

def import_customers(directory_name, customer_file):
    '''Populate MongoDB database '''
    c_start = time.time()
    customer_error = 0
    customer_file_path = os.path.join(directory_name, customer_file)
    attempts = 0

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        customers = db['customers']
        initial_num = db.customers.count_documents({})

    # Attempt to import customer data file into MongoDB db, create customer collection
    try:
        with open(customer_file_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                attempts += 1
                add_customer = {'c_id': row['c_id'],
                                'name': row['name'],
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
    c_overall_time = c_end - c_start

    # print('-----Customer Data Import Timing-----')
    # print(c_overall_time)

    output_queue.put((attempts, initial_num, db.customers.count_documents({}),
                      c_overall_time), customer_error, 'customer_results')

def import_rentals(directory_name, rental_file):
    '''Populate MongoDB database'''
    r_start = time.time()
    rental_error = 0
    customer_file_path = os.path.join(directory_name, rental_file)
    attempts = 0

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        customers = db['rentals']
        initial_num = db.rentals.count_documents({})
    # Attempt to import product data file into MongoDB db, create product collection
    try:
        with open(customer_file_path, encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                attempts += 1
                add_rental = {'r_id': row['r_id'],
                              'p_id': row['p_id'],
                              'c_id': row['c_id']}
                try:
                    customers.insert_one(add_rental)
                    LOGGER.info('rental added!')
                except NameError:
                    LOGGER.info('Error adding rental to database')
                    rental_error += 1
    except FileNotFoundError:
        LOGGER.info('Customer file not found.')
        rental_error += 1

    r_end = time.time()
    r_overall_time = r_end - r_start

    # print('-----Rental Data Import Timing-----')
    # print(r_overall_time)

    output_queue.put((attempts, initial_num, db.rentals.count_documents({}),
                      r_overall_time), rental_error, 'rental_results')
#
def show_available_products():
    '''Return a dictionary of products listed as available'''
    mongo = MongoDBConnection()
    available_products = {}
    with mongo:
        db = mongo.connection.media
        for each in db.products.find({'quantity_available': {'$gt': '0'}}):
            # ''$gt' selects those documents where the value of the field
            # is greater than specfied value AKA 'not available'
            product_info = {'description': each['description'],
                            'product_type': each['product_type'],
                            'quantity_available': each['quantity_available']}
            available_products[each['p_id']] = product_info

    return available_products

def show_rentals(p_id):
    '''Return a dictionary with info from users that have rented with the product id'''
    mongo = MongoDBConnection()
    rental_list = {}
    with mongo:
        db = mongo.connection.media
        for each in db.rentals.find({'p_id': p_id}):
            for pers in db.customers.find({'c_id': each['c_id']}):
                rental_list[pers['c_id']] = {'name': pers['name'],
                                             'address': pers['address'],
                                             'phone_number': pers['phone_number'],
                                             'email': pers['email']}

    return rental_list

def clear_all():
    '''Clears all database collections'''
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media

        db.products.drop()
        db.customers.drop()
        db.rentals.drop()
        LOGGER.info('Cleared all databases!')

if __name__ == '__main__':
    parallel_start = time.time()
    path = ('C:\\Users\\chels\\SP_Python220B_2019\\students\\chelsea_nayan\\lesson07\\data')

    output_queue = Queue()
    #queue_storage = []
    threads = []

    threads.append(threading.Thread(target=import_products,
                                    args=(path, 'products.csv'), daemon=True))
    threads.append(threading.Thread(target=import_customers,
                                    args=(path, 'customers.csv'), daemon=True))
    threads.append(threading.Thread(target=import_rentals,
                                    args=(path, 'rentals.csv'), daemon=True))

    for thread in threads:
        thread.start()
        #queue_storage.append(output_queue.get())
    for thread in threads:
        thread.join()

    parallel_end = time.time()

    # print('-----Product Data Import Timing-----')
    # print(product_info)
    # print('-----Customer Data Import Timing-----')
    # print(customer_info)
    print('-----Total Time: importing customer, product, and rental data-----')
    print(parallel_end-parallel_start)
