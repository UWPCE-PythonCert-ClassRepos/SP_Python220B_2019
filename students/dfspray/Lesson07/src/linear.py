"""
This program imports the data in the csv files linearly
"""

import logging
import csv
import os
import sys
import psutil
from timeit import timeit as timer
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

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.rental_company

        product_error_count = universal_import(directory_name, product_file, mongo, database)
        customer_error_count = universal_import(directory_name, customer_file, mongo, database)
        rentals_error_count = universal_import(directory_name, rentals_file, mongo, database)

    tuple1 = (database.product.count_documents({}), database.customer.count_documents({}),
              database.rentals.count_documents({}))
    tuple2 = (product_error_count, customer_error_count, rentals_error_count)
    LOGGER.debug("%s, %s", tuple1, tuple2)
    return tuple1, tuple2

def universal_import(directory_name, file, mongo, database):
    """This method will import any of the .csv files"""
    product = database["product"]
    customer = database["customer"]
    rentals = database["rentals"]
    error_count = 0
    LOGGER.debug("Importing %s", file)
    try:
        with open(os.path.join(os.path.dirname(__file__), directory_name, file),
                  newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            file_dict = {}
            try:
                if file == 'product_data.csv':
                    file_dict = product_file_reader(reader, product)
                elif file == 'customer_data.csv':
                    file_dict = customer_file_reader(reader, customer)
                elif file == 'rentals_data.csv':
                    file_dict = rentals_file_reader(reader, rentals)
            except Exception as ex:
                error_count += 1
                LOGGER.warning(ex)
                LOGGER.warning("Something went wrong while reading file")
        LOGGER.debug("Successfully imported %s", file)

    except FileNotFoundError:
        LOGGER.error("could not find %s", file)
        error_count += 1

    return error_count

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
    LOGGER.debug("Linear program time: %s seconds", timer(
                 'import_data()', globals=globals(), number=1))
    LOGGER.debug("This program's cpu usage was: %s%%", psutil.cpu_percent())