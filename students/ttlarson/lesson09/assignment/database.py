""""
This module returns for customer and rentals:
    (int) the number of records processed
    (int) the record count in the database prior to running
    (int) the record count after running
    (float) the time taken to run the module.

! mongo tip: use 127.0.0.1 on windows
"""

# pylint: disable=broad-except
# pylint: disable=too-many-locals
# pylint: disable=invalid-name

import logging
import functools
import os
import sys
from threading import Thread
from timeit import default_timer as timer
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# command line option to turn debugging info on/off
if len(sys.argv) > 1 and sys.argv[1].lower() in ('1', 'y', 'yes'):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

record_count_init = {
    "customers": 0,
    "products": 0,
    "rentals": 0
}
record_count = {
    "customers": 0,
    "products": 0,
    "rentals": 0
}
err_count = {
    "customers": 0,
    "products": 0,
    "rentals": 0
}
time_exec = {
    "customers": 0,
    "products": 0,
    "rentals": 0
}

class MongoDBConnection():
    """ MongoDB Connection """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows """
        self.host = host
        self.port = port
        self.connection = None
        logging.info('Starting Mongo connection ...')

    def __enter__(self):
        """ On entering: creating the connection to Mongo  """
        try:
            self.connection = MongoClient(self.host, self.port)
        except ConnectionFailure as e:
            logging.error('Failed to connect to MongoDB: %s', e)
            raise e
        logging.info('Mongo connected.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ On exiting: closing the connection to Mongo  """
        if exc_type:
            logging.error('Error: %s', exc_val)
        self.connection.close()
        logging.info('Mongo connection closed.')

def log_logging():
    """ decorator for logging """
    def error_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = ('And error has occurred at /%s\n', func.__name__)
                logging.exception(error_msg)
                return e
        return wrapper
    return error_log

def print_mdb_collection(collection_name):
    """ print everything in collection_name """
    for doc in collection_name.find():
        print(doc)

def import_data_csv(directory_name, data_file):
    """ import data from csv files """
    file_path = os.path.join(directory_name, data_file)
    logging.debug('Opening file: %s', file_path)

    data = pd.DataFrame()

    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        logging.error('Cannot find file: %s', file_path)

    logging.debug('Done with file: %s', file_path)

    return data

@log_logging()
def db_collection_init(mdb, collection_name):
    """ decorator to initialize mongo collection """
    # create collections if not exist
    logging.debug('Creating the %s collections ...', collection_name)
    collection = mdb[collection_name]

    # clear out the collections and start fresh
    logging.debug('Clearing collection data for %s ...', collection_name)
    collection.drop()

    return collection

@log_logging()
def db_insert(mdb_collection, dict_name, name):
    """ using decorator for mongo insert logging """
    try:
        result = mdb_collection.insert_many(dict_name)
        record_count[name] = len(result.inserted_ids)
        logging.info('%s records inserted into Mongodb collection %s.', record_count[name], name)
    except Exception as err:
        err_count[name] += 1
        logging.debug('Error count incremented by 1 for %s.', name)
        logging.error('%s', err)

def import_data_customers(mongo, directory_name, customer_file):
    """ import customer data """
    dt_start = timer()

    customers = db_collection_init(mongo, 'customers')

    logging.debug('Start loading customer data from CSV file ...')
    dict_customer = import_data_csv(directory_name, customer_file).to_dict('records')

    db_insert(customers, dict_customer, 'customers')

    dt_end = timer()
    time_exec['customers'] = dt_end - dt_start

def import_data_products(mongo, directory_name, product_file):
    """ import product data """
    dt_start = timer()

    products = db_collection_init(mongo, 'products')

    logging.debug('Start loading product data from CSV file ...')
    dict_product = import_data_csv(directory_name, product_file).to_dict('records')

    db_insert(products, dict_product, 'products')

    dt_end = timer()
    time_exec['products'] = dt_end - dt_start

def import_data_rentals(mongo, directory_name, rental_file):
    ''' import rental data '''

    rentals = db_collection_init(mongo, 'rentals')

    logging.debug('Start loading rental data from CSV file ...')
    dict_rental = import_data_csv(directory_name, rental_file).to_dict('records')

    db_insert(rentals, dict_rental, 'rentals')

def import_data(directory_name, product_file, customer_file, rental_file):
    """ import data from CSV files, then insert into MongoDB """

    mdb = MongoDBConnection()
    with mdb:
        mongo = mdb.connection.HPNorton

        c_thread = Thread(target=import_data_customers,
                          args=(mongo, directory_name, customer_file))
        p_thread = Thread(target=import_data_products,
                          args=(mongo, directory_name, product_file))
        r_thread = Thread(target=import_data_rentals,
                          args=(mongo, directory_name, rental_file))

        c_thread.start()
        p_thread.start()
        r_thread.start()

        c_thread.join()
        p_thread.join()
        r_thread.join()

    tup_customer = (record_count['customers']-record_count_init['customers'],
                    record_count_init['customers'],
                    record_count['customers'],
                    time_exec['customers'])
    tup_product = (record_count['products']-record_count_init['products'],
                   record_count_init['products'],
                   record_count['products'],
                   time_exec['products'])

    return [tup_customer, tup_product]

def show_available_products():
    """ function to show all the products avalable """
    available = dict()

    mdb = MongoDBConnection()
    with mdb:
        mongo = mdb.connection.HPNorton

        for product in mongo.products.find():
            if product['quantity_available'] > 0:
                key = product['product_id']
                product = {'description': product['description'],
                           'product_type': product['product_type'],
                           'quantity_available': product['quantity_available']}

                available[key] = product

    return available

def show_rentals(product_id):
    """ function to show the list of user information by using product_id  """
    user_info = dict()

    mdb = MongoDBConnection()
    with mdb:
        mongo = mdb.connection.HPNorton

        for rental in mongo.rentals.find({"product_id": product_id}):
            user_id = rental['user_id']
            for customer in mongo.customers.find():
                if user_id == customer['user_id']:
                    user = {'name': customer['name'],
                            'address': customer['address'],
                            'phone_number': customer['phone_number'],
                            'email': customer['email']}

                    user_info[user_id] = user

        return user_info

if __name__ == '__main__':
    DATA_FILE_CUSTOMER = 'customers.csv'
    DATA_FILE_PRODUCT = 'products.csv'
    DATA_FILE_RENTAL = 'rentals.csv'
    DATA_FILE_PATH = os.getcwd()
    logging.debug('Current directory: %s', DATA_FILE_PATH)

    import_status = import_data(DATA_FILE_PATH,
                                DATA_FILE_PRODUCT,
                                DATA_FILE_CUSTOMER,
                                DATA_FILE_RENTAL)
    logging.info(import_status)

    products_available = show_available_products()
    logging.info(products_available)

    users_E0001 = show_rentals('E0001')
    logging.info(users_E0001)
