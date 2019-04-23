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


        try:
            with open(os.path.join(directory_name, customer_file)) as customer_csv:
                csv_reader = csv.DictReader(customer_csv)

                customer_list = []

                for row in csv_reader:
                    try:
                        customer_list.append({'customer_id': row['Customer ID'],
                                              'first_name': row['First Name'],
                                              'last_name': row['Last Name'],
                                              'home_address': row['Home Address'],
                                              'email_address': row['Email Address'],
                                              'phone_number': row['Phone Number'],
                                              'status': row['Status'],
                                              'credit_limit': row['Credit Limit']})
                    except Exception as ex:
                        LOGGER.warning(ex)
                        LOGGER.warning('customer not added')
                        customer_error += 1
                try:
                    customers.insert_many(customer_list)
                except Exception as ex:
                    LOGGER.warning(ex)
        except Exception as ex:
            LOGGER.warning(ex)
            LOGGER.warning('error when opening customer file')

        try:
            with open(os.path.join(directory_name, product_file)) as product_csv:
                csv_reader = csv.DictReader(product_csv)

                product_list = []

                for row in csv_reader:
                    try:
                        product_list.append({'product_id': row['Product ID'],
                                             'description': row['Description'],
                                             'type': row['Type'],
                                             'total_quantity': row['Total Quantity']})
                    except Exception as ex:
                        LOGGER.warning(ex)
                        LOGGER.warning('product not added')
                        product_error += 1
                try:
                    products.insert_many(product_list)
                except Exception as ex:
                    LOGGER.warning(ex)
        except Exception as ex:
            LOGGER.warning(ex)
            LOGGER.warning('error when opening product file')

        try:
            with open(os.path.join(directory_name, rental_file)) as rental_csv:
                csv_reader = csv.DictReader(rental_csv)

                rental_list = []

                for row in csv_reader:
                    try:
                        rental_list.append({'rental_id': row['Rental ID'],
                                            'customer_id': row['Customer ID'],
                                            'product_id': row['Product ID'],
                                            'quantity': row['Quantity']})
                    except Exception as ex:
                        LOGGER.warning(ex)
                        LOGGER.warning('rental not added')
                        rental_error += 1
                try:
                    rentals.insert_many(rental_list)
                except Exception as ex:
                    LOGGER.warning(ex)
        except Exception as ex:
            LOGGER.warning(ex)
            LOGGER.warning('error when opening rental file')
        record_count = (len(product_list), len(customer_list), len(rental_list))
        error_count = (product_error, customer_error, rental_error)
        return(record_count, error_count)

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