""" Module to initialize and access MongoDB from CSV files """

import csv
import logging
import threading
import time
from queue import Queue
from pymongo import MongoClient

# Disabling invalid-name due to 'db' varaible name
# pylint: disable=logging-fstring-interpolation, invalid-name, too-many-locals

logging.basicConfig(level=logging.INFO)

class MongoDBConnection():
    """ MongoDB Connection """

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file):
    """ Creates and populates a new MongoDB database from csv files """

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpn

        logging.info("Creating MongoDB Collections...")
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        logging.info("Dropping existing Collections...")
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()

        #add_list = []
        #error_list = []

        threads = []
        thread_queue = Queue()
        output = []

        for file_path, collection_name in [(f"{directory_name}/{product_file}", customers),
                                           (f"{directory_name}/{customer_file}", products),
                                           (f"{directory_name}/{rentals_file}", rentals)]:
            thread = threading.Thread(target=process_csv, args=(file_path,
                                                                collection_name,
                                                                thread_queue))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        # Queue is FIFO, so only return the customers and products data
        for _ in range(2):
            result = thread_queue.get()
            output.append(result)

        return output

def process_csv(file_path, collection_name, thread_queue):
    """ Import a given CSV file to a Collection """

    # Note the start time - lesson 7
    csv_start_time = time.time()

    # Initialize the counter variables - lesson 5/7
    add_count = 0
    error_count = 0
    record_count = 0

    # Get the DB record count - lesson 7
    db_record_count_start = collection_name.count_documents({})

    # Process each file and count adds and errors
    try:
        logging.info(f"Importing {file_path}")
        with open(file_path) as csv_file:
            csv_data = csv.DictReader(csv_file)
            for row in csv_data:
                record_count += 1
                try:
                    collection_name.insert_one(row)
                    add_count += 1
                except MongoClient.OperationFailure:
                    error_count += 1
    except FileNotFoundError:
        logging.error(f"{file_path} does not exist")
        error_count += 1

    # Get the DB record count - lesson 7
    db_record_count_end = collection_name.count_documents({})

    # Update the return lists - lesson 5
    #add_list.append(add_count)
    #error_list.append(error_count)

    # Note the end time - lesson 7
    csv_end_time = time.time()
    csv_total_time = csv_end_time - csv_start_time

    # Return counts
    #return (record_count, db_record_count_start, db_record_count_end, csv_total_time)
    thread_queue.put((record_count, db_record_count_start, db_record_count_end, csv_total_time))

if __name__ == '__main__':
    start_time = time.time()
    print(import_data("csv_files", "products.csv", "customers.csv", "rentals.csv"))
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total Run Time:  {total_time} seconds")
