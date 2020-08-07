'''
    sp_py220 assignment 5, consuming api's with MongoDB
'''

#pylint: disable=too-many-statements
#pylint: disable=invalid-name
#pylint: disable=too-many-locals
#pylint: disable=no-else-continue

import sys
import csv
import os
import datetime
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

def db_get_metrics(db):
    time_metric = datetime.datetime.now()
    products_metric = db['Products'].estimated_document_count()
    customers_metric = db['Customers'].estimated_document_count()
    rentals_metric = db['Rentals'].estimated_document_count()
    lst_metrics = [time_metric, products_metric, customers_metric, rentals_metric]
    return lst_metrics

def measure_function(func):
    def wrapper(*args, **kwargs):
        print("{0} is called with parameter {1}".format(func.__qualname__, args[1:]))
        
        host = '127.0.0.1'
        port = 27017
        connection = MongoClient(host, port)
        db = connection.hp_norton

        lst_metrics_before = db_get_metrics(db)
        print("before metrics = " + str(lst_metrics_before))
        
        result = func(*args, **kwargs)

        lst_metrics_after = db_get_metrics(db)
        print("after metrics = " + str(lst_metrics_after))
        
        connection.close()

        start_time = lst_metrics_before[0]
        end_time = lst_metrics_after[0]
        post_counts = lst_metrics_after
        pre_counts = lst_metrics_before
        counts = (abs(post_counts[1]-pre_counts[1]), abs(post_counts[2]-pre_counts[2]),
                  abs(post_counts[3]-pre_counts[3]))
        
        with open('timings.txt', mode='a+') as file:
            file.write('Function: {}, Time: {}, Records Processed: {}\n'.format(func.__name__,
                                                                                end_time-start_time,
                                                                                counts))

        return result

    return wrapper


def measure_all_methods(cls):

    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, measure_function(val))
    return cls


class MetaClassMeasure(type):

    def __new__(cls, clsname, bases, clsdict):
        obj = super().__new__(cls, clsname, bases, clsdict)
        obj = measure_all_methods(obj)
        return obj


class MeasuredDB(metaclass=MetaClassMeasure):
    def import_data(self, directory_name, product_file, customer_file, rentals_file):
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

                        for data in product:
                            if data == '':
                                product_errors += 1
            except FileNotFoundError:
                LOGGER.error('Cannot find product_file')
                LOGGER.debug('Unable to locate product_file')
                product_errors += 1

            customer_collection = database["Customers"]
            try:
                with open(os.path.join(os.path.dirname(__file__),
                                       directory_name, customer_file)) as csvfile:
                    customer_file = csv.reader(csvfile)

                    for customer in customer_file:
                        customer_info = {'user_id': customer[0],
                                         'name': customer[1],
                                         'address': customer[2],
                                         'phone_number': customer[3],
                                         'email': customer[4]}
                        customer_collection.insert_one(customer_info)
                        customer_count += 1

                        for data in customer:
                            if data == '':
                                customer_errors += 1
            except FileNotFoundError:
                LOGGER.error('Cannot find customer_file')
                LOGGER.debug('Unable to locate customer_file')
                customer_errors += 1


            rental_collection = database["Rentals"]
            try:
                with open(os.path.join(os.path.dirname(__file__),
                                       directory_name, rentals_file)) as csvfile:
                    rentals_file = csv.reader(csvfile)

                    for rental in rentals_file:
                        rental_info = {'rid': rental[0],
                                       'product_id': rental[1],
                                       'user_id': rental[2]}
                        rental_collection.insert_one(rental_info)
                        rental_count += 1

                        for data in rental:
                            if data == '':
                                rental_errors += 1
            except FileNotFoundError:
                LOGGER.error('Cannot find rentals_file')
                LOGGER.debug('Unable to locate rentals_file')
                rental_errors += 1

        record_count = (product_count, customer_count, rental_count)
        errors_occurred = (product_errors, customer_errors, rental_errors)
        return record_count, errors_occurred

    def show_available_products(self):
        '''
            des:
                show product inventories with avaialable quanties
            in:
            out:
                dictionary of available product quantities
        '''

        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.hp_norton
            product_collection = database["Products"]
            py_dict = {}
            for product in product_collection.find():
                if product['quantity_available'] == '0':
                    continue
                elif product['quantity_available'] == '':
                    continue
                elif product['quantity_available'] == 'quantity_available':
                    continue
                else:
                    py_dict[product['product_id']] = dict([('description',
                                                            product['description']),
                                                           ('product_type',
                                                            product['product_type']),
                                                           ('quantity_available',
                                                            product['quantity_available'])])
            return py_dict

    def show_rentals(self, product_id):
        '''
            des:
                show customer products rented for given product id
            in:
                product id
            out:
                dictionary of customers who rented given product
        '''
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.hp_norton
            customer_collection = database["Customers"]
            rental_collection = database["Rentals"]
            py_dict = {}
            for renter in rental_collection.find():
                if product_id == renter['product_id']:
                    for customer in customer_collection.find():
                        if renter['user_id'] == customer['user_id']:
                            py_dict[customer['user_id']] = dict([('name',
                                                                  customer['name']),
                                                                 ('address',
                                                                  customer['address']),
                                                                 ('phone_number',
                                                                  customer['phone_number']),
                                                                 ('email',
                                                                  customer['email'])])
        return py_dict

    def dbs_cleanup(self):
        '''drop the db'''
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.hp_norton
            database["Customers"].drop()
            database["Products"].drop()
            database["Rentals"].drop()
        return 'databases dropped'

        
if __name__ == '__main__':

    print("pathspec commandline arg = " + str(sys.argv[1]))
    pathspec = str(sys.argv[1])

    measured_db = MeasuredDB()
    
