#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 22:41:13 2019

@author: lauraannf
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 22:00:11 2019

@author: lauraannf
"""

import csv
import os
import logging
import time
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

def import_products(directory_name, product_file):
    """imports data from csv files and puts in database"""
    mongo = MongoDBConnection()
    product_error = 0
    
    with mongo:
        database = mongo.connection.HPNorton

        products = database["products"]
        product_list = []

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
    
        if product_error > 0:
            product_count = 0
        else:
            product_count = len(product_list)
        return(product_count, product_error)

def import_customers(directory_name, customer_file):
    """imports data from csv files and puts in database"""
    mongo = MongoDBConnection()
    customer_error = 0
    with mongo:
        database = mongo.connection.HPNorton

        customers = database["customers"]
        customer_list = []
        
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
        
        if customer_error > 0:
            customer_count = 0
        else:
            customer_count = len(customer_list)

        return(customer_count, customer_error)

def import_rentals(directory_name, rental_file):
    """imports data from csv files and puts in database"""
    mongo = MongoDBConnection()
    rental_error = 0

    with mongo:
        database = mongo.connection.HPNorton
        rentals = database["rentals"]
        rental_list = []
    
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

        if rental_error > 0:
            rental_count = 0
        else:
            rental_count = len(rental_list)
        return(rental_count, rental_error)


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



if __name__ == "__main__":
    MONGO_RESTART = MongoDBConnection()
    with MONGO_RESTART:
        DATABASE_RESTART = MONGO_RESTART.connection.HPNorton
        delete_database()
    START_ALL = time.clock()
    CUSTOMER_COUNT= import_customers('csvfiles', 'customers.csv')
    CUSTOMER_COUNT= import_products('csvfiles', 'inventory.csv')
    CUSTOMER_COUNT= import_rentals('csvfiles', 'rental.csv')
