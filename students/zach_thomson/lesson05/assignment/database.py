'''
Mongo DB assignment
'''
import csv
import os
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


def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    Function takes a directory name and three csv files as input (product data,
    customer data, rentals data) and creates a MongoDB database.
    Returns 2 tuples:
    1) Record count of number of products, customers and rentals added
    2) A count with any errors that occured in same order
    '''
    product_added = 0
    customer_added = 0
    rentals_added = 0

    product_errors = 0
    customer_errors = 0
    rental_errors = 0

    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        product = db['product']

        with open(os.path.join(directory_name, product_file)) as csvfile:
            product_reader = csv.DictReader(csvfile)
            for row in product_reader:
                product_added += 1
                new_product = {'product_id':row['product_id'],
                               'description':row['description'],
                               'product_type':row['product_type'],
                               'quantity_available':row['quantity_available']}
                product.insert_one(new_product)

        customer = db['customer']

        with open(os.path.join(directory_name, customer_file)) as csvfile:
            customer_reader = csv.DictReader(csvfile)
            for row in customer_reader:
                customer_added += 1
                new_customer = {'user_id':row['user_id'],
                                'name':row['name'],
                                'address':row['phone_number'],
                                'email':row['email']}
                customer.insert_one(new_customer)

        rentals = db['rentals']

        with open(os.path.join(directory_name, rentals_file)) as csvfile:
            rental_reader = csv.DictReader(csvfile)
            for row in rental_reader:
                rentals_added += 1
                new_rental = {'user_id':['user_id'],
                              'product_id':['product_id']}
                rentals.insert_one(new_rental)

    return [(product_added, customer_added, rentals_added),
            (product_errors, customer_errors, rental_errors)]






def show_available_products():
    '''returns a dict of products listed as available with fields:
    product_id, description, product_type, quantity available'''
    pass

def show_rentals(product_id):
    '''returns a dict with the info from users who rented matching product_id:
    user_id, name, address, phone_number, email'''
    pass
