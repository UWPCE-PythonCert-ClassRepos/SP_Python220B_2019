"""
Create database for products, customers, and rentals.
"""
import logging
import csv
import os
import time
from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'linear.log'

FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE, mode='w')
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()

CONSOLE_HANDLER.setFormatter(FORMATTER)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

class MongoDBConnection():
    """
    MongoDB Connection
    """
    def __init__(self, host='127.0.0.1', port=27017):
        """
        Init
        """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """
        Enter
        """
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit
        """
        self.connection.close()


def csv_to_dict(file):
    """
    Creates a list of dictionaries from a csv file
    """
    with open(file) as csv_file:
        key_val_list = []
        for row in csv.DictReader(csv_file):
            temp_dict = {}
            for key, val in row.items():
                temp_dict[key] = val
            key_val_list.append(temp_dict)
    return key_val_list

def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    This function takes a directory name and three csv files as input, one
    with product data, one with customer data and the third one with rentals
    data and creates and populates a new MongoDB database with these data. It
    returns two tuples the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a
    count of any errors that occurred, in the same order.
    """
    start_time = time.time()
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        products = database['products']
        customers = database['customers']
        rentals = database['rentals']

        products_before = products.count_documents({})
        customers_before = customers.count_documents({})

        product_path = os.path.join(directory_name, product_file)
        customer_path = os.path.join(directory_name, customer_file)
        rental_path = os.path.join(directory_name, rentals_file)

        products.insert_many(csv_to_dict(product_path))
        products_count = len(csv_to_dict(product_path))
        logging.info("Successfully added product data to database.")

        customers.insert_many(csv_to_dict(customer_path))
        customers_count = len(csv_to_dict(customer_path))
        logging.info("Successfully added customer data to database.")

        rentals.insert_many(csv_to_dict(rental_path))
        logging.info("Successfully added rental data to database.")

        products_after = products.count_documents({})
        customers_after = customers.count_documents({})

        exec_time = time.time() - start_time

        products_tuple = (products_count, products_before, products_after,
                          exec_time)
        customers_tuple = (customers_count, customers_before, customers_after,
                           exec_time)

        return [products_tuple, customers_tuple]

def drop_db():
    """
    Clear the database
    """
    logging.info("Clearing the database")
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
        database.products.drop()
        database.customers.drop()
        database.rentals.drop()
