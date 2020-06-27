import csv
from pymongo import MongoClient
import logging
import os

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


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    populates a new MongoDB database with these data. It returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a count of any errors that occurred, in the same order.
    """
    mongo = MongoDBConnection()
    with mongo:
        LOGGER.info('Establish Mongo DB')
        database = mongo.connection.HP_Norton
        LOGGER.info('Creating collections')
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
        with open(product_path, encoding='utf-8-sig') as csv_file:
            product_reader = csv.reader(csv_file, delimiter=',')
            for product in product_reader:
                try:
                    product = {'product_id': product[0],
                               'description': product[1],
                               'product_type': product[2],
                               'quantity_available': product[3]}
                    products.insert_one(product)
                    product_count += 1
                    LOGGER.info('Product has been added to the product database')
                except FileNotFoundError:
                    LOGGER.info(f'File not found')
                    product_error_count += 1
                    
        # Reads customer data and inserts into database
        with open(customer_path, encoding='utf-8-sig') as csv_file:
            customer_reader = csv.reader(csv_file, delimiter=',')
            for customer in customer_reader:
                try:
                    customer = {'user_id': customer[0],
                                'name': customer[1],
                                'address': customer[2],
                                'phone_number': customer[3],
                                'email': customer[4]}
                    customers.insert_one(customer)
                    customer_count += 1
                    LOGGER.info('Customer has been added to the customer database')
                except FileNotFoundError:
                    LOGGER.info(f'File not found')
                    customer_error_count += 1
                    
        # Reads rentals data and inserts into database
        with open(rental_path, encoding='utf-8-sig') as csv_file:
            rental_reader = csv.reader(csv_file, delimiter=',')
            for rental in rental_reader:
                try:
                    rental = {'rental_id': rental[0],
                              'user_id': rental[1]}
                    rentals.insert_one(rental)
                    rental_count += 1
                    LOGGER.info('Rental has been added to the rental database')
                except FileNotFoundError:
                    LOGGER.info(f'File not found')
                    rentals_error_count += 1
        record_count = (product_count, customer_count, rental_count)
        error_count = (product_error_count, customer_error_count, rentals_error_count)
        return record_count, error_count


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
            available_products[product['product_id']] = {'description': product['description'],
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
    return print(rentals_dict)


def clear_db():
    mongo = MongoDBConnection()
    with mongo:
        LOGGER.info('Establish Mongo DB connection')
        database = mongo.connection.HP_Norton
        database.products.drop()
        database.customers.drop()
        database.rental.drop()
    LOGGER.info("Data has been removed from the database.")


