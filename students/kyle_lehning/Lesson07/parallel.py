#!/usr/bin/env python3
"""Migration of product data from csv into MongoDB"""
import threading
import logging
import datetime
import time
import os
from timeit import timeit as timer
from pymongo import MongoClient


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


def __setup_logger(name, log_file, level=logging.WARNING, stream=True):
    """
    This function sets up loggers.
    """
    log_format = logging.Formatter("%(asctime)s%(filename)s:%(lineno)-3d %(levelname)s %(message)s")
    handler = logging.FileHandler(log_file)
    handler.setFormatter(log_format)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    if stream is True:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)
        logger.addHandler(stream_handler)
    return logger


MONGO = MongoDBConnection()
LOG_FILE = 'parallel' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
LOGGER = __setup_logger('database_logger', LOG_FILE, logging.DEBUG)


def import_data(directory_name, product_file, customer_file, rental_file):  # pylint: disable=R0914
    """
    This function takes a directory name and three csv files as input, one with product data,
    one with customer data, and the third one with rentals data. It creates and populates a new
    MongoDB database with these data. It returns a list with 3 tuples for customers, products, and
    rentals. Each tuple will contain 4 values: the number of records processed (int), the record
    count in the database prior to running (int), the record count after running (int), and the time
    taken to run the module (float)
    """
    db_names = __set_collection_names()
    # contention is avoided by having each thread write to a different list
    customer_list = []
    product_list = []
    rental_list = []
    with MONGO:
        # mongodb database
        db = MONGO.connection.media  # pylint: disable=C0103
        # different database locations are used to avoid contention
        products = db[db_names[0]]
        customers = db[db_names[1]]
        rentals = db[db_names[2]]
        product_thread = threading.Thread(target=write_to_db, args=(products, product_file,
                                                                    directory_name, product_list)
                                          )
        product_thread.start()
        customer_thread = threading.Thread(target=write_to_db, args=(customers, customer_file,
                                                                     directory_name, customer_list)
                                           )
        customer_thread.start()
        rental_thread = threading.Thread(target=write_to_db, args=(rentals, rental_file,
                                                                   directory_name, rental_list)
                                         )
        rental_thread.start()
        # The following joins are used to ensure the return contains info from all threads
        product_thread.join()
        customer_thread.join()
        rental_thread.join()
        return_list = [tuple(customer_list), tuple(product_list), tuple(rental_list)]
        LOGGER.info("Returned: %s", return_list)
        return return_list


def write_to_db(db, file_name, directory_name, return_list):  # pylint: disable=C0103
    """
    Takes a database, a csv file name, the directory of the csv file, and a list that will be
    written to. The csv file is then read through and written to the return_list.
    """
    start_time = time.time()
    total_error = 0
    start_count = db.count_documents({})
    try:
        read_list = __read_csv(os.path.join(directory_name, file_name))
        read_dict = __make_mongo_dictionary(read_list)
        db_result = db.insert_many(read_dict)
        insert_count = len(db_result.inserted_ids)
    except FileNotFoundError:
        total_error += 1
        insert_count = 0
    final_count = db.count_documents({})
    end_time = time.time()
    total_time = end_time - start_time
    return_list.append(insert_count)
    return_list.append(start_count)
    return_list.append(final_count)
    return_list.append(total_time)


def __make_mongo_dictionary(passed_list):
    """Makes a dictionary from a list who's first item is keys"""
    keys = passed_list.pop(0)
    return_dictionary = []
    for line in passed_list:
        return_dictionary.append(dict(zip(keys, line)))
    return return_dictionary


def __read_csv(passed_file):
    """Make a list from a csv file"""
    return_list = []
    with open(passed_file) as passed_csv:
        for line in passed_csv:
            data_line = line.rstrip().split(',')
            return_list.append(data_line)
    return return_list


def __set_collection_names():
    """Set names with function so that this can be mocked for testing"""
    return ['products', 'customers', 'rentals']


if __name__ == '__main__':
    LOGGER.info('timeit run: %s', timer("import_data('', 'Products.csv', 'Customers.csv', "
                                        "'Rentals.csv')", globals=globals(), number=10))
    erase_db_names = __set_collection_names()  # pylint: disable=C0103
    with MONGO:
        erase_db = MONGO.connection.media # pylint: disable=C0103
        erase_db[erase_db_names[0]].drop()
        erase_db[erase_db_names[1]].drop()
        erase_db[erase_db_names[2]].drop()
