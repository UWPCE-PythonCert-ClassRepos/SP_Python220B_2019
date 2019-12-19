# pylint: disable=R0914, C0103
'''
Mongo DB assignment
'''
import csv
import os
import logging
import time
from pymongo import MongoClient

#logging setup
log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(log_format)
file_handler = logging.FileHandler('timings.txt')
file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

def timer(func):
    '''timer decorator function'''
    def timed(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        time_elapsed = time.time() - start_time
        logging.info('%s took %.3f seconds to run', func.__name__, time_elapsed)
        return result
    return timed


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

@timer
def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    Function takes a directory name and three csv files as input (product data,
    customer data, rentals data) and creates a MongoDB database.
    Returns 2 tuples:
    1) Record count of number of products, customers and rentals added
    2) A count with any errors that occured in same order
    '''
    product_added = 0
    customer_added = 0
    rentals_added = 0

    product_errors = 0
    customer_errors = 0
    rental_errors = 0

    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        #Create product collection
        product_db = db['product']
        #only use drop for resetting database
        #product_db.drop()
        try:
            with open(os.path.join(directory_name, product_file)) as csvfile:
                product_reader = csv.DictReader(csvfile)
                for row in product_reader:
                    product_added += 1
                    new_product = {'product_id':row['product_id'],
                                   'description':row['description'],
                                   'product_type':row['product_type'],
                                   'quantity_available':row['quantity_available']}
                    #LOGGER.info('%s added to database', new_product['product_id'])
                    product_db.insert_one(new_product)
        except FileNotFoundError:
            product_errors += 1

        #Create customer collection
        customer_db = db['customer']
        #only use drop for resetting database
        #customer_db.drop()
        try:
            with open(os.path.join(directory_name, customer_file)) as csvfile:
                customer_reader = csv.DictReader(csvfile)
                for row in customer_reader:
                    customer_added += 1
                    new_customer = {'user_id':row['user_id'],
                                    'name':row['name'],
                                    'address':row['address'],
                                    'phone_number':row['phone_number'],
                                    'email':row['email']}
                    #LOGGER.info('%s added to database', new_customer['user_id'])
                    customer_db.insert_one(new_customer)
        except FileNotFoundError:
            customer_errors += 1

        #Create rentals collection
        rentals_db = db['rentals']
        #only use drop for resetting database
        #rentals_db.drop()
        try:
            with open(os.path.join(directory_name, rentals_file)) as csvfile:
                rental_reader = csv.DictReader(csvfile)
                for row in rental_reader:
                    rentals_added += 1
                    new_rental = {'user_id':row['user_id'],
                                  'product_id':row['product_id']}
                    #LOGGER.info('%s rental added to database', new_rental['product_id'])
                    rentals_db.insert_one(new_rental)
        except FileNotFoundError:
            rental_errors += 1

    return [(product_added, customer_added, rentals_added),
            (product_errors, customer_errors, rental_errors)]

@timer
def show_available_products():
    '''returns a dict of products listed as available with fields:
    product_id, description, product_type, quantity available'''

    mongo = MongoDBConnection()

    product_dict = {}
    with mongo:
        db = mongo.connection.media
        product_db = db['product']
        avail_product = product_db.find({'quantity_available': {'$gt': '0'}})
        for item in avail_product:
            product_dict[item['product_id']] = {'description': item['description'],
                                                'product_type': item['product_type'],
                                                'quantity_available': item['quantity_available']}
    return product_dict

@timer
def show_rentals(product_id):
    '''returns a dict with the info from users who rented matching product_id:
    user_id, name, address, phone_number, email'''

    mongo = MongoDBConnection()

    rentals_dict = {}
    with mongo:
        db = mongo.connection.media
        customer_db = db['customer']
        rentals_db = db['rentals']
        for renter in rentals_db.find({'product_id': product_id}):
            for customer in customer_db.find({'user_id': renter['user_id']}):
                rentals_dict[customer['user_id']] = {'name': customer['name'],
                                                     'address': customer['address'],
                                                     'phone_number': customer['phone_number'],
                                                     'email': customer['email']}
    return rentals_dict

def clear_db():
    '''func to clear database of entries'''
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        product_db = db['product']
        customer_db = db['customer']
        rentals_db = db['rentals']
        product_db.drop()
        customer_db.drop()
        rentals_db.drop()

if __name__ == "__main__":
    clear_db()
    DIR_NAME = input('Directory name: ')
    PRODUCT_FILE = input('Product file: ')
    CUSTOMER_FILE = input('Customer file: ')
    RENTAL_FILE = input('Rental file: ')
    RECORDS_IMPORTED = input('Approx. number of records importing?: ')
    logging.info('Approximate number of records processed: %s', RECORDS_IMPORTED)
    import_data(DIR_NAME, PRODUCT_FILE, CUSTOMER_FILE, RENTAL_FILE)
    show_available_products()
    show_rentals('prd002')
