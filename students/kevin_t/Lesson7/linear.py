""" This module imports .csv files and creates a relational database using MongoDB"""
import os
import csv
import time
from pymongo import MongoClient

class MongoDBConnection():
    """MongoDB Connection"""

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

def import_customers(directory_name, customer_file):
    """Brings in csv files, counts customers, products and rentals as well as errors"""
    local_start_time = time.time()
    customer_count = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        customer = database["customer"]
        customer.drop()

        initial_count = database.customer.count_documents({})

        with open(os.path.join(directory_name, customer_file)) as csvfile:
            customer_reader = csv.reader(csvfile, delimiter=',')
            for row in customer_reader:
                customer_count += 1
                customer_info = {"user_id": row[0], "name": row[1], "address": row[2],
                                 "phone_number": row[3], "email": row[4]}
                customer.insert_one(customer_info)

        final_count = database.customer.count_documents({})

    local_end_time = time.time()

    return (customer_count, initial_count, final_count, local_end_time - local_start_time)

def import_products(directory_name, customer_file):
    """Brings in csv files, counts customers, products and rentals as well as errors"""
    local_start_time = time.time()
    products_count = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        products = database["products"]
        products.drop()

        initial_count = database.products.count_documents({})

        with open(os.path.join(directory_name, customer_file)) as csvfile:
            products_reader = csv.reader(csvfile, delimiter=',')
            for row in products_reader:
                products_count += 1
                products_info = {"product_id": row[0], "description": row[1],
                                 "product_type": row[2], "quantity_available": row[3]}
                products.insert_one(products_info)

        final_count = database.customer.count_documents({})

    local_end_time = time.time()

    return (products_count, initial_count, final_count, local_end_time - local_start_time)

def import_rentals(directory_name, customer_file):
    """Brings in csv files, counts customers, rentals and rentals as well as errors"""
    local_start_time = time.time()
    rentals_count = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        rentals = database["rentals"]
        rentals.drop()

        initial_count = database.rentals.count_documents({})

        with open(os.path.join(directory_name, customer_file)) as csvfile:
            rentals_reader = csv.reader(csvfile, delimiter=',')
            for row in rentals_reader:
                rentals_count += 1
                rentals_info = {"product_id": row[0], "user_id": row[1], "rental_date": row[2],
                                "return_date": row[3]}
                rentals.insert_one(rentals_info)

        final_count = database.customer.count_documents({})

    local_end_time = time.time()

    return (rentals_count, initial_count, final_count, local_end_time - local_start_time)

if __name__ == '__main__':
    TOTAL_START_TIME = time.time()
    CUSTOMERS = import_customers('input_files', 'customers_l7.csv')
    PRODUCTS = import_products('input_files', 'products_l7.csv')
    RENTALS = import_rentals('input_files', 'rentals_l7.csv')
    TOTAL_END_TIME = time.time()

    print("Customers")
    print(CUSTOMERS)
    print("Products")
    print(PRODUCTS)
    print("Rentals")
    print(RENTALS)
    print("Total time")
    print(TOTAL_END_TIME - TOTAL_START_TIME)
    