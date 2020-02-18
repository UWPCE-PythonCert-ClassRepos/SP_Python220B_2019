"""
Module to establish mongo database, add and view data.
"""
# pylint: disable=invalid-name

import timeit
import time
import logging
import os
from functools import partial
from multiprocessing import Process, Queue, Pool
from pymongo import MongoClient
import pandas as pd

main_time = time.time()

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
LOGGER.setLevel(logging.DEBUG)


class MongoDBConnection:
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


def pool_import(directory_name, product_file, customer_file, rental_file):
    """Use pool multiprocessing to import data."""
    with Pool(processes=3) as pool:
        files = (product_file, customer_file, rental_file)
        database_names = ('products', 'customers', 'rentals')
        f = partial(import_data_pool, directory_name)
        counts = pool.starmap(f, zip(files, database_names))
    return counts


def parallel_import(directory_name, product_file, customer_file, rental_file):
    """Add three files at directory to mongo db."""
    files = (product_file, customer_file, rental_file)
    database_names = ('products', 'customers', 'rentals')
    processes = []
    return_list = []
    q = Queue()

    for file_name, database_name in zip(files, database_names):
        process = Process(target=import_data, args=(directory_name, file_name, database_name, q))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    for _ in processes:
        ret = q.get()
        return_list.append(ret)
    return return_list


def import_data(directory_name, file_name, database_name, queue):
    """Add three files at directory to mongo db and return tuples of items added and errors."""
    start_time = time.time()
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        database = db[database_name]
        LOGGER.debug('Attempting to load %s.', file_name)

        init_record_count = database.count_documents({})
        try:
            data, count = import_csv(directory_name, file_name)
            database.insert_many(data)
            LOGGER.debug('Successful addition to %s.', database)

        except FileNotFoundError as error:
            LOGGER.error('Error %s loading %s.', error, file_name)
            count = 0

        final_record_count = database.count_documents({})
        t = (count, init_record_count, final_record_count, time.time() - start_time, )
        queue.put(t)


def import_data_pool(directory_name, file_name, database_name):
    """Add three files at directory to mongo db and return tuples of items added and errors."""
    start_time = time.time()
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        database = db[database_name]
        LOGGER.debug('Attempting to load %s.', file_name)

        init_record_count = database.count_documents({})
        try:
            data, count = import_csv(directory_name, file_name)
            database.insert_many(data)
            LOGGER.debug('Successful addition to %s.', database)

        except FileNotFoundError as error:
            LOGGER.error('Error %s loading %s.', error, file_name)
            count = 0

        final_record_count = database.count_documents({})
        return(count, init_record_count, final_record_count, time.time() - start_time, )


def show_available_products():
    """Return dict of dicts showing available products."""
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
    """Return dict of dicts showing the customers renting the product with product_id argument."""
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        rentals = db['rentals']
        customers = db['customers']
        renters = {}
        rentals_found = rentals.find({'product_id': product_id})
        if rentals_found:
            for rental in rentals_found:
                if not rental:
                    LOGGER.warning('Product ')
                for customer in customers.find({'customer_id': rental['customer_id']}):
                    renters[customer['customer_id']] = {
                        'name': customer['name'],
                        'address': customer['address'],
                        'phone_number': customer['phone_number'],
                        'email': customer['email']
                    }
        else:
            LOGGER.warning('Product not found in database.')
        return renters


def clear_database():
    """Delete database."""
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        db['products'].drop()
        db['customers'].drop()
        db['rentals'].drop()
        LOGGER.debug('Cleared database.')


def main():
    """Call import data with canned inputs. Included for command line use."""
    return parallel_import('sample_csv_files/', 'customers.csv', 'products.csv', 'rentals.csv')


if __name__ == "__main__":
    print(timeit.timeit("pool_import('sample_csv_files/', 'customers.csv', "
                        "'products.csv', 'rentals.csv')",
                        globals=globals(),
                        setup='from __main__ import pool_import',
                        number=1))
