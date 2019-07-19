'''
    Assignment 7, parallel.py
'''
import csv
import os
import logging
import time
import threading
import queue
# import timeit
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


def import_product_file():
    '''
        Imports the product csv file and enters the data into the database.
        Returns products_imported (int),
                product_count_prior (int),
                product_count (int),
                products_time (float)
    '''
    products_init = time.perf_counter()
    product_count = 0
    products_imported = 0
    product_errors = 0
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        product_collection = database["Products"]
        product_count_prior = product_collection.estimated_document_count()
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   'csv_files', 'product_file.csv')) as csvfile:
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
            product_errors += 1
    products_time = time.perf_counter() - products_init
    # print((products_imported, product_count_prior, product_count, products_time))
    return products_imported, product_count_prior, product_count, products_time


def import_customer_file():
    '''
        Imports the customer csv file and enters the data into the database.
        Returns customers_imported (int),
                customer_count_prior (int),
                customer_count (int),
                customers_time (float)
    '''
    customers_init = time.perf_counter()
    customer_count = 0
    customers_imported = 0
    customer_errors = 0
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        customer_collection = database["Customers"]
        customer_count_prior = customer_collection.estimated_document_count()
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   'csv_files', 'customer_file.csv')) as csvfile:
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
            customer_errors += 1
    customers_time = time.perf_counter() - customers_init
    # print(('customers', customers_imported, customer_count_prior, customer_count, customers_time))
    return customers_imported, customer_count_prior, customer_count, customers_time


def import_rentals_file():
    '''
        Imports the rentals csv file and enters the data into the database.
        Returns rental_count (int),
                rental_errors (int)
    '''
    rental_count = 0
    rental_errors = 0
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        rental_collection = database["Rentals"]
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   'csv_files', 'rentals_file.csv')) as csvfile:
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
            rental_errors += 1
    return rental_count, rental_errors


def drop_dbs():
    '''deletes all entries made to the database'''
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        database["Customers"].drop()
        database["Products"].drop()
        database["Rentals"].drop()
        # print('Databases have been dropped')
    return 'Databases have been dropped'


def main():
    '''
        Runs the import functions as threads and drops the databases after the threads
        have completed running.

        Returns a list of two tuples, the customer file tuple and the product file tuple
    '''
    que = queue.Queue()

    thread1 = threading.Thread(target=import_rentals_file)
    thread1.start()
    thread2 = threading.Thread(target=lambda q: q.put(import_customer_file()), args=(que,))
    thread2.start()
    thread3 = threading.Thread(target=lambda q: q.put(import_product_file()), args=(que,))
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    thread_one_return = que.get()
    thread_two_return = que.get()

    drop_dbs()

    return [thread_one_return, thread_two_return]


if __name__ == '__main__':
    # timer = timeit.timeit('main()', globals=globals(), number=1)
    # print(timer)
    RETURNS = main()
    print(RETURNS)
