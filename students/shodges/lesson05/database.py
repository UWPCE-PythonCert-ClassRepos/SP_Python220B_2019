"""
Methods to allow processing of HP Norton inventory, including:

drop_data() to clear the inventory db
import_data(directory_name, product_file, customer_file, rentals_file) to intake existing CSV's
show_available_products() to show available products, accounting for existing rentals
show_rentals(product_id) to show all active rentals for product_id
"""
import csv
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

def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import data from specified CSV's into the database.
    """
    data_directory = Path(directory_name)
    with open(data_directory/product_file, mode='r') as product_input:
        product_list = [row for row in csv.DictReader(product_input)]
        logging.debug('Read in product data from %s: %s', product_file, product_list)

    with open(data_directory/customer_file, mode='r') as customer_input:
        customer_list = [row for row in csv.DictReader(customer_input)]
        logging.debug('Read in customer data from %s: %s', customer_file, customer_list)

    with open(data_directory/rentals_file, mode='r') as rentals_input:
        rentals_list = [row for row in csv.DictReader(rentals_input)]
        logging.debug('Read in rental data from %s: %s', rentals_file, rentals_list)

    mongo = DBConnection()

    with mongo:
        inv_db = mongo.connection.media

        products = inv_db['products']
        products_res = products.insert_many(product_list)
        if products_res.acknowledged is True:
            logging.debug('Wrote %d records to products', len(products_res.inserted_ids))
        else:
            logging.warning('Failed to write records to products')

        customers = inv_db['customers']
        customer_res = customers.insert_many(customer_list)
        if customer_res.acknowledged is True:
            logging.debug('Wrote %d records to customers', len(customer_res.inserted_ids))
        else:
            logging.warning('Failed to write records to customers')

        rentals = inv_db['rentals']
        rentals_res = rentals.insert_many(rentals_list)
        if rentals_res.acknowledged is True:
            logging.debug('Wrote %d records to rentals', len(rentals_res.inserted_ids))
        else:
            logging.warning('Failed to write records to rentals')

    return ((len(products_res.inserted_ids), len(customer_res.inserted_ids),
             len(rentals_res.inserted_ids)), (((0 if products_res.acknowledged is True else 1)
                                               + (0 if customer_res.acknowledged is True else 1) +
                                               (0 if rentals_res.acknowledged is True else 1)),))

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
