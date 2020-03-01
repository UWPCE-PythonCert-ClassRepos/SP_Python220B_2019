"""Imports csv files with HP Norton data, rentals will show and
available products will show"""

#pylint: disable=too-many-statements
#pylint: disable=invalid-name
#pylint: disable=too-many-locals

import logging
import time
import threading
import csv
import os
from queue import Queue
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

def import_products(directory_name, product_file):
    prod_start = time.time()
    error_prod = 0
    product_file_path = os.path.join(directory_name, product_file)
    mongo = MongoDBConnection()
    num_prod_processed = 0
    with mongo:
        db = mongo.connection.hp_norton
        #A collection of products, customers, rentals in the database
        products = db['products']
        db_prod_init_count = db.products.count_documents({})
        try:
            with open(product_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    num_prod_processed += 1
                    prod_add = {'_id': row['_id'],
                                'description': row['description'],
                                'product_type': row['product_type'],
                                'quantity_available': row['quantity_available']}
                    try:
                        products.insert_one(prod_add)
                        LOGGER.info('Added product to the database')
                    except pyerror.DuplicateKeyError as error:
                        LOGGER.info(error)
                        LOGGER.info('Product already in database')
                        error_prod += 1

        except FileNotFoundError:
            LOGGER.info('Product file not found')
            error_prod += 1
        db_prod_after_count = db.products.count_documents({})
        prod_end = time.time()

        output_queue.put((num_prod_processed, db_prod_init_count, db_prod_after_count, prod_end-prod_start), error_prod)
def import_customers(directory_name, customer_file):
    cust_start = time.time()
    error_cust = 0
    customer_file_path = os.path.join(directory_name, customer_file)
    mongo = MongoDBConnection()
    num_cust_processed = 0
    print (customer_file_path)
    with mongo:
        db = mongo.connection.hp_nortion
        customers = db['customers']
        db_init_cust_count = db.customers.count_documents({})
        try:
            with open(customer_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    num_cust_processed += 1
                    cust_add = {'_id': row['_id'],
                                'name': row['name'],
                                'address': row['address'],
                                'phone_number': row['phone_number'],
                                'email': row['email']}
                    try:
                        customers.insert_one(cust_add)
                        LOGGER.info('Added customer to the database')
                    except pyerror.DuplicateKeyError as error:
                        LOGGER.info(error)
                        LOGGER.info('customer already in database')
                        error_cust += 1

        except FileNotFoundError:
            LOGGER.info('Customer file not found')
            error_cust += 1            
    db_after_cust_count = db.customers.count_documents({})
    cust_end = time.time()
    print (cust_end)
    output_queue.put((num_cust_processed, db_init_cust_count, db_after_cust_count, cust_end-cust_start), error_cust)

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

def clear():
    """Clear all collections in database"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton
        LOGGER.info('Clearing database...')
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()
        LOGGER.info('Database Clear')

if __name__ == "__main__":
    start_time = time.time()
    output_queue = Queue()
    storage = []
    threads = []
    path = ('/Users/nicholaslenssen/Desktop/Python/Py220/SP_Python220B_2019/'
                'students/Nick_Lenssen/lesson07/assignment/data')
    threads.append(threading.Thread(target = import_products, args = (path, 'products.csv'), daemon=True))
    threads.append(threading.Thread(target = import_customers, args = (path, 'customers.csv'), daemon=True))
    for thread in threads:
        thread.start() 
        storage.append(output_queue.get())
    stop_time = time.time()

    print ('Total time to run '+str(stop_time-start_time))
    #print (storage)


