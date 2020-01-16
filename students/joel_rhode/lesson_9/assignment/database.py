"""
MongoDB database code for HP Norton customer, rental, and inventory system.
"""
# pylint: disable=too-many-locals

from csv import reader
import os
import logging

from pymongo import MongoClient

DATABASE = 'hp_norton'

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
LOG_FILE = 'database.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE, delay=True)
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)

LOGGER.setLevel(logging.INFO)

class MongoDBConnection():
    """MongoDB Connection"""
    def __init__(self, host='localhost', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        logging.info('MongoDB connection established at host: %s, port: %d',
                     self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        logging.debug('Exit type: %s, exit value: %s, exit traceback: %s',
                      exc_type, exc_val, exc_tb)


def import_data(directory_name, product_file, customers_file, rentals_file):
    """Imports product, customer, and rental .csv files into the database."""
    product_fields = ('product_id', 'description', 'product_type', 'quantity_available')
    customer_fields = ('customer_id', 'name', 'address', 'phone_number', 'email')
    rental_fields = ('rental_id', 'product_id', 'customer_id', 'rental_start', 'rental_end')
    product_list, product_errors = read_csv(directory_name, product_file, product_fields)
    for item in product_list:
        item['quantity_available'] = int(item['quantity_available'])
    product_count = write_many_to_database(DATABASE, 'products', product_list)
    customer_list, customer_errors = read_csv(directory_name, customers_file, customer_fields)
    customer_count = write_many_to_database(DATABASE, 'customers', customer_list)
    rentals_list, rental_errors = read_csv(directory_name, rentals_file, rental_fields)
    rental_count = write_many_to_database(DATABASE, 'rentals', rentals_list)
    return (product_count, customer_count, rental_count), \
           (product_errors, customer_errors, rental_errors)


def read_csv(directory_name, file_name, fields):
    """Reads csv file and puts results into list of dictionaries with keys per fields parameter."""
    csv_list = []
    error_count = 0
    with open(os.path.join(directory_name, file_name), newline='') as csv_file:
        for row in reader(csv_file):
            try:
                assert len(fields) == len(row)
                csv_list.append(dict(zip(fields, row)))
            except AssertionError:
                logging.warning('Mismatch in line data length. Expected %d items but data has'
                                '%d items. Line: %s', len(fields), len(row), row)
                error_count += 1
    return csv_list, error_count


def write_many_to_database(database_name, collection, data_list):
    """Inserts data_dict to collection in MongoDB database."""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection[database_name]
        collection = database[collection]
        result = collection.insert_many(data_list)
    if result.acknowledged:
        return len(result.inserted_ids)
    return False


def show_available_products(database_name=DATABASE, collection='products'):
    """Returns a dictionary with all products listed as available in the database."""
    mongo = MongoDBConnection()
    products_avail = {}
    with mongo:
        database = mongo.connection[database_name]
        product_query = database[collection].find({'quantity_available': {'$gt': 0}})
        for product in product_query:
            products_avail[product['product_id']] = product
            del products_avail[product['product_id']]['_id']
    return products_avail


def show_rentals(product_id, database_name=DATABASE):
    """Returns a dictionary of user data for all users that have rented specified product id."""
    mongo = MongoDBConnection()
    rental_customers = {}
    with mongo:
        database = mongo.connection[database_name]
        for rental in database['rentals'].find({'product_id': product_id}):
            try:
                customer = database['customers'].find_one({'customer_id': rental['customer_id']})
                rental_customers[customer['customer_id']] = customer
                del rental_customers[customer['customer_id']]['_id']
            except KeyError:
                logging.error('Key not found in database.')
                raise
    return rental_customers
