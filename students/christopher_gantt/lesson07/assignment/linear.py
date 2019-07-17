'''
    Assignment 7, linear.py

    pylint Disable=too-many-locals, too-many-statements
'''
import csv
import os
import logging
import time
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


def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
        This function takes a directory name three csv files as input, one with
        product data, one with customer data and the third one with rentals data
        and creates and populates a new MongoDB database with these data.

        It returns 2 tuples: the first with a record count of the number of
        products, customers and rentals added (in that order), the second with a
        timing of the Products import time and the customers import time (in that order).
    '''
    product_count = 0
    customer_count = 0
    rental_count = 0

    products_imported = 0
    customers_imported = 0

    product_errors = 0
    customer_errors = 0
    rental_errors = 0

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton

        products_init = time.perf_counter()
        product_collection = database["Products"]
        product_count_prior = product_collection.estimated_document_count()
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   directory_name, product_file)) as csvfile:
                product_file = csv.reader(csvfile)

                for product in product_file:
                    products_imported += 1
                    product_info = {'product_id': product[0],
                                    'description': product[1],
                                    'product_type': product[2],
                                    'quantity_available': product[3]}
                    product_collection.insert_one(product_info)
                    product_count += 1

                    for data in product: #check for data omissions/'errors'
                        if data == '':
                            product_errors += 1
        except FileNotFoundError:
            LOGGER.error('Cannot find product_file')
            LOGGER.debug('Make sure directory and file name are entered correctly')
            product_errors += 1
        products_time = time.perf_counter() - products_init

        customers_init = time.perf_counter()
        customer_collection = database["Customers"]
        customer_count_prior = customer_collection.estimated_document_count()
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   directory_name, customer_file)) as csvfile:
                customer_file = csv.reader(csvfile)

                for customer in customer_file:
                    customers_imported += 1
                    customer_info = {'user_id': customer[0],
                                     'name': customer[1],
                                     'address': customer[2],
                                     'phone_number': customer[3],
                                     'email': customer[4]}
                    customer_collection.insert_one(customer_info)
                    customer_count += 1

                    for data in customer: #check for data omissions/'errors'
                        if data == '':
                            customer_errors += 1
        except FileNotFoundError:
            LOGGER.error('Cannot find customer_file')
            LOGGER.debug('Make sure directory and file name are entered correctly')
            customer_errors += 1
        customers_time = time.perf_counter() - customers_init


        rental_collection = database["Rentals"]
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   directory_name, rentals_file)) as csvfile:
                rentals_file = csv.reader(csvfile)

                for rental in rentals_file:
                    rental_info = {'user_id': rental[0],
                                   'name': rental[1],
                                   'rentals': rental[2]}
                    rental_collection.insert_one(rental_info)
                    rental_count += 1

                    for data in rental: #check for data omissions/'errors'
                        if data == '':
                            rental_errors += 1
        except FileNotFoundError:
            LOGGER.error('Cannot find rentals_file')
            LOGGER.debug('Make sure directory and file name are entered correctly')
            rental_errors += 1

    import_count = (products_imported, customers_imported)
    record_count_prior = (product_count_prior, customer_count_prior)
    record_count = (product_count, customer_count, rental_count)
    timer = (products_time, customers_time)
    errors_occurred = (product_errors, customer_errors, rental_errors)
    return (import_count, record_count_prior, record_count, timer, errors_occurred)


def drop_dbs():
    '''deletes all entries made to the database'''
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        database["Customers"].drop()
        database["Products"].drop()
        database["Rentals"].drop()
    return 'Databases have been dropped'


def main():
    '''
        Return a list of tuples, one tuple for customer and one for products.
        Each tuple will contain 4 values: the number of records processed, imported (int),
                                          the record count in the database prior to running (int),
                                          the record count in the database after running (int),
                                          and the time taken to run the module (float)
    '''
    imported = import_data('csv_files',
                           'product_file.csv',
                           'customer_file.csv',
                           'rentals_file.csv')
    drop_dbs()
    return[(imported[0][1], imported[1][1], imported[2][1], imported[3][1]),
           (imported[0][0], imported[1][0], imported[2][0], imported[3][0])]


if __name__ == '__main__':
    RETURNS = main()
    print(RETURNS)
