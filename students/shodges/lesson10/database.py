"""
Methods to allow processing of HP Norton inventory, including:

drop_data() to clear the inventory db
import_data(directory_name, product_file, customer_file, rentals_file) to intake existing CSV's
show_available_products() to show available products, accounting for existing rentals
show_rentals(product_id) to show all active rentals for product_id
"""
import csv
import datetime
import logging
from pathlib import Path
from pymongo import MongoClient

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'

FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(FILE_HANDLER)

class DBConnection():
    """
    Class to instantiate the connection to the Mongo DB.
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """
        Initialize the connection class.
        """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """
        Connect to the DB when entering the context manager.
        """
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the connection when exiting the context manager.
        """
        self.connection.close()

def timed_func(func):
    """
    Decorator to time a function call.
    """
    def run_and_time(*args, **kwargs):
        """
        Wrapper function to run the function func and log performance data.
        """
        start_time = datetime.datetime.now()
        ret_val = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print('Function {} ran in {} seconds'.format(func.__name__,
              (end_time - start_time).total_seconds()))
        return ret_val
    return run_and_time

@timed_func
def drop_data():
    """
    Drop the existing data from the database to allow a fresh start.
    """
    mongo = DBConnection()

    with mongo:
        inv_db = mongo.connection.media

        inv_db['products'].drop()
        inv_db['customers'].drop()
        inv_db['rentals'].drop()

        logging.debug('Dropped all databases')

@timed_func
def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import data from specified CSV's into the database.
    """
    data_directory = Path(directory_name)
    with open(data_directory/product_file, mode='r') as csv_input:
        product_list = list(csv.DictReader(csv_input))
        logging.debug('Read in product data from %s: %s', product_file, product_list)

    with open(data_directory/customer_file, mode='r') as csv_input:
        customer_list = list(csv.DictReader(csv_input))
        logging.debug('Read in customer data from %s: %s', customer_file, customer_list)

    with open(data_directory/rentals_file, mode='r') as csv_input:
        rentals_list = list(csv.DictReader(csv_input))
        logging.debug('Read in rental data from %s: %s', rentals_file, rentals_list)

    mongo = DBConnection()

    with mongo:
        inv_db = mongo.connection.media

        products_res = inv_db['products'].insert_many(product_list)
        if products_res.acknowledged is True:
            logging.debug('Wrote %d records to products', len(products_res.inserted_ids))
        else:
            logging.warning('Failed to write records to products')

        customer_res = inv_db['customers'].insert_many(customer_list)
        if customer_res.acknowledged is True:
            logging.debug('Wrote %d records to customers', len(customer_res.inserted_ids))
        else:
            logging.warning('Failed to write records to customers')

        rentals_res = inv_db['rentals'].insert_many(rentals_list)
        if rentals_res.acknowledged is True:
            logging.debug('Wrote %d records to rentals', len(rentals_res.inserted_ids))
        else:
            logging.warning('Failed to write records to rentals')

    return ((len(products_res.inserted_ids), len(customer_res.inserted_ids),
             len(rentals_res.inserted_ids)), (((0 if products_res.acknowledged is True else 1)
                                               + (0 if customer_res.acknowledged is True else 1) +
                                               (0 if rentals_res.acknowledged is True else 1)),))

@timed_func
def show_available_products():
    """
    Return a dictionary of all available products of the following format:
    {'product_id': {'description': 'description',
                    'product_type': 'product_type',
                    'quantity_available': 'quantity_available*'
                   }
    }
    * NOTE: quantity_available will be the value of the total product quantity less current rentals
    """
    mongo = DBConnection()

    product_list = {}

    with mongo:
        inv_db = mongo.connection.media

        products = inv_db['products']
        rentals = inv_db['rentals']

        for item in products.find():
            logging.debug('Found product %s', item['product_id'])
            query = {'product_id': item['product_id']}
            rented_quantity = rentals.count_documents(query)
            quantity_available = int(item['quantity_available']) - rented_quantity
            for rental in rentals.find(query):
                logging.debug('Rented to %s', rental['user_id'])
            logging.debug('Total rentals: %d', rented_quantity)
            product_list[item['product_id']] = {'description': item['description'],
                                                'product_type': item['product_type'],
                                                'quantity_available': quantity_available}

    return product_list

@timed_func
def show_rentals(product_id):
    """
    Return a dictionary of all renters of product_id in the following format:
    {'user_id': {'name': 'name',
                 'address': 'address',
                 'phone_number': 'phone_number'
                 'email': 'email'
                }
    }
    """
    mongo = DBConnection()

    renter_list = {}

    with mongo:
        inv_db = mongo.connection.media

        rentals = inv_db['rentals']
        customers = inv_db['customers']

        logging.debug('Finding renters for %s', product_id)
        query_1 = {'product_id': product_id}
        for rental in rentals.find(query_1):
            logging.debug('Found renter %s', rental['user_id'])
            query_2 = {'user_id': rental['user_id']}
            for renter in customers.find(query_2):
                renter_list[renter['user_id']] = {'name': renter['name'],
                                                  'address': renter['address'],
                                                  'phone_number': renter['phone_number'],
                                                  'email': renter['email']}
                logging.debug('Renter info: %s', renter_list[renter['user_id']])

        return renter_list
