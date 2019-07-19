"""
Victor A Medina
Assignment 5
"""

import logging
import csv
import os
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class MongoDBConnection():
    """
    MongoDB connection
    """
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """

    :param directory_name:
    :param product_file:
    :param customer_file:
    :param rentals_file:
    :return:
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hpnorton

        product_file = os.path.join(directory_name, product_file)
        customer_file = os.path.join(directory_name, customer_file)
        rentals_file = os.path.join(directory_name, rentals_file)

        LOGGER.debug("Importing %s", product_file)
        products = database["products"]
        with open(product_file) as product:
            products_csv = csv.DictReader(product)
            for row in products_csv:
                print(row)
                products.insert_one(row)

        LOGGER.debug("Importing %s", customer_file)
        customers = database["customers"]
        with open(customer_file) as product:
            products_csv = csv.DictReader(product)
            for row in products_csv:
                print(row)
                customers.insert_one(row)

        LOGGER.debug("Importing %s", rentals_file)
        rentals = database["rentals"]
        with open(rentals_file) as product:
            products_csv = csv.DictReader(product)
            for row in products_csv:
                print(row)
                rentals.insert_one(row)

    with mongo:
        db = mongo.connection.hpnorton
        print("Printing the collection of DB")
        print(db.list_collection_names())


def show_available_products():
    """Display the products in inventory"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        available_products = {}
        for entry in database.product.find():
            for key, value in entry.items():
                if key != '_id':
                    if value['quantity_available'] != '0':
                        available_products[key] = value
        return available_products


def show_rentals(product_id):
    """Display the users who rented a product"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        renters_dict = {}
        for entry in database.rentals.find():
            for key, value in entry.items():
                if key != '_id':
                    if product_id in value['rentals']:
                        for customer in database.customer.find():
                            renters_dict[key] = customer[key]
                    else:
                        LOGGER.debug("No matches found")

        LOGGER.debug('The returned rentals matched are: %s', renters_dict)
        return renters_dict


if __name__ == '__main__':
    directory_Name = "D:/Users/Victor/Desktop/python_pwe/SP_Python220B_2019" \
                     "/students/vmedina/lesson_05/data"
    import_data(directory_Name, "customers.csv", "products.csv", "rentals.csv")
