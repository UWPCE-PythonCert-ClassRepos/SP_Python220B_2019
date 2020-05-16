# parallel_with_lock.py
""" This module defines all the functions for HP Norton MongoDB database"""
import os
import csv
import sys
import logging
import time
import threading
import queue
from linear import MongoDBConnection


processed_records = queue.Queue()

# set logging configuration
LOG_FORMAT = "%(levelname)s %(filename)s %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class Counter_With_Lock():
    """ This class defines a counter """
    def __init__(self, start=0):
        self.value = start
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1


def read_thousand_csv_file(dir_name, csv_file, collection, counter):
    records_num = 0
    try:
        filename = os.path.join(dir_name, csv_file)
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                counter.increment()
                collection.insert_one(row)
                records_num += 1
    except FileNotFoundError:
        LOGGER.info('FileNotFoundError')
        sys.exit()
    except Exception as error:
        LOGGER.info('Exception:')
        LOGGER.info(error)
        sys.exit()
    processed_records.put(records_num)


def import_thousand_data(dir_name, product_file, customer_file, rentals_file):
    """ This function takes a directory name three csv files as input, one with
        product data, one with customer data and the third one with rentals
        data and creates and populates a new MongoDB database with these data.
        It returns a list of tuples, one tuple for customer & one for products.
        Each tuple will contain 4 values: the number of records processed (int),
        the record count in the database prior to running (int), the record
        count after running (int), and the time taken to run the module (float).
    """
    counter = Counter_With_Lock()
    client = MongoDBConnection()
    with client:
        hp_norton_db = client.connection.rental
        products = hp_norton_db['products']
        customers = hp_norton_db['customers']
        rentals = hp_norton_db['rentals']
        exist_products = products.count()
        exist_customers = customers.count()
        exist_rentals = rentals.count()

        # 1. load the products collection parallel
        start = time.time()
        LOGGER.info('Start the products collection thread')
        pro_thread = threading.Thread(target=read_thousand_csv_file,
                                      args=(dir_name, product_file, products,
                                            counter))
        pro_thread.start()

        # 2. load the customers collection parallel
        start = time.time()
        LOGGER.info('Start the customers collection thread')
        cust_thread = threading.Thread(target=read_thousand_csv_file,
                                       args=(dir_name, customer_file,
                                             customers, counter))
        cust_thread.start()
        # 3. load the rentals collection parallel
        LOGGER.info('Start the rentals collection thread')
        rent_thread = threading.Thread(target=read_thousand_csv_file,
                                       args=(dir_name, rentals_file,
                                             rentals, counter))
        rent_thread.start()

        ####################################################
        # let the main thread wait for each thread finishing.
        pro_thread.join()
        product_tuple = (processed_records.get(), exist_products,
                         products.count(), time.time() - start)

        cust_thread.join()
        customer_tuple = (processed_records.get(), exist_customers,
                          customers.count(), time.time() - start)

        rent_thread.join()
        rental_tuple = (processed_records.get(), exist_rentals,
                        rentals.count(), time.time() - start)

        LOGGER.info(f'Return product tuple {product_tuple}')
        LOGGER.info(f'Return customer tuple {customer_tuple}')
        LOGGER.info(f'Return rental tuple {rental_tuple}')
        LOGGER.info('Total record prcessed for all three files:'
                    f'{counter.value}')
        return [product_tuple, customer_tuple]
