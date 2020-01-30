"""Module for linear"""

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
    """"""
    
    p_start = time.time()
    added_records = 0
    
    mongo = MongoDBConnection()    
    with mongo:
        database = mongo.connection.store
        products = database["products"]
        initial_records = products.count_documents({})
        product_file_path = os.path.join(directory_name, product_file)
        
        with open(product_file_path, encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                p_info = {"product_id": row[0],
                          "description": row[1],
                          "product_type": row[2],
                          "quantity_available": row[3]}
                products.insert_one(p_info)
                added_records += 1
        final_records = products.count_documents({})
        mod_time = time.time() - p_start
        p_tup = (added_records, initial_records, final_records, mod_time)
        return p_tup


def import_customers_data(directory_name, customer_file):
    """"""
    
    c_start = time.time()
    added_records = 0
    
    mongo = MongoDBConnection()    
    with mongo:
        database = mongo.connection.store
        customers = database["customers"]
        initial_records = customers.count_documents({})
        customer_file_path = os.path.join(directory_name, customer_file)
        
        with open(customer_file_path, encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                c_info = {"rental_id": row[0],
                          "product_id": row[1],
                          "customer_id": row[2]}
                customers.insert_one(c_info)
                added_records += 1
        final_records = customers.count_documents({})
        mod_time = time.time() - c_start
        c_tup = (added_records, initial_records, final_records, mod_time)
        return c_tup


def import_rentals_data(directory_name, rental_file):
    """"""
    
    r_start = time.time()
    added_records = 0
    
    mongo = MongoDBConnection()    
    with mongo:
        database = mongo.connection.store
        rentals = database["rentals"]
        initial_records = rentals.count_documents({})
        rental_file_path = os.path.join(directory_name, rental_file)
        
        with open(rental_file_path, encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                r_info = {"customer_id": row[0],
                          "name": row[1],
                          "address": row[2],
                          "phone_number": row[3],
                          "email": row[4]}
                rentals.insert_one(r_info)
                added_records += 1
        final_records = rentals.count_documents({})
        mod_time = time.time() - r_start
        r_tup = (added_records, initial_records, final_records, mod_time)
        return r_tup


if __name__ == "__main__":
    start_time = time.time()
    products = import_products_data("csv_files", "products.csv")
    customers = import_customers_data("csv_files", "customers.csv")
    end_time = time.time()
    tot_time = end_time - start_time
    
    print("Products:")
    print(products)
    print("Customers:")
    print(customers)
    print("Total Time:", tot_time)