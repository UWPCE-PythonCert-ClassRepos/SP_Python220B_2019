"""
Victor Medina
Assignment 5
"""
import csv
import os
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class MongoDBConnection(object):
    """
    Mongodb Connection
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        self.product = None
        self.customer = None
        self.rentals = None
        self.database = None

    def __enter__(self):
        """Connects to MongoDB"""
        self.connection = MongoClient(self.host, self.port)
        self.database = self.connection.rental_company
        self.product = self.database["product"]
        self.customer = self.database["customer"]
        self.rentals = self.database["rentals"]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rental_file):
    """

    :param directory_name:
    :param product_file:
    :param customer_file:
    :param rental_file:
    :return:
    """
    mongo = MongoDBConnection()
    customer_error = 0
    product_error = 0
    rental_error = 0

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
                                          'phone_number': row['Phone Number'],
                                          'email_address': row['Email Address']})
                try:
                    customers.insert_many(customer_list)
                except AttributeError as ex:
                    LOGGER.info(ex)
                    customer_error += 1

        except IOError as ex:
            LOGGER.info(ex)
            LOGGER.info('error when opening customer file')
            customer_error += 1

        if customer_error > 0:
            customer_count = 0
        else:
            customer_count = len(customer_list)

        rentals = database["rentals"]
        rental_list = []

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
                except AttributeError as ex:
                    LOGGER.info(ex)
                    product_error += 1
        except IOError as ex:
            LOGGER.info(ex)
            LOGGER.info('error when opening product file')
            product_error += 1
        if product_error > 0:
            product_count = 0
        else:
            product_count = len(product_list)
        products = database["products"]
        product_list = []
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
                except AttributeError as ex:
                    LOGGER.info(ex)
                    rental_error += 1
        except IOError as ex:
            LOGGER.info(ex)
            LOGGER.info('error when opening rental file')
            rental_error += 1

        if rental_error > 0:
            rental_count = 0
        else:
            rental_count = len(rental_list)

        record_count = (product_count, customer_count, rental_count)
        error_count = (product_error, customer_error, rental_error)
        return record_count, error_count


def show_available_products():
    """
    :return:
    """

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


def delete_database():
    """

    :return:
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        database.product.drop()
        database.customer.drop()
        database.rentals.drop()
    LOGGER.debug("Cleared database")
