"""Imports csv files with HP Norton data, rentals will show and
available products will show"""

#pylint: disable=too-many-statements
#pylint: disable=invalid-name
#pylint: disable=too-many-locals
#pylint: disable=R0201,R0913,W0612

import logging
import csv
import os
import types
import datetime
from pymongo import errors as pyerror
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def func_timer(func):
    """Function used to add timing to any function  passed in as a parameter"""
    def timer_data(*args, **kwargs):
        """Finds all functions in a class and outputs timing info to a file"""
        start_time = datetime.datetime.now()
        pre_counts = (db_total.products.count_documents({}), db_total.customers.count_documents({}),
                      db_total.rentals.count_documents({}))
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        post_counts = (db_total.products.count_documents({}),
                       db_total.customers.count_documents({}),
                       db_total.rentals.count_documents({}))
        counts = (abs(post_counts[0]-pre_counts[0]), abs(post_counts[1]-pre_counts[1]),
                  abs(post_counts[2]-pre_counts[2]))

        with open('timings.txt', mode='a+') as file:
            file.write('Function: {}, Time: {}, Records Processed: {}\n'.format(func.__name__,
                                                                                end_time-start_time,
                                                                                counts))
        return result
    return timer_data

class DBT(type):
    """MongoDB Connection"""
    # overriding __new__ method
    def __new__(cls, clsname, bases, clsdict):
        for attr, value in clsdict.items():
            if isinstance(value, types.FunctionType):
                clsdict[attr] = func_timer(value)
        return super(DBT, cls).__new__(cls, clsname, bases, clsdict)

class TimedDB(metaclass=DBT):
    """Class for all of actions performed on the hp_norton database"""

    def import_data(self, db, directory_name, product_file, customer_file, rental_file):
        """
        Take three *.csv files as input and populate a new MongoDB database.

        params:

        directory name: path to the database
        product_file: file with product data
        customer_file: file with customer data
        retnals_file: file wit rental data

        return:
        record_count = tuple with counts of products, customers, and rentals added
        fail_count = tuple with counts of failed adds of products, customers, and rentals.
        """
        # Variables for counting the number of errors raised when importing data.
        error_prod, error_cust, error_rentals = 0, 0, 0
        product_file_path = os.path.join(directory_name, product_file)
        customer_file_path = os.path.join(directory_name, customer_file)
        rental_file_path = os.path.join(directory_name, rental_file)
        #A collection of products, customers, rentals in the database
        products = db['products']
        customers = db['customers']
        rentals = db['rentals']

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
                        #LOGGER.info('Added product to the database')
                    except pyerror.DuplicateKeyError as error:
                        #LOGGER.info(error)
                        #LOGGER.info('Product already in database')
                        error_prod += 1

        except FileNotFoundError:
            #LOGGER.info('Product file not found')
            error_prod += 1

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
                        #LOGGER.info('Added customer to the database')
                    except pyerror.DuplicateKeyError as error:
                        #LOGGER.info(error)
                        #LOGGER.info('customer already in database')
                        error_cust += 1

        except FileNotFoundError:
            #LOGGER.info('Customer file not found')
            error_cust += 1

        try:
            with open(rental_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rent_add = {'_id': row['_id'],
                                'product_id': row['product_id'],
                                'user_id': row['user_id']}
                    try:
                        rentals.insert_one(rent_add)
                        #LOGGER.info('Added rental to the database')
                    except pyerror.DuplicateKeyError as error:
                        #LOGGER.info(error)
                        #LOGGER.info('Rental already in database')
                        error_rentals += 1

        except FileNotFoundError:
            #LOGGER.info('Rental file not found')
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

    def clear(self, db):
        """Clear all collections in database"""
        #LOGGER.info('Clearing database...')
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()
        #LOGGER.info('Database Clear')

if __name__ == '__main__':
    PATH = ('/Users/nicholaslenssen/Desktop/Python/Py220/SP_Python220B_2019/'
            'students/Nick_Lenssen/lesson10/assignment')
    host = '127.0.0.1'
    port = 27017
    connection = MongoClient(host, port)
    with connection:
        db_total = connection.hp_norton
        db_timed = TimedDB()
        # Functions to be run with timing output to file
        db_timed.import_data(db_total, PATH, 'products.csv', 'customers.csv', 'rentals.csv')
        db_timed.show_available_products(db_total)
        db_timed.show_rentals(db_total, 'prd001')
        db_timed.clear(db_total)
