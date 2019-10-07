"""
Work with the MongoDB database with python and implement the multithreading
and Queuing techniques to improve the performance.
"""

import csv
import os
import time
from threading import Thread
from queue import Queue
from pymongo import MongoClient


#pylint: disable = W0702, R0914

class MongoDatabase:
    """This class sets up the MongoDB database connection."""
    def __init__(self, host='127.0.0.1', port=27017):
        """constructor
        :parm host: local MongoDB host
        :parm port: local MongoDB port
        """
        self.host = host
        self.port = port
        self.connection = None


    def __enter__(self):
        """
        This megic method is called in the background when a context manager
        is created.
        :return: self
        """
        self.connection = MongoClient(self.host, self.port)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
         Close the database connection on exit.
        :parm exc_type:
        :parm exc_val:
        :parm:exc_tb
        """
        self.connection.close()


def import_customers_data(folder, filename, queue):
    """creates a customers table in the database.
    :parm dir: directory name
    :parm filename: data file
    :return tuple:
    """
    start_time = time.time()
    records = 0
    mongo = MongoDatabase()

    with mongo:
        database = mongo.connection["Store2"]
        customer_table = database["Customer"]
        with open(os.path.join(folder, filename), 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            initial_records = customer_table.count()
            for row in reader:
                customer = {'customer_id':row[0], 'name':row[1],
                            'address':row[2], 'phone_number':row[3],
                            'email':row[4]}
                records += 1
                customer_table.insert_one(customer)
        final_records = customer_table.count()
    queue.put((records, initial_records, final_records, time.time()-start_time))


def import_products_data(folder, filename, queue):
    """creates a products table in the database.
    :parm dir: directory name
    :parm filename: data file
    :return tuple:
    """
    start_time = time.time()
    records = 0

    mongo = MongoDatabase()

    with mongo:
        database = mongo.connection["Store2"]
        product_table = database["Product"]
        with open(os.path.join(folder, filename), 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            initial_records = product_table.count()
            for row in reader:
                product = {'product_id':row[0], 'description':row[1],
                           'category':row[2], 'quantity':row[3]}
                records += 1
                product_table.insert_one(product)
            final_records = product_table.count()
    queue.put((records, initial_records, final_records, time.time()-start_time))


def import_rentals_data(folder, filename, queue):
    """creates a rentals table in the database.
    :parm dir: directory name
    :parm filename: data file
    :return tuple:
    """
    start_time = time.time()
    records = 0
    mongo = MongoDatabase()

    with mongo:
        database = mongo.connection["Store2"]
        rental_table = database["Rental"]
        with open(os.path.join(folder, filename), 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            initial_records = rental_table.count()
            for row in reader:
                rental = {'product_id':row[0], 'customer_id':row[1],
                          'category':row[2], 'rental_start_date':row[3],
                          'rental_end_date':row[3], 'cost_per_day':row[4]}
                records += 1
                rental_table.insert_one(rental)
            final_records = rental_table.count()
    queue.put((records, initial_records, final_records, time.time()-start_time))


if __name__ == "__main__":
    print('Parallel Result')
    START = time.time()
    QUEUE = Queue()   # FIFO queue by default.
    THREAD_1 = Thread(target=import_customers_data,
                      args=('data', 'customers.csv', QUEUE))
    THREAD_1.start()
    THREAD_2 = Thread(target=import_products_data,
                      args=('data', 'products.csv', QUEUE))
    THREAD_2.start()
    THREAD_3 = Thread(target=import_rentals_data,
                      args=('data', 'rentals.csv', QUEUE))
    THREAD_3.start()

    THREAD_1.join()
    THREAD_2.join()
    THREAD_3.join()

    CUSTOMERS = QUEUE.get()
    PRODUCTS = QUEUE.get()
    RENTALS = QUEUE.get()

    END = time.time()

    print('Customers')
    print(CUSTOMERS)
    print('Products')
    print(PRODUCTS)
    print('Rentals')
    print(RENTALS)
    print('Total time elapsed {} seconds'.format(END-START))
