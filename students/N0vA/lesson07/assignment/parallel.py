"""
Module to load test data in parallel.
"""


# pylint:disable=too-many-locals
# pylint:disable=invalid-name

import csv
import os
import time
import threading
from pymongo import MongoClient

class MongoDBConnection():
    """Setup for MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """Initialize MongoDB Database"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def read_data(csv_file):
    """Reads csv file and creates list of dictionaries."""

    new_data = []

    with open(csv_file) as input_file:
        reader = csv.reader(input_file)
        header = next(reader)

        for row in reader:
            temp = dict(zip(header[:], row[:]))
            new_data.append(temp)

    return new_data

def add_table(csv_data, table):
    """Add file to database.
    I added this function to help make the code for
    parrel processing cleaner and like the example
    from the Threading and Multiprocessing Part 4 reading."""

    try:
        table.insert_many(csv_data)
    except FileNotFoundError as e:
        print(e)

def import_data_parallel(directory_name, product_file, customer_file, rental_file):
    """Reads in data from a given directory and set of 3 input files for products,
    customers, and rentals in that order."""
    start_time = time.time()

    print('\nImporting data...\n\n')
    # Prep input data - filepaths
    product_path = os.path.join(directory_name, product_file)
    customer_path = os.path.join(directory_name, customer_file)
    rental_path = os.path.join(directory_name, rental_file)

    client = MongoDBConnection()

    with client:
        db = client.connection.hp_norton

        # Create and open tables for database
        products = db['products']
        customers = db['customers']
        rentals = db['rentals']

        # Prep for output
        customers_before = customers.count_documents({})
        products_before = products.count_documents({})

        # Set up input for loading data
        product_data = read_data(product_path)
        customer_data = read_data(customer_path)
        rental_data = read_data(rental_path)

        # Set up threads and load data
        products_thread = threading.Thread(target=add_table,
                                           args=(product_data, products))
        customer_thread = threading.Thread(target=add_table,
                                           args=(customer_data, customers))
        rentals_thread = threading.Thread(target=add_table,
                                          args=(rental_data, rentals))

        # Start threads
        customer_thread.start()
        products_thread.start()
        rentals_thread.start()

        customer_thread.join()
        customer_thread.join()
        rentals_thread.join()

        # Record records added
        customers_added = len(customer_data)
        products_added = len(product_data)
        print(customers_added, 'customers added to the database.\n\n')
        print(products_added, 'products added to the database.\n\n')

        # State of database after reading data
        customers_after = customers_before + customers_added
        products_after = products_before + products_added
        parallel_run_time = time.time() - start_time

    print('Data upload complete.\n\n')
    print('The run time for parallel importation method was', parallel_run_time, '\n')

    # Outputs
    customers_tuple = (customers_added, customers_before, customers_after, parallel_run_time)
    products_tuple = (products_added, products_before, products_after, parallel_run_time)
    return customers_tuple, products_tuple

def show_available_products():
    """Returns a python dictionary of product availability."""

    # Connect to database
    client = MongoDBConnection()
    with client:
        db = client.connection.hp_norton
        query = db['products']

        # Dictionary output
        available_products = {}

        # Iterate through products for dictionary
        for product in query.find():
            available_products[product['product_id']] = {
                'description': product['description'],
                'product_type': product['product_type'],
                'quantity_available': product['quantity_available']}

        return available_products

def show_rentals():
    """Returns a python dictionary for users that have rented products."""

    # Dictionary output
    rentals_available = {}

    # Connect to database
    client = MongoDBConnection()
    with client:
        db = client.connection.hp_norton

        rentals = db['rentals']
        customers = db['customers']
        renters = []

        # Get list of customer ids who have rented products
        for rental in rentals.find():
            renters.append(rental['user_id'])

        # Get customer information for each person in renters list
        for renter in renters:
            for per in customers.find({'user_id': renter}):
                rentals_available[per['user_id']] = {'name': per['name'],
                                                     'address': per['address'],
                                                     'phone_number': per['phone_number'],
                                                     'email': per['email']}
        return rentals_available

def clear_database():
    """Clear database of existing data."""

    client = MongoDBConnection()
    with client:
        db = client.connection.hp_norton

        # Drop tables
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()

    print('Database all cleared.')
