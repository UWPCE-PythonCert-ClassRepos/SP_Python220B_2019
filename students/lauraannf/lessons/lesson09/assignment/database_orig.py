""" Creates the HP Norton Database"""
import csv
import os
import logging
from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setFormatter(FORMATTER)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class MongoDBConnection(object):
    "MongoDB Connection"""
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
    """imports data from csv files and puts in database"""
    mongo = MongoDBConnection()
    customer_error = 0
    product_error = 0
    rental_error = 0

    with mongo:
        database = mongo.connection.HPNorton

        customers = database["customers"]
        rentals = database["rentals"]
        products = database["products"]
        customer_list = []
        rental_list = []
        product_list = []

        try:
            with open(os.path.join(directory_name, customer_file)) as customer_csv:
                csv_reader = csv.DictReader(customer_csv)
                for row in csv_reader:
                    customer_list.append({'customer_id': row['Customer ID'],
                                          'first_name': row['First Name'],
                                          'last_name': row['Last Name'],
                                          'home_address': row['Home Address'],
                                          'email_address': row['Email Address'],
                                          'phone_number': row['Phone Number'],
                                          'status': row['Status'],
                                          'credit_limit': row['Credit Limit']})
                try:
                    customers.insert_many(customer_list)
                except Exception as ex:
                    LOGGER.warning(ex)
                    customer_error += 1
        except Exception as ex:
            LOGGER.warning(ex)
            LOGGER.warning('error when opening customer file')
            customer_error += 1
        try:
            with open(os.path.join(directory_name, product_file)) as product_csv:
                csv_reader = csv.DictReader(product_csv)

                for row in csv_reader:
                    product_list.append({'product_id': row['Product ID'],
                                         'description': row['Description'],
                                         'type': row['Type'],
                                         'total_quantity': row['Total Quantity']})
                try:
                    products.insert_many(product_list)
                except Exception as ex:
                    LOGGER.warning(ex)
                    product_error += 1
        except Exception as ex:
            LOGGER.warning(ex)
            LOGGER.warning('error when opening product file')
            product_error += 1
        try:
            with open(os.path.join(directory_name, rental_file)) as rental_csv:
                csv_reader = csv.DictReader(rental_csv)


                for row in csv_reader:
                    rental_list.append({'rental_id': row['Rental ID'],
                                        'customer_id': row['Customer ID'],
                                        'product_id': row['Product ID'],
                                        'quantity': row['Quantity']})
                try:
                    rentals.insert_many(rental_list)
                except Exception as ex:
                    LOGGER.warning(ex)
                    rental_error += 1
        except Exception as ex:
            LOGGER.warning(ex)
            LOGGER.warning('error when opening rental file')
            rental_error += 1

        if product_error > 0:
            product_count = 0
        else:
            product_count = len(product_list)
        if rental_error > 0:
            rental_count = 0
        else:
            rental_count = len(rental_list)
        if customer_error > 0:
            customer_count = 0
        else:
            customer_count = len(customer_list)

        record_count = (product_count, customer_count, rental_count)
        error_count = (product_error, customer_error, rental_error)
        return(record_count, error_count)

def show_available_products():
    """ lists all available products"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.HPNorton
        product_dict = {}
        for product in database.products.find():
            total_count = int(product['total_quantity']) - total_rented(product['product_id'])
            product_dict[product['product_id']] = {
                'description': product['description'],
                'product_type': product['type'],
                'total_quantity': product['total_quantity'],
                'available_quantity': total_count}
    return product_dict

def show_rentals(product_id):
    """lists all rentals"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.HPNorton
        rental_dict = {}
        for rental in database.rentals.find({'product_id': product_id}):
            for customer in database.customers.find({'customer_id': rental['customer_id']}):
                rental_dict[rental['rental_id']] = {
                    'customer_id': rental['customer_id'],
                    'customer_name': customer['first_name'] + ' ' + customer['last_name'],
                    'customer_address': customer['home_address'],
                    'phone_number': customer['phone_number'],
                    'email': customer['email_address'],
                    'quantity': rental['quantity']}
        return rental_dict

def total_rented(product_id):
    "returns total number rented for product_id"
    rental_dict = show_rentals(product_id)
    total = 0
    for key in rental_dict:
        total += int(rental_dict[key]['quantity'])
    return  total

def delete_database():
    """deletes database to start fresh"""
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.HPNorton

        customers = database["customers"]
        rentals = database["rentals"]
        products = database["products"]

        customers.drop()
        rentals.drop()
        products.drop()
