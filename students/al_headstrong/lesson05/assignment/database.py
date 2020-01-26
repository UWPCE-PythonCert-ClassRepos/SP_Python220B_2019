from pymongo import MongoClient
import pandas as pd
import logging
import os

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'

FORMATTER = logging.Formatter(LOG_FORMAT)

LOG_FILE = 'db.log'

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.WARNING)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


class MongoDBConnection(object):
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


def import_csv(directory, file):
    """Read csv file in directory into data frame, then return list of dicts and dict count."""
    df = pd.read_csv(os.path.join(os.path.abspath(directory), file))
    return df.to_dict('records'), df.shape[0]


def import_data(directory_name, product_file, customer_file, rentals_file):
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        files = (product_file, customer_file, rentals_file)
        databases = (db['products'], db['customers'], db['rentals'])
        input_count = []
        error_count = []

        for file_name, database in zip(files, databases):

            try:
                data, count = import_csv(directory_name, file_name)
                database.insert_many(data)

            except FileNotFoundError as error:
                LOGGER.error('Error %s loading %s.', error, file)
                error_count += 1
                count = 0

            input_count.append(count)

        return tuple(input_count), tuple(error_count)


def show_available_products():
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        products = db['products']
        available_products = {}
        for product in products.find():
            if product["quantity_available"] > 0:
                available_products[product['product_id']] = {
                    'description': product['description'],
                    'product_type': product['product_type'],
                    'quantity_available': product['quantity_available']
                }
        return available_products


def show_rentals(product_id):
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        rentals = db['rentals']
        customers = db['customers']
        renters = {}
        for rental in rentals.find({'product_id': product_id}):
            for customer in customers.find({'customer_id': rental['customer_id']}):
                renters[customer['customer_id']] = {
                    'name': customer['name'],
                    'address': customer['address'],
                    'phone_number': customer['phone_number'],
                    'email': customer['email']
                }
        return renters


