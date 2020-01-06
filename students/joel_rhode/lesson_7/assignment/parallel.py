"""
MongoDB database code for HP Norton customer, rental, and inventory system using parallel threads.
"""
# pylint: disable=too-many-locals, unused-argument, unused-variable

from csv import reader
import os
import logging
import threading
from datetime import datetime
from pprint import pprint
from queue import Queue

from pymongo import MongoClient

DATABASE = 'hp_norton_parallel'

LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
LOG_FILE = 'database.log'

FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler(LOG_FILE, delay=True)
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)

LOGGER.setLevel(logging.INFO)

class MongoDBConnection():
    """MongoDB Connection"""
    def __init__(self, host='localhost', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_all_data(directory_name, product_file, customers_file, rentals_file):
    """Imports product, customer, and rental .csv files into the database."""
    start = datetime.now()
    product_fields = ('product_id', 'description', 'product_type', 'quantity_available')
    customer_fields = ('customer_id', 'name', 'address', 'phone_number', 'email')
    rental_fields = ('rental_id', 'product_id', 'customer_id', 'rental_start', 'rental_end')

    threads = []
    # In order to prevent contention, queues are used. Since specific values must be pulled for the
    # results and the order of completion of the threads is unknown, multiple queues are used.
    product_queue = Queue()
    customer_queue = Queue()
    rental_queue = Queue()

    product_thread = threading.Thread(target=import_data, args=(directory_name, product_file,
                                                                'products', product_fields,
                                                                product_queue))
    threads.append(product_thread)
    customer_thread = threading.Thread(target=import_data, args=(directory_name, customers_file,
                                                                 'customers', customer_fields,
                                                                 customer_queue))
    threads.append(customer_thread)
    rental_thread = threading.Thread(target=import_data, args=(directory_name, rentals_file,
                                                               'rentals', rental_fields,
                                                               rental_queue))
    threads.append(rental_thread)
    for thread in threads:
        thread.start()
        thread.join()

    product_count, prod_init_db_size, prod_errors = product_queue.get()
    customer_count, cust_init_db_size, cust_errors = customer_queue.get()
    rental_count, rental_init_db_size, rent_errors = rental_queue.get()


    end = datetime.now()
    return [(customer_count, cust_init_db_size, cust_init_db_size + customer_count,
             (end - start).total_seconds()),
            (product_count, prod_init_db_size, prod_init_db_size + product_count,
             (end - start).total_seconds())]


def import_data(directory_name, csv_file, db_target, fields, work_queue):
    """Read csv file of data with fields and place into Mongo db with collection db_target"""
    item_list, error_count = read_csv(directory_name, csv_file, fields)
    item_count, initial_db_size = write_many_to_database(DATABASE, db_target, item_list)
    work_queue.put((item_count, initial_db_size, error_count))
    return item_count, initial_db_size, error_count


def read_csv(directory_name, file_name, fields):
    """Reads csv file and puts results into list of dictionaries with keys per fields parameter."""
    csv_list = []
    error_count = 0
    with open(os.path.join(directory_name, file_name), newline='') as csv_file:
        for row in reader(csv_file):
            try:
                assert len(fields) == len(row)
                csv_list.append(dict(zip(fields, row)))
            except AssertionError:
                logging.warning('Mismatch in line data length. Expected %d items but data has'
                                '%d items. Line: %s', len(fields), len(row), row)
                error_count += 1
    return csv_list, error_count


def write_many_to_database(database_name, collection, data_list):
    """Inserts data_dict to collection in MongoDB database."""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection[database_name]
        collection = database[collection]
        initial_size = collection.count_documents({})
        result = collection.insert_many(data_list)
    if result.acknowledged:
        return len(result.inserted_ids), initial_size
    return False


def show_available_products(database_name=DATABASE, collection='products'):
    """Returns a dictionary with all products listed as available in the database."""
    mongo = MongoDBConnection()
    products_avail = {}
    with mongo:
        database = mongo.connection[database_name]
        product_query = database[collection].find({'quantity_available': {'$gt': '0'}})
        for product in product_query:
            products_avail[product['product_id']] = product
            del products_avail[product['product_id']]['_id']
    return products_avail


def show_rentals(product_id, database_name=DATABASE):
    """Returns a dictionary of user data for all users that have rented specified product id."""
    mongo = MongoDBConnection()
    rental_customers = {}
    with mongo:
        database = mongo.connection[database_name]
        for rental in database['rentals'].find({'product_id': product_id}):
            try:
                customer = database['customers'].find_one({'customer_id': rental['customer_id']})
                rental_customers[customer['customer_id']] = customer
                del rental_customers[customer['customer_id']]['_id']
            except KeyError:
                logging.error('Key not found in database.')
                raise
    return rental_customers


if __name__ == '__main__':
    pprint(import_all_data('sample_csv_files', 'products.csv', 'customers.csv', 'rentals.csv'))
