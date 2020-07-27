"""parallel.py"""

import os
import csv
import time
import threading
import queue
from pymongo import MongoClient

class MongoDBConnection():
    """MongoDBConnection"""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None


    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_customers(directory_name, customer_file, queue):
    start_time = time.time()
    customer_count = 0
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.store
        customer = database["customer"]
        customer.drop()
        initial = database.customer.count_documents({})
        with open(os.path.join(directory_name, customer_file)) as csv_file:
            cust_reader = csv.reader(csv_file, delimiter=',')
            firstline = True
            for row in cust_reader:
                if firstline:
                    firstline = False
                    continue
                customer_count += 1
                customer_info = {'customer_id': row[0], 'name': row[1], 'address': row[2],
                                'phone': row[3], 'email': row[4]}
                customer.insert_one(customer_info)
        final = database.customer.count_documents({})
    end_time = time.time()
    queue.put((customer_count, initial, final, end_time-start_time))


def import_products(directory_name, customer_file, queue):
    start_time = time.time()
    product_count = 0
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.store
        product = database["products"]
        product.drop()
        initial = database.products.count_documents({})

        with open(os.path.join(directory_name, customer_file)) as csv_file:
            prod_read = csv.reader(csv_file, delimiter=',')
            firstline = True
            for row in prod_read:
                if firstline:
                    firstline = False
                    continue
                product_count += 1
                product_info = {'product_id': row[0], 'description': row[1], 'product_type': row[2],
                                'quantity': row[3]}
                product.insert_one(product_info)
        
        final = database.customer.count_documents({})
    end_time = time.time()
    queue.put((product_count, initial, final, end_time-start_time))


def import_rentals(directory_name, customer_file, queue):
    start_time = time.time()
    rental_count = 0
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.store
        rental = database["rentals"]
        rental.drop()

        initial = database.rentals.count_documents({})
        
        with open(os.path.join(directory_name, customer_file)) as csv_file:
            rent_read = csv.reader(csv_file, delimiter=',')
            firstline = True
            for row in rent_read:
                if firstline:
                    firstline = False
                    continue
                rental_count += 1
                info = {'customer_id': row[0], 'product_id': row[1]}
                rental.insert_one(info)
        
        final = database.customer.count_documents({})
    end_time = time.time()
    queue.put((rental_count, initial, final, end_time-start_time))


if __name__ == '__main__':
    total_start_time = time.time()
    queue = queue.Queue()
    thread1 = threading.Thread(target=import_customers, args=('csv_data', 'customers_long.csv', queue))
    thread1.start()
    thread2 = threading.Thread(target=import_products, args=('csv_data', 'products_long.csv', queue))
    thread2.start()
    thread3 = threading.Thread(target=import_rentals, args=('csv_data', 'rentals_long.csv', queue))
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
    first = queue.get()
    second = queue.get()
    third = queue.get()
    total_end_time = time.time()
    print(first)
    print(second)
    print(third)
    print("total time")
    print(total_end_time - total_start_time)



