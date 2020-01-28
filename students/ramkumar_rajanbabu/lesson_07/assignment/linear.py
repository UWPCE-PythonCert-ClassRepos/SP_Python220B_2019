"""Module for linear"""

import csv
import os
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class MongoDBConnection():
    """Connect to MongoDB (Code from part 5)"""
    LOGGER.info("Connecting to MongoDB")

    def __init__(self, host='127.0.0.1', port=27017):
        """Initialize"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Enter connection"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit connection"""
        self.connection.close()


def import_product():
    pass


def import_customer():
    pass


def import_rental():
    pass


def import_data(directory_name, product_file, customer_file, rental_file):
    """
    Create and populate a new MongoDB database with
    three csv files

    Args:
        product_file: csv file with product data
        customer_file: csv file with customer data
        rental_file: csv file with rental data

    Returns:
        total_count: record counts and fail counts
    """
    LOGGER.info("Creating add counts")
    product_count, customer_count, rental_count = 0, 0, 0

    LOGGER.info("Creating error counts")
    product_error, customer_error, rental_error = 0, 0, 0

    LOGGER.info("Creating file paths for files")
    product_file_path = os.path.join(directory_name, product_file)
    customer_file_path = os.path.join(directory_name, customer_file)
    rental_file_path = os.path.join(directory_name, rental_file)

    mongo = MongoDBConnection()

    with mongo:
        LOGGER.info("Creating mongo database")
        database = mongo.connection.media

        database.products.drop()
        database.customers.drop()
        database.rental.drop()
        LOGGER.info("Cleared all databases")

        LOGGER.info("Creating collections in database")
        products = database["products"]
        customers = database["customers"]
        rentals = database["rentals"]

        try:
            LOGGER.info("Converting product csv file to dictionary")
            with open(product_file_path, encoding="utf-8-sig") as csv_file:
                reader = csv.DictReader(csv_file)
                for item in reader:
                    csv_item = {"product_id": item["product_id"],
                                "description": item["description"],
                                "product_type": item["product_type"],
                                "quantity_available":
                                item["quantity_available"]}
                    products.insert_one(csv_item)
                    product_count += 1
                    LOGGER.info("Added product")
        except FileNotFoundError:
            LOGGER.info("File not found!")
            product_error += 1

        try:
            LOGGER.info("Converting customer csv file to dictionary")
            with open(customer_file_path, encoding="utf-8-sig") as csv_file:
                reader = csv.DictReader(csv_file)
                for item in reader:
                    csv_item = {"user_id": item["user_id"],
                                "name": item["name"],
                                "address": item["address"],
                                "phone_number": item["phone_number"],
                                "email": item["email"]}
                    customers.insert_one(csv_item)
                    customer_count += 1
                    LOGGER.info("Added customer")
        except FileNotFoundError:
            LOGGER.info("File not found!")
            customer_error += 1

        try:
            LOGGER.info("Converting rental csv file to dictionary")
            with open(rental_file_path, encoding="utf-8-sig") as csv_file:
                reader = csv.DictReader(csv_file)
                for item in reader:
                    csv_item = {"rental_id": item["rental_id"],
                                "product_id": item["product_id"],
                                "user_id": item["user_id"]}
                    rentals.insert_one(csv_item)
                    rental_count += 1
                    LOGGER.info("Added rental")
        except FileNotFoundError:
            LOGGER.info("File not found!")
            rental_error += 1

        LOGGER.info("Counting adds and errors")
        record_count = (product_count, customer_count, rental_count)
        fail_count = (product_error, customer_error, rental_error)
        total_count = record_count, fail_count
        return total_count


def show_available_products():
    """Return dictionary of products listed as product_id, description,
    product_type, quantity_available

    Returns:
        product_dict: dictionary of product information
    """
    mongo = MongoDBConnection()
    product_dict = dict()

    with mongo:
        LOGGER.info("Connecting to mongo database")
        database = mongo.connection.media

        LOGGER.info("Finding products")
        for product in database.products.find():
            product_info = {"description": product["description"],
                            "product_type": product["product_type"],
                            "quantity_available":
                            product["quantity_available"]}
            product_dict[product["product_id"]] = product_info
    return product_dict


def show_rentals(product_id):
    """Return dictionary with user information from users that have
    rented products matching product_id

    Args:
        product_id: product id number

    Returns:
        rental_dict: dictionary of rental information
    """
    mongo = MongoDBConnection()
    rental_dict = dict()

    with mongo:
        LOGGER.info("Connecting to mongo database")
        database = mongo.connection.media

        LOGGER.info("Finding rentals")
        rentals = database.rentals.find({"product_id":
                                         product_id}).sort("user_id")
        rental_list = [rental["user_id"] for rental in rentals]
        customers = database.customers.find({"user_id": {'$in': rental_list}})
        rental_dict = {person["user_id"]: {"name": person["name"],
                                           "address": person["address"],
                                           "phone_number":
                                           person["phone_number"],
                                           "email": person["email"]}
                       for person in customers}
    return rental_dict