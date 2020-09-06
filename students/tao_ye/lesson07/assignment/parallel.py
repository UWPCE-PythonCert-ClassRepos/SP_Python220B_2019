"""
Use mongoDB for data storage, concurrent version
"""
import logging
import csv
import time
import concurrent.futures as cf
from pymongo import MongoClient

DATABASE = "norton_furniture"
PRODUCT_COLLECTION = "product"
CUSTOMER_COLLECTION = "customer"
RENTALS_COLLECTION = "rentals"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a logging "formatter"
LOG_FORMAT = "%(filename)s:%(lineno)-3d %(message)s"
formatter = logging.Formatter(LOG_FORMAT)

# Create a log message handler that sends output to log_file
file_handler = logging.FileHandler('parallel.log', mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class MongoDBConnection():
    """ MongoDB Connection context manager class """

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


def import_data_parallel(directory_name, product_file, customer_file, rentals_file):
    """
    Read data from CSV files and save to MongoDB

    Return a list of tuples, one tuple for customer and one for products.
    Each tuple will contain 4 values: the number of records processed (int),
    the record count in the database prior to running (int), the record count
    after running (int), and the time taken to run the module (float).
    """

    # multithreading to import from 3 files concurrently
    start = time.perf_counter()
    with cf.ThreadPoolExecutor(max_workers=3) as executor:
        future_product = executor.submit(import_one_file,
                                         PRODUCT_COLLECTION, directory_name, product_file)
        future_customer = executor.submit(import_one_file,
                                          CUSTOMER_COLLECTION, directory_name, customer_file)
        executor.submit(import_one_file,
                        RENTALS_COLLECTION, directory_name, rentals_file)
    end = time.perf_counter()
    logger.info(f"Concurrent import takes {end - start} seconds.")

    (record_processed, before_count, after_count) = future_product.result()
    product_tuple = (record_processed, before_count, after_count, end - start)
    (record_processed, before_count, after_count) = future_customer.result()
    customer_tuple = (record_processed, before_count, after_count, end - start)

    return [customer_tuple, product_tuple]


def import_one_file(collection_name, directory, file_name):
    """ read one CSV file and save to MongoDB """
    with MongoDBConnection() as mongo:

        database = mongo.connection[DATABASE]

        error_count = 0
        try:
            new_collection = database[collection_name]
            before_count = new_collection.count_documents({})
            record_processed = 0
            with open(directory + '/' + file_name, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)  # return an ordered dictionary
                for row in csv_reader:
                    new_collection.insert_one(row)
                    record_processed += 1
        except (FileNotFoundError, TypeError):
            error_count += 1

        after_count = new_collection.count_documents({})

        return record_processed, before_count, after_count
