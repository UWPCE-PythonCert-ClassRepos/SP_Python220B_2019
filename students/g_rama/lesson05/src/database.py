"""Mongo DB class to import the CSV data and to display the data"""
import csv
import os
import logging
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='localhost', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """Import data for inventory management"""

    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.hpnorton

        product_file_csv = os.path.join(directory_name, product_file)
        customer_file_csv = os.path.join(directory_name, customer_file)
        rentals_file_csv = os.path.join(directory_name, rentals_file)

        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        with open(product_file_csv) as product:
            products_csv = csv.DictReader(product)
            for row in products_csv:
                print(row)
                products.insert_one(row)

        with open(customer_file_csv) as product:
            products_csv = csv.DictReader(product)
            for row in products_csv:
                print(row)
                customers.insert_one(row)

        with open(rentals_file_csv) as product:
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
    pass


def show_rentals(product_id):
    """Display the users who rented a product"""
    pass


if __name__ == '__main__':
    directory_name = "/Users/guntur/PycharmProjects/uw/" \
               "p220/SP_Python220B_2019/students/g_rama/lesson05/src/data"
    import_data(directory_name,"customers.csv","products.csv","rentals.csv")

