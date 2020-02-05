""" Code for lesson07 assignment, adapted from the lesson05 assignment.
"""

import os
import csv
import logging
import queue
from threading import Thread, Lock
from time import process_time
from pymongo import MongoClient

logging.basicConfig(level=logging.ERROR)
LOGGER = logging.getLogger(__name__)

PROCESS_ROW_LOCK = Lock()

RESULTS_QUEUE = queue.Queue(2)

def store_in_queue(func):
    def wrapper(*args):
        RESULTS_QUEUE.put(func(*args))
    return wrapper


class MongoDBConnection():
    """ MongoDB Connection

    This class's code is swiped from "Part 5: Python code" from the lesson05 materials.
    """

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

MONGO = MongoDBConnection()
with MONGO:
    DB = MONGO.connection.media
    PRODUCT_COLLECTION = DB['product']
    CUSTOMER_COLLECTION = DB['customers']
    RENTAL_COLLECTION = DB['rentals']


def import_data(directory_name="csv_files", product_file="product.csv",
                customer_file="customers.csv"):
    """ Note: For lesson07 we are no longer interested in the rentals data.

    Take a directory name and two csv files as input, one with product data, one with customer
    data. Create and populate a MongoDB database with these data. Returns two tuples, one for
    products, the other for customers, containing: number of products processed, tuple with a
    document count of the number documents processed, the number of documents in the collection at
    the beginning, the number of documents in the collection at the end, and the time spent
    importing the documents (in that order).

    Keyword arguments:
    directory_name - the directory that contains the csv_files
    product_file - a csv file with product data with the first line containing the field names
    customer_file - a csv file with customer data with the first line containing the field
                    names
    """
    threads = []

    n_docs_start_products, n_docs_start_customers = count_documents()

    # process products
    path = os.path.join(directory_name, product_file)
    t_import_start = process_time()
    product_thread = Thread(target=populate_collection, args=(path, PRODUCT_COLLECTION,))
    product_thread.start()
    threads.append(product_thread)
    t_product_import_time = process_time() - t_import_start

    # process customers
    path = os.path.join(directory_name, customer_file)
    t_import_start = process_time()
    customer_thread = Thread(target=populate_collection, args=(path, CUSTOMER_COLLECTION,))
    customer_thread.start()
    threads.append(customer_thread)
    t_customer_import_time = process_time() - t_import_start

    for thread in threads:
        thread.join

    n_docs_end_products, n_docs_end_customers = count_documents()

    n_products = 0
    n_customers = 0
    for i in range(2):
        item = RESULTS_QUEUE.get()
        if item[0].name == 'product':
            n_products = item[1]
        else:  # item[0].name == 'customers'
            n_customers = item[1]

    return (n_products, n_docs_start_products, n_docs_end_products, t_product_import_time),\
           (n_customers, n_docs_start_customers, n_docs_end_customers, t_customer_import_time)


def count_documents():
    """ Return the number of documents in the product and customer collections.
    """
    return PRODUCT_COLLECTION.count_documents({}), CUSTOMER_COLLECTION.count_documents({})


@store_in_queue
def populate_collection(file_path, hpn_collection):
    """ Populate a collection with data from a CSV file. Return the number of documents added to
    the collection and the collection.

    Arguments:
    file_path - the path to the CSV file, including the file name.
    hpn_collection - a MongoDB collection
    """
    docs = 0
    threads = []

    with open(file_path, newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            thread = Thread(target=process_row, args=(row, hpn_collection,))
            thread.start()
            threads.append(thread)
            docs += 1

    for thread in threads:
        thread.join()

    return (hpn_collection, docs)


def process_row(row, hpn_collection):
    """ Take the dictionary from a row of data and add the row to the Mongo collection.

    Arguments:
    row - row of data from the input cvs file, already in dictionary format
    hpn_collection - Mongo collection
    """
    with PROCESS_ROW_LOCK:
        with MONGO:
            hpn_collection.insert_one(row)


def main():
    """ Time the program and save the results to a file.
    """
    with open("parallel_file_processing_db_writes.csv", 'w', newline='') as file:
        times = []
        for i in range(1000):
            product_results, customer_results = import_data()

            times.append("{}.,{},{}\n".format(i + 1, product_results[3], customer_results[3]))

        file.writelines(times)


if __name__ == "__main__":
    main()
