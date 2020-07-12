# pylint: disable = W0614, W0401, C0301, C0305, R0914
"""Database.py"""
import os
import logging
import csv
from pymongo import MongoClient
import cProfile
import threading
import queue
import time

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class MongoDBConnection():
    """Establish MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_products(directory_name, product_file):
    """populates a new MongoDB database with products data. """
    start_time = time.time()
    product_count = 0
    product_error_count = 0
    product_path = os.path.join(directory_name, product_file)

    mongo = MongoDBConnection()
    with mongo:
        LOGGER.info('Establish Mongo DB')
        database = mongo.connection.HP_Norton
        LOGGER.info('Creating collections')
        products = database['products']
        prior_number = database.products.count_documents({})

        with open(product_path, 'r', encoding='utf-8-sig') as csv_file:
            product_reader = csv.DictReader(csv_file)
            for product in product_reader:
                try:
                    product = {'product_id': product['product_id'],
                               'description': product['description'],
                               'product_type': product['product_type'],
                               'quantity_available': product['quantity_available']}
                    products.insert_one(product)
                    product_count += 1
                    LOGGER.info(f"{product['product_id']} has been added to the product database")
                except FileNotFoundError:
                    LOGGER.info('File not found')
                    product_error_count += 1
            after_number = database.products.count_documents({})
    end_time = time.time()
    time_spent = end_time - start_time
    queue.put((product_count, prior_number, after_number, time_spent), product_error_count)


def import_customers(directory_name, customer_file):
    """populates a new MongoDB database with customers data. """
    start_time = time.time()
    customer_count = 0
    customer_error_count = 0
    customer_path = os.path.join(directory_name, customer_file)

    mongo = MongoDBConnection()
    with mongo:
        LOGGER.info('Establish Mongo DB')
        database = mongo.connection.HP_Norton
        LOGGER.info('Creating collections')
        customers = database['customers']
        prior_number = database.customers.count_documents({})

        with open(customer_path, 'r', encoding='utf-8-sig') as csv_file:
            customer_reader = csv.DictReader(csv_file)
            for customer in customer_reader:
                try:
                    customer = {'user_id': customer['user_id'],
                                'name': customer['name'],
                                'address': customer['address'],
                                'phone_number': customer['phone_number'],
                                'email': customer['email']}
                    customers.insert_one(customer)
                    customer_count += 1
                    LOGGER.info(
                        f"{customer['user_id']} has been added to the customer database")
                except FileNotFoundError:
                    LOGGER.info('File not found')
                    customer_error_count += 1
            after_number = database.products.count_documents({})
    end_time = time.time()
    time_spent = end_time - start_time
    queue.put((customer_count, prior_number, after_number, time_spent), customer_error_count)


def import_rentals(directory_name, rentals_file):
    """populates a new MongoDB database with rentals data. """
    start_time = time.time()
    rental_count = 0
    rentals_error_count = 0
    rental_path = os.path.join(directory_name, rentals_file)

    mongo = MongoDBConnection()
    with mongo:
        LOGGER.info('Establish Mongo DB')
        database = mongo.connection.HP_Norton
        LOGGER.info('Creating collections')
        rentals = database['rentals']
        prior_number = database.rentals.count_documents({})

        with open(rental_path, 'r', encoding='utf-8-sig') as csv_file:
            rental_reader = csv.DictReader(csv_file)
            for rental in rental_reader:
                try:
                    rental = {'product_id': rental['product_id'],
                              'user_id': rental['user_id']}
                    rentals.insert_one(rental)
                    rental_count += 1
                    LOGGER.info(
                        f"{rental['product_id']} has been added to the rental database")
                except FileNotFoundError:
                    LOGGER.info('File not found')
                    rentals_error_count += 1
            after_number = database.products.count_documents({})
    end_time = time.time()
    time_spent = end_time - start_time
    queue.put((rental_count, prior_number, after_number, time_spent), rentals_error_count)


def show_available_products():
    """Returns a Python dictionary of products listed as available """
    mongo = MongoDBConnection()
    available_products = {}
    with mongo:
        LOGGER.info('Establish Mongo DB connection')
        database = mongo.connection.HP_Norton
        products = database['products']
        LOGGER.info('Searching or for available products')
        for product in products.find({'quantity_available': {'$gt': '0'}}):
            available_products[product['product_id']] = \
                {'description': product['description'],
                 'product_type': product['product_type'],
                 'quantity_available': product['quantity_available']}
    return available_products


def show_rentals(product_id):
    """Returns a Python dictionary user information from users
    that have rented products matching product_id"""
    mongo = MongoDBConnection()
    with mongo:
        LOGGER.info('Establish Mongo DB connection')
        database = mongo.connection.HP_Norton
        rentals = database['rentals']
        customers = database['customers']
        LOGGER.info('Searching or for rentals')
        rentals_dict = {}
        for renter in rentals.find({'product_id': product_id}):
            customer = customers.find_one({'user_id': renter['user_id']})
            rentals_dict[renter['user_id']] = {
                'name': customer['name'],
                'address': customer['address'],
                'phone_number': customer['phone_number'],
                'email': customer['email']}
    return rentals_dict


def clear_db():
    """Clears the database"""
    mongo = MongoDBConnection()
    with mongo:
        LOGGER.info('Establish Mongo DB connection')
        database = mongo.connection.HP_Norton
        database.products.drop()
        database.customers.drop()
        database.rental.drop()
    LOGGER.info("Data has been removed from the database.")


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    path = f'/Users/Tian/Documents/PythonClass/Tianx/SP_Python220B_2019/students/Tianx/Lesson7/'
    queue = queue.Queue()
    threads = []
    queues = []
    threads.append(threading.Thread(target=import_products,
                                    args=(path, 'product.csv'), daemon=True))
    threads.append(threading.Thread(target=import_customers,
                                    args=(path, 'customers.csv'), daemon=True))
    threads.append(threading.Thread(target=import_rentals, args=(path, 'rental.csv'), daemon=True))
    for thread in threads:
        thread.start()
        queues.append(queue.get())
        thread.join()
    pr.disable()
    pr.print_stats()

