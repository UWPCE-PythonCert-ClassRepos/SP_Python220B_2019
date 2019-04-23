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
    """This function takes a directory name and three csv files and creates/populates a new
       MongoDB database with the data. It then returns two tuples: The first contains a record
       count of the number of products, customers and rentals added. The second contains a count
       of any errors that occurred in products, customers, and rentals"""

    manager = mp.Manager()
    count_dict = manager.dict()

    product_process = mp.Process(target=universal_import, args=(directory_name, product_file,
                                                                'product_errors', count_dict))
    product_process.start()
    customer_process = mp.Process(target=universal_import, args=(directory_name, customer_file,
                                                                 'customer_errors', count_dict))
    customer_process.start()
    rentals_process = mp.Process(target=universal_import, args=(directory_name, rentals_file,
                                                                'rentals_errors', count_dict))
    rentals_process.start()
    product_process.join()
    customer_process.join()
    rentals_process.join()
    tuple1 = (count_dict['product_count'], count_dict['customer_count'],
              count_dict['rentals_count'])
    tuple2 = (count_dict['product_errors'], count_dict['customer_errors'],
              count_dict['rentals_errors'])
    LOGGER.debug("%s, %s", tuple1, tuple2)
    return tuple1, tuple2

def universal_import(directory_name, file, error_index, count_dict):
    """This method will import any of the .csv files"""
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.rental_company
        count_dict.setdefault('product_errors', 0)
        count_dict.setdefault('customer_errors', 0)
        count_dict.setdefault('rentals_errors', 0)
        count_dict.setdefault('product_count', 0)
        count_dict.setdefault('customer_count', 0)
        count_dict.setdefault('rentals_count', 0)
        product = database["product"]
        customer = database["customer"]
        rentals = database["rentals"]
        LOGGER.debug("Importing %s", file)
        try:
            with open(os.path.join(os.path.dirname(__file__), directory_name, file),
                      newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                file_dict = {}
                try:
                    if file == 'product_data.csv':
                        file_dict = product_file_reader(reader, product)
                        count_dict['product_count'] = database.product.count_documents({})
                    elif file == 'customer_data.csv':
                        file_dict = customer_file_reader(reader, customer)
                        count_dict['customer_count'] = database.customer.count_documents({})
                    elif file == 'rentals_data.csv':
                        file_dict = rentals_file_reader(reader, rentals)
                        count_dict['rentals_count'] = database.rentals.count_documents({})
                except Exception as ex:
                    count_dict[error_index] += 1
                    LOGGER.warning(ex)
                    LOGGER.warning("Something went wrong while reading file")
            LOGGER.debug("Successfully imported %s", file)

        except FileNotFoundError:
            LOGGER.error("could not find %s", file)
            count_dict[error_index] += 1
        return

def product_file_reader(reader, product):
    """This method will loop through and read the product_file"""
    products_dict = {}
    for row in reader:
        products_dict[row['id']] = {'description': row['description'],
                                    'product_type': row['product_type'],
                                    'quantity_available': row['quantity_available']}
    product.insert_one(products_dict)
    return products_dict

def customer_file_reader(reader, customer):
    """This method will loop through and read the product_file"""
    customer_dict = {}
    for row in reader:
        customer_dict[row['id']] = {'name': row['name'], 'address': row['address'],
                                     'phone_number': row['phone_number']}
    customer.insert_one(customer_dict)
    return customer_dict

def rentals_file_reader(reader, rentals):
    """This method will loop through and read the product_file"""
    rentals_dict = {}
    for row in reader:
        rentals_dict[row['id']] = {'name': row['name'], 'rentals': row['rentals'].split()}
    rentals.insert_one(rentals_dict)
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
    LOGGER.debug("Linear program time: %s seconds", timer(
                 'import_data()', globals=globals(), number=1))


    LOGGER.debug("This program's cpu usage was: %s%%", psutil.cpu_percent())
