# pylint: disable=W0104, W0702, R0914
"""creates a Mongo database out of csv files and has functions for working with db"""
import csv
import os
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

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
    """imports data from csv files to populate a mongoDB database"""

    #error counts
    product_errors = 0
    customer_errors = 0
    rentals_errors = 0

    #row counts
    products = 0
    customers = 0
    rental_units = 0

    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.store

        #create collections for product file, customer file, and rental file
        product = database["product"]
        customer = database["customer"]
        rentals = database["rentals"]

        #make sure databases are empty to start with
        product.drop
        customer.drop
        rentals.drop

        try:
            with open(os.path.join(directory_name, product_file)) as csvfile:
                product_reader = csv.reader(csvfile, delimiter=',')
                for row in product_reader:
                    products += 1
                    product_info = {"product_id": row[0], "description": row[1],
                                    "product_type": row[2],
                                    "quantity_available": row[3]}
                    product.insert_one(product_info)
        except:
            product_errors += 1

        try:
            with open(os.path.join(directory_name, customer_file)) as csvfile:
                customer_reader = csv.reader(csvfile, delimiter=',')
                for row in customer_reader:
                    customers += 1
                    customer_info = {"customer_id": row[0], "name": row[1],
                                     "address": row[2], "phone_number": row[3],
                                     "email": row[4]}
                    customer.insert_one(customer_info)
        except:
            customer_errors += 1

        try:
            with open(os.path.join(directory_name, rentals_file)) as csvfile:
                rentals_reader = csv.reader(csvfile, delimiter=',')
                for row in rentals_reader:
                    rental_units += 1
                    rental_info = {"product_id": row[0], "customer_id": row[1],
                                   "rental_start_date": row[2],
                                   "rental_end_date": row[3],
                                   "cost_per_day": row[4]}
                    rentals.insert_one(rental_info)
        except:
            rentals_errors += 1

    return ((products, customers, rental_units), (product_errors, customer_errors, rentals_errors))


def show_available_products():
    """returns a dictionary of available products"""
    mongo = MongoDBConnection()

    product_dict = {}
    with mongo:
        database = mongo.connection.store

        result = database.product.find({"quantity_available": {"$gt": "0"}})
        for row in result:
            product_dict[row["product_id"]] = {"description": row["description"],
                                               "product_type": row["product_type"],
                                               "quantity_available": row["quantity_available"]}

    return product_dict

def show_rentals(product_id):
    """returns a dictionary with information of users who have rented product"""
    mongo = MongoDBConnection()

    renters_dict = {}
    with mongo:
        database = mongo.connection.store

        result = database.rentals.find({"product_id": product_id})
        for row in result:
            query = database.customer.find_one({"customer_id": row["customer_id"]})
            renters_dict[query["customer_id"]] = {"name": query["name"],
                                                  "address": query["address"],
                                                  "phone_number": query["phone_number"],
                                                  "email": query["email"]}

    return renters_dict
