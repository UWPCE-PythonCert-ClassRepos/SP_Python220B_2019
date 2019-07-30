"""
Victor Medina
Assignment 7
Linear Version
"""

import csv
import os
import logging
import time
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class MongoDBConnection(object):
    """

    """

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_customers(directory_name, customer_file):
    """
    :param directory_name:
    :param customer_file:
    :return:
    """

    start_c = time.clock()
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.HPNorton
        customer_count_orig = database.customers.count_documents({})

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
                    customers.insert_many(customer_list)

        except IOError as ex:
            LOGGER.warning(ex)
            LOGGER.warning("Can't open customer file")
        customer_count_new = database.customers.count_documents({})

        return (customer_count_new - customer_count_orig, customer_count_orig,
                customer_count_new, time.clock() - start_c)


def import_rentals(directory_name, rental_file):
    """
    :param directory_name:
    :param rental_file:
    :return:
    """
    start_r = time.clock()
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.HPNorton
        rental_count_orig = database.rentals.count_documents({})
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
                    rentals.insert_many(rental_list)

        except IOError as ex:
            LOGGER.warning(ex)
            LOGGER.warning('error when opening rental file')
        rental_count_new = database.rentals.count_documents({})

        return (rental_count_new - rental_count_orig, rental_count_orig,
                rental_count_new, time.clock() - start_r)


def import_products(directory_name, product_file):
    """
    :param directory_name:
    :param product_file:
    :return:
    """

    start_p = time.clock()
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.HPNorton
        product_count_orig = database.products.count_documents({})
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
                    products.insert_many(product_list)

        except IOError as ex:
            LOGGER.warning(ex)
            LOGGER.warning('Cant open product file')

        product_count_new = database.products.count_documents({})

        return (product_count_new - product_count_orig, product_count_orig,
                product_count_new, time.clock() - start_p)


def delete_db():
    """
    :return:
    """
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
    START = time.clock()
    CUSTOMER_COUNT = import_customers('csvfiles', 'customers.csv')
    PRODUCT_COUNT = import_products('csvfiles', 'inventory.csv')
    RENTAL_COUNT = import_rentals('csvfiles', 'rentals.csv')
    END = time.clock() - START
    print(PRODUCT_COUNT, CUSTOMER_COUNT)
    print('Total Time for linear = {}s'.format(END))
