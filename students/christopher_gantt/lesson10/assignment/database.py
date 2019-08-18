'''
    Assignment 10, MetaProgramming

    pylint Diasble = too-many-instance-attributes, no-member
'''
import csv
import os
import logging
from timeit import timeit
from datetime import datetime
from pymongo import MongoClient

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

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


class ImportData():
    '''restructuring import data function into a class'''
    def __init__(self, directory_name, product_file, customer_file, rentals_file):
        self.directory_name = directory_name
        self.product_file = product_file
        self.customer_file = customer_file
        self.rentals_file = rentals_file
        self.product_count = 0
        self.product_errors = 0
        self.customer_count = 0
        self.customer_errors = 0
        self.rental_count = 0
        self.rental_errors = 0

    def import_product_file(self):
        '''imports the product file csv and moves it into a mongodb database'''
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.hp_norton
            product_collection = database["Products"]
            try:
                with open(os.path.join(os.path.dirname(__file__),
                                       self.directory_name, self.product_file)) as csvfile:
                    product_file = csv.reader(csvfile)

                    for product in product_file:
                        product_info = {'product_id': product[0],
                                        'description': product[1],
                                        'product_type': product[2],
                                        'quantity_available': product[3]}
                        product_collection.insert_one(product_info)
                        self.product_count += 1

                        for data in product: #check for data omissions/'errors'
                            if data == '':
                                self.product_errors += 1
            except FileNotFoundError:
                LOGGER.error('Cannot find product_file')
                LOGGER.debug('Make sure directory and file name are entered correctly')
                self.product_errors += 1
        return (self.product_count, self.product_errors)

    def import_customer_file(self):
        '''imports the customer file csv and moves it into a mongodb database'''
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.hp_norton
            customer_collection = database["Customers"]
            try:
                with open(os.path.join(os.path.dirname(__file__),
                                       self.directory_name, self.customer_file)) as csvfile:
                    customer_file = csv.reader(csvfile)

                    for customer in customer_file:
                        customer_info = {'user_id': customer[0],
                                         'name': customer[1],
                                         'address': customer[2],
                                         'phone_number': customer[3],
                                         'email': customer[4]}
                        customer_collection.insert_one(customer_info)
                        self.customer_count += 1

                        for data in customer: #check for data omissions/'errors'
                            if data == '':
                                self.customer_errors += 1
            except FileNotFoundError:
                LOGGER.error('Cannot find customer_file')
                LOGGER.debug('Make sure directory and file name are entered correctly')
                self.customer_errors += 1
        return (self.customer_count, self.customer_errors)

    def import_rentals_file(self):
        '''imports the rentals file csv and moves it into a mongodb database'''
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.hp_norton
            rental_collection = database["Rentals"]
            try:
                with open(os.path.join(os.path.dirname(__file__),
                                       self.directory_name, self.rentals_file)) as csvfile:
                    rentals_file = csv.reader(csvfile)

                    for rental in rentals_file:
                        rental_info = {'user_id': rental[0],
                                       'name': rental[1],
                                       'rentals': rental[2]}
                        rental_collection.insert_one(rental_info)
                        self.rental_count += 1

                        for data in rental: #check for data omissions/'errors'
                            if data == '':
                                self.rental_errors += 1
            except FileNotFoundError:
                LOGGER.error('Cannot find rentals_file')
                LOGGER.debug('Make sure directory and file name are entered correctly')
                self.rental_errors += 1
        return (self.rental_count, self.rental_errors)


def time_class_methods(self):
    '''
        Method to be passed into the ImportData class.
        Times all class methods and then writes the relavent data
        to timings.txt

        Function Name, Time Taken, Number of Records Processed
    '''
    data = []

    time_products = timeit(self.import_product_file, number=10)
    time_customers = timeit(self.import_customer_file, number=10)
    time_rentals = timeit(self.import_rentals_file, number=10)

    data.append(f'\nFunction Name: import_product_file\nTime Taken: {time_products}\n'+
                f'Records Processed: {self.product_count}\n')
    data.append(f'\nFunction Name: import_customer_file\nTime Taken: {time_customers}\n'+
                f'Records Processed: {self.customer_count}\n')
    data.append(f'\nFunction Name: import_rentals_file\nTime Taken: {time_rentals}\n'+
                f'Records Processed: {self.rental_count}\n\n')

    with open('timings.txt', 'a') as file:
        file.write(f'\nTime class methods {datetime.now()}\n')
        for entry in data:
            file.write(entry)

    return data


def drop_dbs():
    '''deletes all entries made to the database'''
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        database["Customers"].drop()
        database["Products"].drop()
        database["Rentals"].drop()
    return 'Databases have been dropped'


if __name__ == '__main__':
    setattr(ImportData, 'time_class_methods', time_class_methods)
    ID = ImportData('csv_files', 'product_file.csv', 'customer_file.csv', 'rentals_file.csv')
    ID.time_class_methods()
    drop_dbs()
