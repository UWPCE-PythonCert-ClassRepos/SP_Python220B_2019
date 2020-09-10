""""
This module returns for customer and rentals:
    (int) the number of records processed
    (int) the record count in the database prior to running
    (int) the record count after running
    (float) the time taken to run the module.

! mongo tip: use 127.0.0.1 on windows

ref: https://medium.com/swlh/python-meta-programming-d9e06a4d4240
ref: https://stackabuse.com/python-metaclasses-and-metaprogramming/
"""

# pylint: disable=broad-except
# pylint: disable=too-many-locals
# pylint: disable=invalid-name

import logging
import os
import sys
import types
import warnings
from functools import wraps
from timeit import default_timer as timer
import pandas as pd
from pandas import DataFrame
import pymongo as mongodb
from pymongo import MongoClient
from pymongo import collection
from pymongo.errors import ConnectionFailure

# surpress deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning) 

# command line option to turn debugging info on/off
if len(sys.argv) > 1 and sys.argv[1].lower() in ('1', 'y', 'yes'):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# constant
OUTPUT_FILE = 'timings.txt'

def wrapper_timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tm_start = timer()
        result = func(*args, **kwargs)
        tm_end = timer()
        tm_lapsed = tm_end - tm_start
        num_records = 0

        # logging.info('restul type: %s' % type(result))

        if type(result) is None:
            num_records = 0
        elif type(result) is list:
            num_records = len(result[0])
        elif type(result) is dict:
            num_records = len(result)
        elif type(result) is int:
            num_records = result
        elif isinstance(result, pd.DataFrame):
            num_records = len(result.index)
        elif isinstance(result, mongodb.collection.Collection):
            num_records = result.count()

        # log timing result to file
        with open(OUTPUT_FILE, mode='a+') as file:
            file.write('(%s) - %s records processed in %s seconds.\n' % (func.__name__, num_records, tm_lapsed))
            if func.__name__ == '__exit__':
                file.write('%s' % '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                file.write('\n')

        return result
    return wrapper


# A metaclass that replaces methods of its classes
class MetaTime(type):
    """
    Using meta programming to create a timeit wrapper for each function
    """
    def __new__(cls, name, bases, attr):
        """  """
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = wrapper_timeit(value)

        # Return a new type called TimeMetareturn 
        return super(MetaTime, cls).__new__(cls, name, bases, attr)


class MongoDBConnection():
    """ MongoDB Connection """
    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows """
        self.host = host
        self.port = port
        self.connection = None
        logging.debug('Starting Mongo connection ...')

    def __enter__(self):
        """ On entering: creating the connection to Mongo  """
        try:
            self.connection = MongoClient(self.host, self.port)
        except ConnectionFailure as e:
            logging.error('Failed to connect to MongoDB: %s', e)
            raise e
        logging.debug('Mongo connected.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ On exiting: closing the connection to Mongo  """
        if exc_type:
            logging.error('Error: %s', exc_val)
        self.connection.close()
        logging.debug('Mongo connection closed.')


class HpNortonDbApp(metaclass=MetaTime):
    """ HP Norton Database Application """
    def __init__(self):
        """ initializing the HP Norton App  """
        logging.debug('HP Norton App started.')

    def __enter__(self):
        self.record_count_init = {
            "customers": 0,
            "products": 0,
            "rentals": 0
        }
        self.record_count = {
            "customers": 0,
            "products": 0,
            "rentals": 0
        }
        self.err_count = {
            "customers": 0,
            "products": 0,
            "rentals": 0
        }

    def print_mdb_collection(self, collection_name):
        """ print everything in collection_name """
        for doc in collection_name.find():
            print(doc)

    def import_data_csv(self, directory_name, data_file):
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

    def db_collection_init(self, mdb, collection_name):
        """ decorator to initialize mongo collection """
        # create collections if not exist
        logging.debug('Creating the %s collections ...', collection_name)
        collection = mdb[collection_name]

        # clear out the collections and start fresh
        logging.debug('Clearing collection data for %s ...', collection_name)
        collection.drop()

        return collection

    def db_insert(self, mdb_collection, dict_name, name):
        """ using decorator for mongo insert logging """
        try:
            result = mdb_collection.insert_many(dict_name)
            self.record_count[name] = len(result.inserted_ids)
            logging.debug('%s records inserted into Mongodb collection %s.', self.record_count[name], name)
        except Exception as err:
            self.err_count[name] += 1
            logging.debug('Error count incremented by 1 for %s.', name)
            logging.error('%s', err)

        return int(self.record_count[name])

    def import_data_customers(self, mongo, directory_name, customer_file):
        """ import customer data """
        customers = self.db_collection_init(mongo, 'customers')

        logging.debug('Start loading customer data from CSV file ...')
        dict_customer = self.import_data_csv(directory_name, customer_file).to_dict('records')

        return self.db_insert(customers, dict_customer, 'customers')

    def import_data_products(self, mongo, directory_name, product_file):
        """ import product data """
        products = self.db_collection_init(mongo, 'products')

        logging.debug('Start loading product data from CSV file ...')
        dict_product = self.import_data_csv(directory_name, product_file).to_dict('records')

        return self.db_insert(products, dict_product, 'products')

    def import_data_rentals(self, mongo, directory_name, rental_file):
        ''' import rental data '''
        rentals = self.db_collection_init(mongo, 'rentals')

        logging.debug('Start loading rental data from CSV file ...')
        dict_rental = self.import_data_csv(directory_name, rental_file).to_dict('records')

        return self.db_insert(rentals, dict_rental, 'rentals')

    def import_data(self, directory_name, product_file, customer_file, rental_file):
        """ import data from CSV files, then insert into MongoDB """

        mdb = MongoDBConnection()
        with mdb:
            mongo = mdb.connection.HPNorton

            self.import_data_customers(mongo, directory_name, customer_file)
            self.import_data_products(mongo, directory_name, product_file)
            self.import_data_rentals(mongo, directory_name, rental_file)

        tup_customer = (self.record_count['customers']-self.record_count_init['customers'],
                        self.record_count_init['customers'],
                        self.record_count['customers'])
        tup_product = (self.record_count['products']-self.record_count_init['products'],
                    self.record_count_init['products'],
                    self.record_count['products'])

        return [tup_customer, tup_product]

    def show_available_products(self):
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

    def show_rentals(self, product_id):
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ closing the HP Norton App  """
        if exc_type:
            logging.error('Error: %s', exc_val)
        logging.debug('HP Norton App closed.')

if __name__ == '__main__':
    DATA_FILE_CUSTOMER = 'customers_x1000.csv'
    DATA_FILE_PRODUCT = 'products_x1000.csv'
    DATA_FILE_RENTAL = 'rentals_x1000.csv'
    DATA_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    logging.debug('Current directory: %s', DATA_FILE_PATH)

    hp = HpNortonDbApp()

    # in order to call __exit__, we need to use hp as a context manager
    with hp:
        import_status = hp.import_data(DATA_FILE_PATH,
                                DATA_FILE_PRODUCT,
                                DATA_FILE_CUSTOMER,
                                DATA_FILE_RENTAL)
        logging.info(import_status)

        products_available = hp.show_available_products()
        logging.info(products_available)

        users_E0001 = hp.show_rentals('E0001')
        logging.info(users_E0001)
