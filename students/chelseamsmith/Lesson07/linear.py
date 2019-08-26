# pylint: disable=W0104, W0702, R0914
"""creates a Mongo database out of csv files and has functions for working with db"""
import csv
import os
import time
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_products(directory_name, product_file):
    """imports data from csv files to populate product database"""

    prod_start = time.time()
    records_added = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        product = database["product"]
        initial_records = database.product.count_documents({})

        with open(os.path.join(directory_name, product_file)) as csvfile:
            product_reader = csv.reader(csvfile, delimiter=',')
            for row in product_reader:
                records_added += 1
                product_info = {"product_id": row[0], "description": row[1],
                                "product_type": row[2],
                                "quantity_available": row[3]}
                product.insert_one(product_info)

        final_records = database.product.count_documents({})

        return (records_added, initial_records, final_records, time.time() - prod_start)


def import_customers(directory_name, customer_file):
    """imports data from csv files to populate customer database"""

    cust_start = time.time()
    records_added = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        customer = database["customer"]
        initial_records = database.customer.count_documents({})

        with open(os.path.join(directory_name, customer_file)) as csvfile:
            customer_reader = csv.reader(csvfile, delimiter=',')
            for row in customer_reader:
                records_added += 1
                customer_info = {"customer_id": row[0], "name": row[1],
                                 "address": row[2], "phone_number": row[3],
                                 "email": row[4]}
                customer.insert_one(customer_info)

        final_records = database.customer.count_documents({})

        return (records_added, initial_records, final_records, time.time() - cust_start)


def import_rentals(directory_name, rentals_file):
    """imports data from csv files to populate rentals database"""

    rent_start = time.time()
    records_added = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        rentals = database["rentals"]
        initial_records = database.rentals.count_documents({})

        with open(os.path.join(directory_name, rentals_file)) as csvfile:
            rentals_reader = csv.reader(csvfile, delimiter=',')
            for row in rentals_reader:
                records_added += 1
                rental_info = {"product_id": row[0], "customer_id": row[1],
                               "rental_start_date": row[2],
                               "rental_end_date": row[3],
                               "cost_per_day": row[4]}
                rentals.insert_one(rental_info)

        final_records = database.rentals.count_documents({})

        return (records_added, initial_records, final_records, time.time() - rent_start)


if __name__ == '__main__':
    start_time = time.time()
    products = import_products('csvfiles', 'products.csv')
    customers = import_customers('csvfiles', 'customers.csv')
    rent = import_rentals('csvfiles', 'rentals.csv')
    end_time = time.time()

    print("Products")
    print(products)
    print("Customers")
    print(customers)
    print("Total Time")
    print(str(end_time-start_time))
