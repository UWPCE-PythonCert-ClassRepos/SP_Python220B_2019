"""
This program imports the data in exactly the same form as database.py, but in parallel
"""
import logging
import multiprocessing as mp
from timeit import timeit as timer
import csv
import os
import sys
import psutil
from pymongo import MongoClient
sys.path.append(os.path.join(os.path.dirname(__file__), 'csvs'))

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'parallel.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class MongoDBConnection():
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """Initiates the connection settings"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Connects to MongoDB"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Disconnects from MongoDB"""
        self.connection.close()

def import_data(directory_name='csvs', product_file='product_data.csv',
                customer_file='customer_data.csv', rentals_file='rentals_data.csv'):
    """This method will run the full program, and return a tuple containing
    the number of records processed (int), the record count in the database
    prior to running (int), the record count after running (int), and the
    time taken to run the module (float)."""

    manager = mp.Manager()
    count_dict = manager.dict()

    count_dict.setdefault('product_errors', 0)
    count_dict.setdefault('customer_errors', 0)
    count_dict.setdefault('rentals_errors', 0)
    count_dict.setdefault('product_count_before', 0)
    count_dict.setdefault('customer_count_before', 0)
    count_dict.setdefault('product_count_after', 0)
    count_dict.setdefault('customer_count_after', 0)
    count_dict.setdefault('product_time', 0)
    count_dict.setdefault('product_time', 0)
    count_dict.setdefault('customer_time', 0)

    product_process = mp.Process(target=universal_import, args=(directory_name, product_file,
                                                                'product_errors', count_dict))
    product_process.start()
    product_process.join()
    customer_process = mp.Process(target=universal_import, args=(directory_name, customer_file,
                                                                 'customer_errors', count_dict))
    customer_process.start()
    customer_process.join()
    rentals_process = mp.Process(target=universal_import, args=(directory_name, rentals_file,
                                                                'rentals_errors', count_dict))

    rentals_process.join()
    product_tuple = (count_dict['product_count_after'] - count_dict['product_count_before'],
                     count_dict['product_count_before'], count_dict['product_count_after'],
                     count_dict['product_time'])
    customer_tuple = (count_dict['customer_count_after'] - count_dict['customer_count_before'],
                      count_dict['customer_count_before'], count_dict['customer_count_after'],
                      count_dict['customer_time'])
    LOGGER.debug("%s, %s", product_tuple, customer_tuple)
    return product_tuple, customer_tuple

def universal_import(directory_name, file, error_index, count_dict):
    """This method will import any of the .csv files"""

    LOGGER.debug("Importing %s", file)
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        try:
            if file == 'product_data.csv':
                count_dict['product_count_before'] = database.product.count_documents({})
                count_dict['product_time'] = timer('product_file_reader()',
                                                   globals=globals(), number=1)
                count_dict['product_count_after'] = database.product.count_documents({})
            elif file == 'customer_data.csv':
                count_dict['customer_count_before'] = database.customer.count_documents({})
                count_dict['customer_time'] = timer('customer_file_reader()',
                                                    globals=globals(), number=1)
                count_dict['customer_count_after'] = database.customer.count_documents({})
            elif file == 'rentals_data.csv':
                rentals_file_reader()
                count_dict['rentals_count'] = database.rentals.count_documents({})
        except Exception as ex:
            count_dict[error_index] += 1
            LOGGER.warning(ex)
            LOGGER.warning("Something went wrong while reading file")
        LOGGER.debug("Successfully imported %s", file)

    return

def product_file_reader():
    """This method will loop through and read the product_file"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        product = database["product"]
        products_dict = {}
        try:
            with open(os.path.join(os.path.dirname(__file__), 'csvs', 'product_data.csv'),
                      newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    products_dict[row['id']] = {'description': row['description'],
                                                'product_type': row['product_type'],
                                                'quantity_available': row['quantity_available']}
                product.insert_one(products_dict)
        except FileNotFoundError:
            LOGGER.error("Could not find product_data.csv")
    return products_dict

def customer_file_reader():
    """This method will loop through and read the product_file"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        customer = database["customer"]
        customer_dict = {}
        try:
            with open(os.path.join(os.path.dirname(__file__), 'csvs', 'customer_data.csv'),
                      newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    customer_dict[row['id']] = {'name': row['name'], 'address': row['address'],
                                                'phone_number': row['phone_number']}
                customer.insert_one(customer_dict)
        except FileNotFoundError:
            LOGGER.error("Could not find customer_data.csv")
        return customer_dict

def rentals_file_reader():
    """This method will loop through and read the product_file"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        rentals = database["rentals"]
        rentals_dict = {}
        try:
            with open(os.path.join(os.path.dirname(__file__), 'csvs', 'rentals_data.csv'),
                      newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    rentals_dict[row['id']] = {'name': row['name'], 'rentals': row['rentals'].split()}
                rentals.insert_one(rentals_dict)
        except FileNotFoundError:
            LOGGER.error("Could not find rentals_data.csv")
    return rentals_dict

def delete_database():
    """This method deletes the database to reset for other tests"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        database.product.drop()
        database.customer.drop()
        database.rentals.drop()
    LOGGER.debug("Cleared database")

if __name__ == '__main__':
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"

    LOGGER.debug("Parallel program time: %s seconds", timer(
        'import_data()', globals=globals(), number=1))

    LOGGER.debug("This program's cpu usage was: %s%%", psutil.cpu_percent())
