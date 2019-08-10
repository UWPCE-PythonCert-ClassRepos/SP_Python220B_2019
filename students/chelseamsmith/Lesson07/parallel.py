# pylint: disable=W0104, W0702, R0914
"""creates a Mongo database out of csv files and has functions for working with db"""
import csv
import os
import time
import threading
import queue
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


def import_products(directory_name, product_file, queue):
    """imports data from csv files to populate product database"""

    prod_start = time.time()
    products_added = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        product = database["product"]
        prod_initial_records = database.product.count_documents({})

        with open(os.path.join(directory_name, product_file)) as csvfile:
            product_reader = csv.reader(csvfile, delimiter=',')
            for row in product_reader:
                products_added += 1
                product_info = {"product_id": row[0], "description": row[1],
                                "product_type": row[2],
                                "quantity_available": row[3]}
                product.insert_one(product_info)

        prod_final_records = database.product.count_documents({})

    queue.put((products_added, prod_initial_records, prod_final_records, time.time() - prod_start))


def import_customers(directory_name, customer_file, queue):
    """imports data from csv files to populate customer database"""

    cust_start = time.time()
    customers_added = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        customer = database["customer"]
        cust_initial_records = database.customer.count_documents({})

        with open(os.path.join(directory_name, customer_file)) as csvfile:
            customer_reader = csv.reader(csvfile, delimiter=',')
            for row in customer_reader:
                customers_added += 1
                customer_info = {"customer_id": row[0], "name": row[1],
                                 "address": row[2], "phone_number": row[3],
                                 "email": row[4]}
                customer.insert_one(customer_info)

        cust_final_records = database.customer.count_documents({})

    queue.put((customers_added, cust_initial_records, cust_final_records, time.time() - cust_start))


def import_rentals(directory_name, rentals_file, queue):
    """imports data from csv files to populate rentals database"""

    rent_start = time.time()
    rentals_added = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store
        rentals = database["rentals"]
        rent_initial_records = database.rentals.count_documents({})

        with open(os.path.join(directory_name, rentals_file)) as csvfile:
            rentals_reader = csv.reader(csvfile, delimiter=',')
            for row in rentals_reader:
                rentals_added += 1
                rental_info = {"product_id": row[0], "customer_id": row[1],
                               "rental_start_date": row[2],
                               "rental_end_date": row[3],
                               "cost_per_day": row[4]}
                rentals.insert_one(rental_info)

        rent_final_records = database.rentals.count_documents({})

    queue.put((rentals_added, rent_initial_records, rent_final_records, time.time() - rent_start))


if __name__ == '__main__':
    start_time = time.time()
    my_queue = queue.Queue()
    thread1 = threading.Thread(target=import_products, args=("csvfiles", "products.csv", my_queue))
    thread1.start()
    prod_output = my_queue.get()
    thread2 = threading.Thread(target=import_customers, args=("csvfiles", "customers.csv", my_queue))
    thread2.start()
    cust_output = my_queue.get()
    thread3 = threading.Thread(target=import_rentals, args=("csvfiles", "rentals.csv", my_queue))
    thread3.start()
    rent_output = my_queue.get()
    end_time = time.time()


    print("Products")
    print(prod_output)
    print("Customers")
    print(cust_output)
    print("Total Time")
    print(str(end_time-start_time))
