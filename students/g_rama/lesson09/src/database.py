"""Mongo DB class to import the CSV data and to display the data"""
import csv
import os
import pymongo
from pymongo import MongoClient


class MongoDBConnection:
    """MongoDB Connection"""

    def __init__(self, host='localhost', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        self.products = None
        self.customers = None
        self.rentals = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        self.DB = self.connection.hpnorton
        self.products = self.DB["products"]
        self.customers = self.DB["customers"]
        self.rentals = self.DB["rentals"]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rental_file):
    """Import data for inventory management"""

    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        products_error = 0
        customers_error = 0
        rentals_error = 0
        try:
            product_file_csv = os.path.join(directory_name, product_file)
        except FileNotFoundError:
            products_error += 1
        try:
            customer_file_csv = os.path.join(directory_name, customer_file)
        except FileNotFoundError:
            customers_error += 1
        try:
            rental_file_csv = os.path.join(directory_name, rental_file)
        except FileNotFoundError:
            rentals_error += 1

        with mongo:
            DB = mongo.connection.hpnorton
            print("Printing the collection of DB")
            print(DB.list_collection_names())

        try:
            with open(product_file_csv, encoding='utf-8-sig') as product:
                products_csv = csv.DictReader(product)
                for row in products_csv:
                    print(row)
                    try:
                        mongo.products.insert_one(row)
                    except pymongo.errors.DuplicateKeyError:
                        products_error += 1
        except FileNotFoundError:
            products_error += 1

        try:
            with open(customer_file_csv, encoding='utf-8-sig') as customer:
                customers_csv = csv.DictReader(customer)
                for row in customers_csv:
                    print(row)
                    try:
                        mongo.customers.insert_one(row)
                    except pymongo.errors.DuplicateKeyError:
                        customers_error += 1
        except FileNotFoundError:
            customers_error += 1

        try:
            with open(rental_file_csv, encoding='utf-8-sig') as rental:
                rentals_csv = csv.DictReader(rental)
                for row in rentals_csv:
                    print(row)
                    try:
                        mongo.rentals.insert_one(row)
                    except Exception as ex:
                        rentals_error += 1
        except FileNotFoundError:
            rentals_error += 1

        products_count = DB.products.count_documents({})
        customers_count = DB.customers.count_documents({})
        rentals_count = DB.rentals.count_documents({})

        tuple1 = (products_count, customers_count, rentals_count)
        tuple2 = (products_error, customers_error, rentals_error)
        return tuple1, tuple2


def show_available_products():
    """Display the products in inventory"""
    mongo = MongoDBConnection()
    with mongo:
        DB = mongo.connection.hpnorton
        print(DB.list_collection_names())
        available_products = {}
        for prod in DB.products.find():
            if int(prod["quantity_available"]) > 0:
                available_products.update({prod["product_id"]: {prod["description"],
                                                                prod["product_type"],
                                                                prod["quantity_available"]}})

        return available_products


def show_rentals(product_id):
    """Display the users who rented a product"""
    mongo = MongoDBConnection()
    with mongo:
        DB = mongo.connection.hpnorton
        rented_user_id = []
        rentals_all = DB.rentals.find({'product_id': {'$eq': product_id}})
        for rental in rentals_all:
            rented_user_id.append(rental['user_id'])
        print(rented_user_id)
        rented_user_info = {}
        for user in rented_user_id:
            for rented_user in DB.customers.find({'user_id': {'$eq': user}}):
                rented_user_info.update({rented_user["user_id"]: {rented_user["name"],
                                                                  rented_user["address"],
                                                                  rented_user["email"]}})
        return rented_user_info


def drop_collections():
    """Function to clean the collections created"""
    mongo = MongoDBConnection()
    with mongo:
        DB = mongo.connection.hpnorton
        DB.products.drop()
        print("deleted the products")
        DB.customers.drop()
        print("deleted the customers")
        DB.rentals.drop()
        print("deleted the rentals")
