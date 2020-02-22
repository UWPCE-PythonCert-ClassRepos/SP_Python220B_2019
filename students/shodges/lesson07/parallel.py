"""
Methods to allow processing of HP Norton inventory, including:

drop_data() to clear the inventory db
import_data(directory_name, product_file, customer_file, rentals_file) to intake existing CSV's
show_available_products() to show available products, accounting for existing rentals
show_rentals(product_id) to show all active rentals for product_id
"""
# pylint: disable=dangerous-default-value, too-many-arguments
import csv
import datetime
import logging
import threading
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

class ImportData(threading.Thread):
    """
    Class to allow multithreading of data imports.
    """

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        """
        Override Thread __init__ to initialize analysis variables and allow run to leverage needed
        kwargs.

        Pass in file, which should be a Path to the correct file, and type, which should be:
        customers, products, or rentals
        """
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._processed = None
        self._startcount = None
        self._endcount = None
        self._starttime = None
        self._runtime = None
        self._file = kwargs['file']
        self._type = kwargs['type']

    def run(self):
        """
        Run the CSV import and DB insert.
        """
        self._starttime = datetime.datetime.now()

        with open(self._file, mode='r') as csv_input:
            import_list = list(csv.DictReader(csv_input))
            logging.debug('Read in %s data from %s: %s', self._type, self._file.name, import_list)
            self._processed = len(import_list)

        mongo = DBConnection()

        with mongo:
            inv_db = mongo.connection.media
            type_table = inv_db[self._type]

            self._startcount = type_table.count_documents({})

            import_res = type_table.insert_many(import_list)
            if import_res.acknowledged is True:
                logging.debug('Wrote %d records to %s', len(import_res.inserted_ids), self._type)
            else:
                logging.warning('Failed to write records to %s', self._type)

            self._endcount = type_table.count_documents({})

        self._runtime = (datetime.datetime.now() - self._starttime).total_seconds()

        logging.debug('Database import complete in %d seconds', self._runtime)

    def join(self, timeout=None):
        """
        Override Thread join function to return tuple for analysis.
        """
        threading.Thread.join(self, timeout)
        return (self._processed, self._startcount, self._endcount, self._runtime)


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
    prod_import = ImportData(kwargs={'type': 'products', 'file': data_directory/product_file})
    cust_import = ImportData(kwargs={'type': 'customers', 'file': data_directory/customer_file})
    rent_import = ImportData(kwargs={'type': 'rentals', 'file': data_directory/rentals_file})

    prod_import.start()
    cust_import.start()
    rent_import.start()

    prod_res = prod_import.join()
    cust_res = cust_import.join()
    rent_import.join()

    return (prod_res, cust_res)

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
