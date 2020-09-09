#!/usr/bin/env python3
'''Adds csv file to a MongoDB database'''

import logging
import csv
import os
import types
import datetime
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def func_timer(func):
    """Function to add timing to any function"""
    def timer_data(*args, **kwargs):
        """Finds all functions in class and outputs timing info to timings.txt"""
        start_time = datetime.datetime.now()
        counts_before = (DB.products.count_documents({}),
                         DB.customers.count_documents({}),
                         DB.rentals.count_documents({}))
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        counts_after = (DB.products.count_documents({}),
                        DB.customers.count_documents({}),
                        DB.rentals.count_documents({}))
        counts = (abs(counts_after[0]-counts_before[0]),
                  abs(counts_after[1]-counts_before[1]),
                  abs(counts_after[2]-counts_before[2]))
        with open('timings.txt', mode='a+') as file:
            if func.__name__ == 'import_data':
                file.write('Function: {}\n Time: {}\n Records Processed: {}\n'.
                           format(func.__name__, end_time-start_time, counts))
            if func.__name__ != 'import_data':
                file.write('Function: {}\n Time: {}\n'.
                           format(func.__name__, end_time-start_time))
        return result
    return timer_data
#https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python
#https://uwpce-pythoncert.github.io/PythonCertDevel220/modules/lesson10/content.html
class DBT(type):
    """MongoDB Connection"""
    def __new__(cls, clsname, bases, clsdict):
        for attr, value in clsdict.items():
            if isinstance(value, types.FunctionType):
                clsdict[attr] = func_timer(value)
        return super(DBT, cls).__new__(cls, clsname, bases, clsdict)

class TimedDB(metaclass=DBT):
    """Class for all of actions performed on the hpn database"""
    #@classmethod cls
    def import_data(self, data_base, directory_name, product_file,
                    customer_file, rentals_file):
        '''
        Populate new MongoDB database using the three csv file inputs.
        Returns record count of (# of products, customers, rentals) and
        count of (# of product errors, customers errors, rentals errors)
        '''
        product_error = 0
        customer_error = 0
        rental_error = 0
        product_count = 0
        customer_count = 0
        rental_count = 0
        product_file_path = os.path.join(directory_name, product_file)
        customer_file_path = os.path.join(directory_name, customer_file)
        rentals_file_path = os.path.join(directory_name, rentals_file)
        products = data_base['products']
        customers = data_base['customers']
        rentals = data_base['rentals']

        # Attempt to import product data file into MongoDB db, create product collection
        try:
            with open(product_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    add_product = {'product_id': row['product_id'],
                                   'description': row['description'],
                                   'product_type': row['product_type'],
                                   'quantity_available': row['quantity_available']}
                    try:
                        products.insert_one(add_product)
                        #LOGGER.info('Product added!')
                        product_count += 1
                    except NameError:
                        #LOGGER.info('Error adding product to database')
                        product_error += 1
        except FileNotFoundError:
            LOGGER.info('Product file not found.')
            product_error += 1
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
                        #LOGGER.info('Customer added!')
                        customer_count += 1
                    except NameError:
                        #LOGGER.info('Error adding customer to database')
                        customer_error += 1
        except FileNotFoundError:
            LOGGER.info('Customer file not found.')
            customer_error += 1
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
                        #LOGGER.info('Rentals added!')
                    except NameError:
                        #LOGGER.info('Error adding rentals to database')
                        rental_error += 1
        except FileNotFoundError:
            LOGGER.info('Rentals file not found.')
            rental_error += 1
        record_count = (product_count, customer_count, rental_count)
        error_count = (product_error, customer_error, rental_error)

        return record_count, error_count

    #@classmethod cls
    def show_available_products(self, data_base):
        '''Return a dictionary of products listed as available'''
        available_products = {}
        for each in data_base.products.find({'quantity_available': {'$gt': '0'}}):
            # ''$gt' selects those documents where the value of the field
            # is greater than specfied value ie 'not available'
            product_info = {'description': each['description'],
                            'product_type': each['product_type'],
                            'quantity_available': each['quantity_available']}
            available_products[each['product_id']] = product_info
        return available_products

    #@classmethod cls
    def show_rentals(self, data_base, product_id):
        '''Return a dictionary with info from users that have rented with the product id'''
        rental_list = {}
        for each in data_base.rentals.find({'product_id': product_id}):
            for pers in data_base.customers.find({'customer_id': each['customer_id']}):
                rental_list[pers['customer_id']] = {'firstname': pers['firstname'],
                                                    'lastname': pers['lastname'],
                                                    'address': pers['address'],
                                                    'phone_number': pers['phone_number'],
                                                    'email': pers['email']}
        return rental_list


    def clear_all(self, data_base):
        """Clear all collections in database"""
        data_base.products.drop()
        data_base.customers.drop()
        data_base.rentals.drop()

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 27017
    CONNECTION = MongoClient(HOST, PORT)
    with CONNECTION:
        DB = CONNECTION.hpn
        TIMED_DB = TimedDB()
        TIMED_DB.clear_all(DB)
        TIMED_DB.import_data(DB, os.getcwd(),
                             'data/products_expanded.csv',
                             'data/customers_expanded.csv',
                             'data/rentals_expanded.csv')
        TIMED_DB.import_data(DB, os.getcwd(),
                             'data/products.csv',
                             'data/customers.csv',
                             'data/rentals.csv')
        TIMED_DB.show_available_products(DB)
        TIMED_DB.show_rentals(DB, 'p1')
