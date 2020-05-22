""" This module imports .csv files and creates a relational database using MongoDB"""
# pylint: disable=too-many-locals,pointless-statement
import os
import csv
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

def import_data(directory_name, product_file, customer_file, rental_file):
    """Brings in csv files, counts customers, products and rentals as well as errors"""
    customer_errors = 0
    product_errors = 0
    rental_errors = 0

    customer_count = 0
    product_count = 0
    rental_count = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media

        customer = database["customer"]
        product = database["product"]
        rental = database["rental"]

        customer.drop
        product.drop
        rental.drop

        try:
            with open(os.path.join(directory_name, customer_file)) as csvfile:
                customer_reader = csv.reader(csvfile, delimiter=',')
                for row in customer_reader:
                    customer_count += 1
                    customer_info = {"user_id": row[0], "name": row[1], "address": row[2],
                                     "phone_number": row[3], "email": row[4]}
                    customer.insert_one(customer_info)
        except FileNotFoundError:
            customer_errors += 1

        try:
            with open(os.path.join(directory_name, product_file)) as csvfile:
                product_reader = csv.reader(csvfile, delimiter=',')
                for row in product_reader:
                    product_count += 1
                    product_info = {"product_id": row[0], "description": row[1],
                                    "product_type": row[2], "quantity_available": row[3]}
                    product.insert_one(product_info)
        except FileNotFoundError:
            product_errors += 1

        try:
            with open(os.path.join(directory_name, rental_file)) as csvfile:
                rental_reader = csv.reader(csvfile, delimiter=',')
                for row in rental_reader:
                    rental_count += 1
                    rental_info = {"product_id": row[0], "user_id": row[1], "rental_date": row[2],
                                   "return_date": row[3]}
                    rental.insert_one(rental_info)
        except FileNotFoundError:
            rental_errors += 1

    return ((customer_count, product_count, rental_count),
            (customer_errors, product_errors, rental_errors))

def show_available_products():
    """ Uses database to return a dictionary of available products """
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        products = database['product']
        product_dict = {}
        for items in products.find():
            product_dict[items['product_id']] = {'description': items['description'],
                                                 'product_type': items['product_type'],
                                                 'quantity_available': items['quantity_available']}
    return product_dict

def show_rentals(product_id):
    """ Uses database to return information of customers that have rented a certain product"""
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.media
        rentals = database['rental']
        customer_dict = {}

        for row in rentals.find({'product_id': product_id}):
            result = database.customer.find_one({'user_id': row['user_id']})
            customer_dict[result['user_id']] = {'name': result['name'], 'address': result['address'],
                                               'phone_number': result['phone_number'],
                                               'email': result['email']}

    return customer_dict
