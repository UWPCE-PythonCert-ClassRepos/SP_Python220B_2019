# pylint: disable=R0914, C0103
'''
Linear vs parallelization lesson (linear module)
Testing insert_one
'''
import csv
import os
import logging
import time
from pymongo import MongoClient

#logging setup
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

#formatting and file name
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = 'db.log'

#handling setup
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


class MongoDBConnection():
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

def dict_to_import(database, file):
    '''func takes a csvfile and reads in each row into a database'''
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_entry = {}
            for key, val in row.items():
                new_entry[key] = val
            database.insert_one(new_entry)


def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    Function takes a directory name and three csv files as input (product data,
    customer data, rentals data) and imports to a MongoDB database.
    Returns list of 2 tuples:
    1) Customer
    2) products

    Each tuple will contain 4 values: the number of records processed (int),
    the record count in the database prior to running (int),
    the record count after running (int),
    and the time taken to run the module (float).
    '''

    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        #Create product collection
        p_time_start = time.time()
        product_db = db['product']
        initial_product_count = product_db.count_documents({})
        try:
            dict_to_import(product_db, os.path.join(directory_name, product_file))
            final_product_count = product_db.count_documents({})
            p_time_end = time.time()
            p_elapsed = (p_time_end - p_time_start)
            LOGGER.info('Product info addition took %s', p_elapsed)
            product_tuple = ((final_product_count-initial_product_count),
                             initial_product_count,
                             final_product_count, p_elapsed)
        except FileNotFoundError:
            pass

        #Create customer collection
        c_time_start = time.time()
        customer_db = db['customer']
        initial_cust_count = customer_db.count_documents({})
        try:
            dict_to_import(customer_db, os.path.join(directory_name, customer_file))
            final_cust_count = customer_db.count_documents({})
            c_time_end = time.time()
            c_elapsed = (c_time_end - c_time_start)
            LOGGER.info('Customer info addition took %s', c_elapsed)
            customer_tuple = ((final_cust_count - initial_cust_count),
                              initial_cust_count,
                              final_cust_count, c_elapsed)
        except FileNotFoundError:
            pass

        #Create rentals collection
        rentals_db = db['rentals']

        try:
            dict_to_import(rentals_db, os.path.join(directory_name, rentals_file))
            LOGGER.info('Rentals info added to database')
        except FileNotFoundError:
            pass

    return [customer_tuple, product_tuple]

#Was using to easily time and make sure correct entry counts
#if __name__ == '__main__':
#    START_TIME = time.time()
#    RESULTS = import_data('csv_files', 'product_file.csv',
#                          'customer_file.csv', 'rental_file.csv')
#    END_TIME = time.time()
#    print('total time is', END_TIME-START_TIME)
#    print(RESULTS)
