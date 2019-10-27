""" Module to initialize and access MongoDB from CSV files """

import csv
import logging
from pymongo import MongoClient

# Disabling invalid-name due to 'db' varaible name
# pylint: disable=logging-fstring-interpolation, invalid-name, too-many-locals

logging.basicConfig(level=logging.INFO)

class MongoDBConnection():
    """ MongoDB Connection """

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file):
    """ Creates and populates a new MongoDB database from csv files """

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpn

        logging.info("Creating MongoDB Collections...")
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        logging.info("Dropping existing Collections...")
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()

        add_list = []
        error_list = []

        for file_path, collection_name in [(f"{directory_name}/{product_file}", products),
                                           (f"{directory_name}/{customer_file}", customers),
                                           (f"{directory_name}/{rentals_file}", rentals)]:

            # Initialize the counter variables
            add_count = 0
            error_count = 0

            # Process each file and count adds and errors
            try:
                logging.info(f"Importing {file_path}")
                with open(file_path) as csv_file:
                    csv_data = csv.DictReader(csv_file)
                    for row in csv_data:
                        try:
                            collection_name.insert_one(row)
                            add_count += 1
                        except MongoClient.OperationFailure:
                            error_count += 1
            except FileNotFoundError:
                logging.error(f"{file_path} does not exist")
                error_count += 1

            # Update the return lists
            add_list.append(add_count)
            error_list.append(error_count)

        # Return tuples
        return tuple(add_list), tuple(error_list)

def show_available_products():
    """ Returns a Python dictionary of products listed as available """

    # Initialize return dictionary
    available_products = {}

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpn

        logging.info("Finding available products...")
        for product in db.products.find({"quantity_available": {"$gt": "0"}}):
            available_products[product["product_id"]] = {
                'description': product["description"],
                'product_type': product["product_type"],
                'quantity_available': product["quantity_available"]}

    return available_products

def show_rentals(product_id):
    """ Returns a Python dictionary of users that have rented products matching product_id """

    # Initialize return dictionary
    users_who_rented = {}

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpn

        logging.info(f"Finding rentals for {product_id}...")
        for rental in db.rentals.find({"product_id": product_id}):
            user_to_find = rental["user_id"]
            logging.info(f"Finding user details for {user_to_find}")
            for user in db.customers.find({"user_id": user_to_find}):
                users_who_rented[user_to_find] = {'name': user["name"],
                                                  'address': user["address"],
                                                  'phone_number': user["phone_number"],
                                                  'email': user["email"]}

    return users_who_rented
