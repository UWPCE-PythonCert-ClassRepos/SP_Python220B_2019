"""Module for parallel"""

import csv
import os
import time
from threading import Thread
from queue import Queue
from pymongo import MongoClient


class MongoDBConnection():
    """Connect to MongoDB (Code from part 5)"""

    def __init__(self, host='127.0.0.1', port=27017):
        """Initialize"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Enter connection"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit connection"""
        self.connection.close()


def import_products_data(directory_name, product_file, queue):
    """Import data to products database"""
    p_start = time.time()
    p_added = 0

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
        products = database["products"]
        product_file_path = os.path.join(directory_name, product_file)

        p_initial = products.count()
        with open(product_file_path, encoding="utf-8-sig") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                p_info = {"product_id": row[0],
                          "description": row[1],
                          "product_type": row[2],
                          "quantity_available": row[3]}
                products.insert_one(p_info)
                p_added += 1
        p_final = products.count()
        mod_time = time.time() - p_start
    queue.put((p_added, p_initial, p_final, mod_time))


def import_customers_data(directory_name, customer_file, queue):
    """Import data to customers database"""
    c_start = time.time()
    c_added = 0

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
        customers = database["customers"]
        customer_file_path = os.path.join(directory_name, customer_file)

        c_initial = customers.count()
        with open(customer_file_path, encoding="utf-8-sig") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                c_info = {"customer_id": row[0],
                          "name": row[1],
                          "address": row[2],
                          "phone_number": row[3],
                          "email": row[4]}
                customers.insert_one(c_info)
                c_added += 1
        c_final = customers.count()
        mod_time = time.time() - c_start
    queue.put((c_added, c_initial, c_final, mod_time))


def import_rentals_data(directory_name, rental_file, queue):
    """Import data to rentals database"""
    r_start = time.time()
    r_added = 0

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media
        rentals = database["rentals"]
        rental_file_path = os.path.join(directory_name, rental_file)

        r_initial = rentals.count()
        with open(rental_file_path, encoding="utf-8-sig") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                r_info = {"rental_id": row[0],
                          "product_id": row[1],
                          "customer_id": row[2]}
                rentals.insert_one(r_info)
                r_added += 1
        r_final = rentals.count()
        mod_time = time.time() - r_start
    queue.put((r_added, r_initial, r_final, mod_time))


if __name__ == "__main__":
    print("Parallel Results:")
    START_TIME = time.time()
    MY_QUEUE = Queue()
    THREAD_1 = Thread(target=import_products_data,
                      args=("sample_csv_files", "products.csv", MY_QUEUE))
    THREAD_1.start()
    THREAD_2 = Thread(target=import_customers_data,
                      args=("sample_csv_files", "customers.csv", MY_QUEUE))
    THREAD_2.start()
    THREAD_1.join()
    THREAD_2.join()
    PRODUCTS = MY_QUEUE.get()
    CUSTOMERS = MY_QUEUE.get()
    END_TIME = time.time()
    TOT_TIME = END_TIME - START_TIME

    print("Products:")
    print(PRODUCTS)
    print("Customers:")
    print(CUSTOMERS)
    print("Total Time:", TOT_TIME)
