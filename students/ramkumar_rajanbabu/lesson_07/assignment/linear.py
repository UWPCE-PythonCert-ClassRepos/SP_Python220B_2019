"""Module for linear"""

# pylint: disable=too-many-locals

import csv
import os
import time
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


def import_products_data(directory_name, product_file):
    """Import data to products database"""
    p_start = time.time()
    p_added = 0

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.store
        products = database["products"]
        p_initial = products.count_documents({})
        product_file_path = os.path.join(directory_name, product_file)

        with open(product_file_path, encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                p_info = {"product_id": row[0],
                          "description": row[1],
                          "product_type": row[2],
                          "quantity_available": row[3]}
                products.insert_one(p_info)
                p_added += 1
        p_final = products.count_documents({})
        mod_time = time.time() - p_start
        p_tup = (p_added, p_initial, p_final, mod_time)
    return p_tup


def import_customers_data(directory_name, customer_file):
    """Import data to customers database"""
    c_start = time.time()
    c_added = 0

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.store
        customers = database["customers"]
        c_initial = customers.count_documents({})
        customer_file_path = os.path.join(directory_name, customer_file)

        with open(customer_file_path, encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                c_info = {"customer_id": row[0],
                          "name": row[1],
                          "address": row[2],
                          "phone_number": row[3],
                          "email": row[4]}
                customers.insert_one(c_info)
                c_added += 1
        c_final = customers.count_documents({})
        mod_time = time.time() - c_start
        c_tup = (c_added, c_initial, c_final, mod_time)
    return c_tup


def import_rentals_data(directory_name, rental_file):
    """Import data to rentals database"""
    r_start = time.time()
    r_added = 0

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.store
        rentals = database["rentals"]
        r_initial = rentals.count_documents({})
        rental_file_path = os.path.join(directory_name, rental_file)

        with open(rental_file_path, encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                r_info = {"rental_id": row[0],
                          "product_id": row[1],
                          "customer_id": row[2]}
                rentals.insert_one(r_info)
                r_added += 1
        r_final = rentals.count_documents({})
        mod_time = time.time() - r_start
        r_tup = (r_added, r_initial, r_final, mod_time)
    return r_tup


if __name__ == "__main__":
    START_TIME = time.time()
    PRODUCTS = import_products_data("sample_csv_files", "products.csv")
    CUSTOMERS = import_customers_data("sample_csv_files", "customers.csv")
    END_TIME = time.time()
    TOT_TIME = END_TIME - START_TIME

    print("Products:")
    print(PRODUCTS)
    print("Customers:")
    print(CUSTOMERS)
    print("Total Time:", TOT_TIME)
