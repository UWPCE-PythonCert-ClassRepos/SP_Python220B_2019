# pylint: disable = W0614, W0401, C0301, C0305, R0914
"""Database.py"""
import os
import logging
import csv
from pymongo import MongoClient
from functools import wraps
import time

logging.basicConfig(level=logging.INFO,
                    filename='timings.txt',
                    format='%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s')


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


def timing(func):
    """Count time elapsed to run a function"""
    @wraps(func)
    def timed(*args, **kw):
        start = time.time()
        output = func(*args, **kw)
        end = time.time()
        time_elapsed = end - start
        try:
            records = output[0]
        except KeyError:
            records = len(output.keys())
        logging.info(f'ran {func.__name__} and processed {records} records in'
                     f' {str(time_elapsed)}')
        return output
    return timed

@timing
def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    populates a new MongoDB database with these data. It returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a count of any errors that occurred, in the same order.
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.HP_Norton
        # Create collections
        products = database['products']
        customers = database['customers']
        rentals = database['rentals']
        # Define file paths
        product_path = os.path.join(directory_name, product_file)
        customer_path = os.path.join(directory_name, customer_file)
        rental_path = os.path.join(directory_name, rentals_file)
        # Initiate 0 counts to start
        product_count, customer_count, rental_count = 0, 0, 0
        product_error_count, customer_error_count, rentals_error_count = 0, 0, 0
        # Reads products data and inserts into database
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
                except FileNotFoundError:
                    product_error_count += 1
        # Reads customer data and inserts into database
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
                except FileNotFoundError:
                    customer_error_count += 1
        # Reads rentals data and inserts into database
        with open(rental_path, 'r', encoding='utf-8-sig') as csv_file:
            rental_reader = csv.DictReader(csv_file)
            for rental in rental_reader:
                try:
                    rental = {'product_id': rental['product_id'],
                              'user_id': rental['user_id']}
                    rentals.insert_one(rental)
                    rental_count += 1
                except FileNotFoundError:
                    rentals_error_count += 1
        record_count = (product_count, customer_count, rental_count)
        error_count = (product_error_count, customer_error_count, rentals_error_count)
        return record_count, error_count

@timing
def show_available_products():
    """Returns a Python dictionary of products listed as available """
    mongo = MongoDBConnection()
    available_products = {}
    with mongo:
        database = mongo.connection.HP_Norton
        products = database['products']
        for product in products.find({'quantity_available': {'$gt': '0'}}):
            available_products[product['product_id']] = \
                {'description': product['description'],
                 'product_type': product['product_type'],
                 'quantity_available': product['quantity_available']}
    return available_products

@timing
def show_rentals(product_id):
    """Returns a Python dictionary user information from users
    that have rented products matching product_id"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.HP_Norton
        rentals = database['rentals']
        customers = database['customers']
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
        database = mongo.connection.HP_Norton
        database.products.drop()
        database.customers.drop()
        database.rental.drop()


if __name__ == '__main__':
    clear_db()
    import_data('/Users/Tian/Documents/PythonClass/Tianx/SP_Python220B_2019'
                           '/students/Tianx/Lesson10/data/',
                               'product.csv',
                               'customers.csv',
                               'rental.csv')
    show_available_products()
    show_rentals("prd001")
    clear_db()
    import_data('/Users/Tian/Documents/PythonClass/Tianx/SP_Python220B_2019'
                           '/students/Tianx/Lesson10/large_data/',
                               'product.csv',
                               'customers.csv',
                               'rental.csv')
    show_available_products()
    show_rentals("prd557")

