'''
    sp_py220 assignment 5, consuming api's with MongoDB
'''

#pylint: disable=too-many-statements
#pylint: disable=invalid-name
#pylint: disable=too-many-locals

import csv
import os
import logging
from pymongo import MongoClient

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class MongoDBConnection():
    """ MongoDB Connection """
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
        des:
            read 3 csv data files and insert data into mongo db
        in:
            path to csv, products file, customers file, rentals files
        out:
            tuple total records count, errors count
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

                    for data in product: #check for empty data error
                        if data == '':
                            product_errors += 1
        except FileNotFoundError:
            LOGGER.error('Cannot find product_file')
            LOGGER.debug('Make sure directory and file name are entered correctly')
            product_errors += 1


    record_count = (product_count, customer_count, rental_count)
    errors_occurred = (product_errors, customer_errors, rental_errors)
    return record_count, errors_occurred

def show_available_products():
    pass

def show_rentals(product_id):
    pass

def dbs_cleanup():
    '''drop the db'''
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        database["Customers"].drop()
        database["Products"].drop()
        database["Rentals"].drop()
    return 'databases dropped'
