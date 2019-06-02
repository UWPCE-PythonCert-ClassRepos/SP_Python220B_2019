"""Mongo DB class to import the CSV data and to display the data"""
import csv
import os
import logging
import pymongo
from pymongo import MongoClient
from prettytable import PrettyTable

x = PrettyTable()
x.field_names = ["name", "Address", "Phone", "Email"]


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


def import_data(directory_name, product_file, customer_file, rental_file):
    """Import data for inventory management"""

    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.hpnorton

        product_file_csv = os.path.join(directory_name, product_file)
        customer_file_csv = os.path.join(directory_name, customer_file)
        rental_file_csv = os.path.join(directory_name, rental_file)
        products_error = 0
        customers_error = 0
        rentals_error = 0

        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        with open(product_file_csv) as product:
            products_csv = csv.DictReader(product)
            for row in products_csv:
                print(row)
                try:
                    products.insert_one(row)
                except pymongo.errors.DuplicateKeyError:
                    products_error += 1

        with open(customer_file_csv) as customer:
            customers_csv = csv.DictReader(customer)
            for row in customers_csv:
                print(row)
                try:
                    customers.insert_one(row)
                except pymongo.errors.DuplicateKeyError:
                    customers_error += 1

        with open(rental_file_csv) as rental:
            rentals_csv = csv.DictReader(rental)
            for row in rentals_csv:
                print(row)
                try:
                    rentals.insert_one(row)
                except Exception as ex:
                    rentals_error += 1

        products_count = db.products.count_documents({})
        customers_count = db.customers.count_documents({})
        rentals_count = db.rentals.count_documents({})

        tuple1 = (products_count, customers_count, rentals_count)
        tuple2 = (products_error, customers_error, rentals_error)
        return tuple1, tuple2
    #
    # with mongo:
    #     db = mongo.connection.hpnorton
    #     print("Printing the collection of DB")
    #     print(db.list_collection_names())


def show_available_products():
    """Display the products in inventory"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpnorton
        products = db.products.find()
        print("NAME" + "    " + "Address" + "    " + "phone_number" + "   " + "email")
        for product in products:
            print(f'{product["name"]} {product["address"]} { product["phone_number"]} {product["email"]}\n')


def show_rentals():
    """Display the users who rented a product"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpnorton
        # print(product_id)
        # print(type(product_id))
        rentals = db.rentals.find()
        # {'product_id': {'$in': [product_id]}}
        #type(rentals)
        #rentals = db.rentals.find()
        #print(rentals)
        # for rental in rentals:
        #     print("i am in")
        #     print(f'{rental["product_id"]} \n')
        #
        for rental in rentals:
            print(rental['user_id'])


def drop_collections():
    """Function to clean the collections created"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpnorton
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()


if __name__ == '__main__':
    directory_name = "/Users/guntur/PycharmProjects/uw/" \
               "p220/SP_Python220B_2019/students/g_rama/lesson05/src/data"
    import_data(directory_name, "customers.csv", "products.csv", "rentals.csv")
    show_available_products()

    show_rentals()
    drop_collections()

