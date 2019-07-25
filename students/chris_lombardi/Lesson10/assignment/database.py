"""Module to add furniture data to a MongoDB database."""

#pylint: disable=R0201, R0913, C0103, R0914, R0915

import logging
import csv
import os
import datetime
import types
from pymongo import errors as pyerror
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def func_timer(func):
    """Function used to add timing to any function  passed in as a parameter"""
    def timer_data(*args, **kwargs):
        """Finds all functions in a class and outputs timing info to a file"""
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()

        counts = (db_store.products.count_documents({}), db_store.customers.count_documents({}),
                  db_store.rentals.count_documents({}))

        with open('timings.txt', mode='a+') as file:
            file.write('Function: {}, Time: {}, Records: {}\n'.format(func.__name__,
                                                                      end_time-start_time,
                                                                      counts))
        return result
    return timer_data

class DBTimer(type):
    """
    Metaclass for adding timing of methods within a database interaction class
    """

    def __new__(cls, clsname, bases, _dict):
        print(_dict)
        for attr, value in _dict.items():
            if isinstance(value, types.FunctionType):
                _dict[attr] = func_timer(value)
        return super(DBTimer, cls).__new__(cls, clsname, bases, _dict)

class TimedDBActions(metaclass=DBTimer):
    """Class for all of actions performed on the hp_norton database"""

    def import_data(self, directory_name, db, product_file, customer_file, rentals_file):
        """
        Take three *.csv files as input and populate a new MongoDB database.

        params:
        directory name: name of Database
        product_file: file with product data
        customer_file: file with customer data
        retnals_file: file with rental data

        return:
        record_count = tuple with counts of products, customers, and rentals added
        fail_count = tuple with counts of failed adds of products, customers, and rentals.
        """
        # Variables for counting the number of errors raised when importing data.
        error_prod, error_cust, error_rentals = 0, 0, 0
        product_file_path = os.path.join(directory_name, product_file)
        customer_file_path = os.path.join(directory_name, customer_file)
        rentals_file_path = os.path.join(directory_name, rentals_file)

        # A collection of products in the database.
        products = db['products']
        # A collection of customers in the database.
        customers = db['customers']
        # A collection of rentals in the database.
        rentals = db['rentals']

        # Import product data file into database.
        try:
            with open(product_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    prod_add = {'_id': row['_id'],
                                'description': row['description'],
                                'product_type': row['product_type'],
                                'quantity_available': row['quantity_available']}
                    try:
                        products.insert_one(prod_add)
                        LOGGER.info('Added product to the database.')
                    except pyerror.DuplicateKeyError as error:
                        LOGGER.info(error)
                        LOGGER.info('Error adding product to database.')
                        error_prod += 1
        except FileNotFoundError:
            LOGGER.info('Product file not found')
            error_prod += 1

        # Import customer data file into database.
        try:
            with open(customer_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cust_add = {'_id': row['_id'],
                                'name': row['name'],
                                'address': row['address'],
                                'phone_number': row['phone_number'],
                                'email': row['email']}
                    try:
                        customers.insert_one(cust_add)
                        LOGGER.info('Added customer to the database.')
                    except pyerror.DuplicateKeyError as error:
                        LOGGER.info(error)
                        LOGGER.info('Error adding customer to the database.')
                        error_cust += 1
        except FileNotFoundError:
            LOGGER.info('Customer file not found')
            error_cust += 1

        # Import rental data file into database.
        try:
            with open(rentals_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rental_add = {'_id': row['_id'],
                                  'product_id': row['product_id'],
                                  'user_id': row['user_id']}
                    try:
                        rentals.insert_one(rental_add)
                        LOGGER.info('Added rental to the database.')
                    except pyerror.DuplicateKeyError as error:
                        LOGGER.info(error)
                        LOGGER.info('Error adding rental to database.')
                        error_rentals += 1
        except FileNotFoundError:
            LOGGER.info('Rental file not found')
            error_rentals += 1

        record_count = (products.count_documents({}), customers.count_documents({}),
                        rentals.count_documents({}))
        total_errors = (error_prod, error_cust, error_rentals)

        return record_count, total_errors

    def show_available_products(self, db):
        """
        Return a python dictionary of products listed available based on a
        field 'quantity availalble' that stores an integrer count of
        products available.
        """
        avail_prod = {}
        for prod in db.products.find({'quantity_available': {'$gt': '0'}}):
            prod_info = {'description': prod['description'],
                         'product_type': prod['product_type'],
                         'quantity_available': prod['quantity_available']}
            avail_prod[prod['_id']] = prod_info

        return avail_prod

    def show_rentals(self, db, product_id):
        """
        Return a dictionary with user information from users that have
        rented products matching the product_id.
        """
        rental_list = {}
        for cust in db.rentals.find({'product_id': product_id}):
            for person in db.customers.find({'_id': cust['user_id']}):
                entry = {'name': person['name'],
                         'address': person['address'],
                         'phone_number': person['phone_number'],
                         'email': person['email']}
                rental_list[person['_id']] = entry

        return rental_list

    def drop_all(self, db):
        """Clear all collections in database"""
        LOGGER.info('Clearing database...')
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()
        LOGGER.info('Database Clear')

if __name__ == '__main__':
    PATH = ('C:\\users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\students\\'
            'chris_lombardi\\Lesson10\\assignment\\')
    host = '127.0.0.1'
    port = 27017
    connection = MongoClient(host, port)
    with connection:
        # Database containing all customer, product, and rental info
        db_store = connection.hp_norton

        db_timed = TimedDBActions()

        # Functions to be run with timing output to file
        db_timed.import_data(PATH, db_store, 'products.csv', 'customers.csv', 'rentals.csv')
        db_timed.show_available_products(db_store)
        db_timed.show_rentals(db_store, 'prd001')
        db_timed.drop_all(db_store)
