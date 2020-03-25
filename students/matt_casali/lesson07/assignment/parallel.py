#!/usr/bin/env python3

"""
Creates a Mongo database connection, adds data, and queries data
"""

# pylint: disable= R0915, E0401, R0914, C0103, W1202, W0612

import csv
import logging
import os
import time
import threading
from queue import Queue
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)


class MongoDBConnection():
    """
    Connect to Mongo database, opens and closes.
    """

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name, product_file, customer_file):
    """
    Creates a connection to Mongo database, clears data, and updates with data from CSVs
    """

    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.hpn
        logging.info("Creating Mongo database.")

        products = db["products"]
        customers = db["customers"]

        logging.info("Dropping old data.")
        db.products.drop()
        db.customers.drop()

        product_csv = os.path.join(directory_name, product_file)
        customer_csv = os.path.join(directory_name, customer_file)

        csvs = {product_csv: products, customer_csv: customers}

        threads = []
        thread_queue = Queue()
        output = []

        for csv_path, collection in csvs.items():
            thread = threading.Thread(target=add_csv, args=(csv_path, collection, thread_queue))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        for x in range(2):
            result = thread_queue.get()
            output.append(result)

        return output


def add_csv(csv_path, collection_name, thread_queue):
    """ Adds csv data  """

    start = time.time()

    adds = 0
    errors = 0
    records = 0

    record_count_start = collection_name.count_documents({})

    try:
        logging.info(f"Importing {csv_path}")
        with open(csv_path) as csv_data:
            data = csv.DictReader(csv_data)
            for row in data:
                records += 1
                try:
                    collection_name.insert_one(row)
                    adds += 1
                except MongoClient.OperationFailure:
                    errors += 1
    except FileNotFoundError:
        logging.error(f"{csv_path} was not found")
        errors += 1

    record_count_end = collection_name.count_documents({})
    end = time.time()
    time_total = end - start

    thread_queue.put((records, record_count_start, record_count_end, time_total))


if __name__ == '__main__':
    start_time = time.time()
    print(import_data("sample_csv_files", "products.csv", "customers.csv"))
    end_time = time.time()
    total_time = end_time - start_time
    print("Run time:  {} seconds".format(total_time))
