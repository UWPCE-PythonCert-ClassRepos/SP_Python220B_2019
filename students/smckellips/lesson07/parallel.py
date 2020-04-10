# pylint: disable=C0103,R0914
'''HP Norton Inventory System based on MongoDB.'''
import csv
import datetime
import logging
import queue
# import asyncio
# import aiofiles
import threading

from pymongo import MongoClient

DB_NAME = 'Inventory'
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'
FORMATTER = logging.Formatter(LOG_FORMAT)

FH = logging.FileHandler(LOG_FILE)
CH = logging.StreamHandler()
FH.setFormatter(FORMATTER)
CH.setFormatter(FORMATTER)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FH)
# LOGGER.addHandler(CH)

RESULT_QUEUE = queue.Queue()


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        self.db = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        self.db = self.connection[DB_NAME]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    Maintain original signature.  Wrap concurrent functions here.
    DB calls are handled by external dependency.
    Only opportunity for concurrency is importing the three data files.
    '''
    LOGGER.info("Beginning import_data")
    prod_start_count = document_count('Product')
    cust_start_count = document_count('Customer')

    start = datetime.datetime.now()

    product_thread = threading.Thread(target=import_file, args=(
        directory_name, product_file, 'Product', 'product_id'))
    customer_thread = threading.Thread(target=import_file, args=(
        directory_name, customer_file, 'Customer', 'customer_id'))
    rentals_thread = threading.Thread(target=import_file, args=(
        directory_name, rentals_file, 'Rental', 'rental_id'))
    threads = [product_thread, customer_thread, rentals_thread]

    for thread in threads:
        thread.start()

    # Wait for all threads to complete before moving on.
    for thread in threads:
        thread.join()

    end = datetime.datetime.now()

    prod_end_count = document_count('Product')
    cust_end_count = document_count('Customer')

    results = {}
    for _ in range(RESULT_QUEUE.qsize()):
        result = RESULT_QUEUE.get()
        results[result[0]] = {'processed': result[1], 'time': result[2]}
        LOGGER.info("results: %s, %s, %s.",
                    result[0], result[1], result[2])

    results['products.csv']['start'] = prod_start_count
    results['products.csv']['end'] = prod_end_count
    results['customers.csv']['start'] = cust_start_count
    results['customers.csv']['end'] = cust_end_count

    LOGGER.info("Total run time: %s", end-start)

    products_results = (
        results['products.csv']['processed'],
        results['products.csv']['start'],
        results['products.csv']['end'],
        results['products.csv']['time'])
    customers_results = (
        results['customers.csv']['processed'],
        results['customers.csv']['start'],
        results['customers.csv']['end'],
        results['customers.csv']['time'])

    return [products_results, customers_results]


def import_file(directory_name, data_file, db_name, key):
    '''
    Original import function refactored to process a single file.
    Locking around the shared log file and queue to avoid contention.
    '''
    mongo = MongoDBConnection()
    count = 0
    start_time = datetime.datetime.now()
    with threading.Lock():
        LOGGER.info("Importing %s at %s.",
                    data_file, start_time)

    with open(f'{directory_name}/{data_file}', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # with threading.Lock():
            result = insert_db(mongo, db_name, row)
            if result:
                count += 1
                with threading.Lock():
                    LOGGER.info("Adding %s to collection %s. ID: %s",
                                row[key], db_name, result)
            else:
                with threading.Lock():
                    LOGGER.warning("Failed to add %s to database.",
                                   row[key])
    end_time = datetime.datetime.now()
    # Result queue is shared resource and requires locking.
    with threading.Lock():
        RESULT_QUEUE.put((data_file, count, str(end_time - start_time)))


def orig_import_data(directory_name, product_file, customer_file, rentals_file):
    '''Linear import data function'''
    mongo = MongoDBConnection()

    inv_map = {}
    inv_map[product_file] = {'Name': 'Product',
                             'key': 'product_id', 'count': 0, 'errors': 0}
    inv_map[customer_file] = {'Name': 'Customer',
                              'key': 'customer_id', 'count': 0, 'errors': 0}
    inv_map[rentals_file] = {'Name': 'Rental',
                             'key': 'rental_id', 'count': 0, 'errors': 0}

    for file_name in inv_map:
        with open(f'{directory_name}/{file_name}', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                result = insert_db(mongo, inv_map[file_name]['Name'], row)
                if result:
                    inv_map[file_name]['count'] += 1
                    LOGGER.info("Adding %s to collection %s. ID: %s",
                                row[inv_map[file_name]['key']], inv_map[file_name]['Name'], result)
                else:
                    inv_map[file_name]['errors'] += 1
                    LOGGER.warning("Failed to add %s to database.",
                                   row[inv_map[file_name]['key']])

    count_tuple = (inv_map[product_file]['count'], inv_map[customer_file]
                   ['count'], inv_map[rentals_file]['count'])
    error_tuple = (inv_map[product_file]['errors'], inv_map[customer_file]
                   ['errors'], inv_map[rentals_file]['errors'])
    return count_tuple, error_tuple


def insert_db(context_mgr, collection_name, record):
    '''
    Insert records function, using provided db, collection.
    Should not use context manager for each row for bulk import.
    Would need second "bulk" insert function that assumes you're already
    in a context manager.
    '''
    with context_mgr:
        collection = context_mgr.db[collection_name]

        result = None
        if isinstance(record, list):
            result = collection.insert_many(record).inserted_ids
        elif isinstance(record, dict):
            result = collection.insert_one(record).inserted_id
        else:
            raise NotImplementedError
        return result


def document_count(collection):
    '''Retrieve collection document count.'''
    mongo = MongoDBConnection()
    with mongo:
        collection = mongo.db[collection]
        record_count = collection.count_documents({})
    return record_count


def list_products():
    '''List all product ID's with no filtering.'''
    mongo = MongoDBConnection()

    with mongo:
        collection = mongo.db['Product']
        products = [x['product_id'] for x in collection.find()]
    return products


def list_available_products():
    '''List all products with inventory available.'''
    mongo = MongoDBConnection()

    with mongo:
        collection = mongo.db['Product']
        wanted_attribs = ['product_id', 'description',
                          'product_type', 'quantity_available']
        # return value here includes mongo ID.  Remove to hide implementation detail.
        # products = [x for x in collection.find({'quantity_available': {'$gt': '0'}})]
        products = list(collection.find({'quantity_available': {'$gt': '0'}}))
        san_products = []
        for product in products:
            san_products.append(
                {x: product[x] for x in product if x in wanted_attribs})
    return san_products


def show_rentals(product_id):
    '''Show customer information who rented specified product.'''
    mongo = MongoDBConnection()

    with mongo:
        collection = mongo.db['Rental']
        rental_customers = [x['customer_id']
                            for x in collection.find({'product_id': product_id})]

        collection = mongo.db['Customer']
        unwanted_attribs = ['_id', 'credit_limit']
        san_customers = []
        # customers = [x for x in collection.find({'customer_id': { "$in": rental_customers}})]
        customers = list(collection.find(
            {'customer_id': {"$in": rental_customers}}))
        for customer in customers:
            san_customers.append(
                {x: customer[x] for x in customer if x not in unwanted_attribs})

    return san_customers


if __name__ == "__main__":
    # count, errors = read_source(MongoDBConnection(),'data/customers.csv','Customer')
    product_tuple, customer_tuple = import_data(
        'data', 'products.csv', 'customers.csv', 'rentals.csv')
    LOGGER.info("Product results: %s", product_tuple)
    LOGGER.info("Customer results: %s", customer_tuple)
