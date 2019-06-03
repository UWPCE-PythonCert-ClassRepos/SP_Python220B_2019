"""Mongo DB class to import the CSV data and to display the data"""
import csv
import os
import logging
import pymongo
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


def import_data(directory_name, product_file, customer_file, rental_file):
    """Import data for inventory management"""

    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.hpnorton
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

        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        with mongo:
            db = mongo.connection.hpnorton
            print("Printing the collection of DB")
            print(db.list_collection_names())

        try:
            with open(product_file_csv, encoding='utf-8-sig') as product:
                products_csv = csv.DictReader(product)
                for row in products_csv:
                    print(row)
                    try:
                        products.insert_one(row)
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
                        customers.insert_one(row)
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
                        rentals.insert_one(row)
                    except Exception as ex:
                        rentals_error += 1
        except FileNotFoundError:
            rentals_error += 1

        products_count = db.products.count_documents({})
        customers_count = db.customers.count_documents({})
        rentals_count = db.rentals.count_documents({})

        tuple1 = (products_count, customers_count, rentals_count)
        tuple2 = (products_error, customers_error, rentals_error)
        return tuple1, tuple2


def show_available_products():
    """Display the products in inventory"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpnorton
        print(db.list_collection_names())
        available_products = {}
        for p in db.products.find():
            if int(p["quantity_available"]) > 0:
                available_products.update({p["product_id"]: {p["description"],
                                                             p["product_type"],
                                                             p["quantity_available"]}})

        return available_products


def show_rentals(product_id):
    """Display the users who rented a product"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpnorton
        rented_user_id = []
        rentals_all = db.rentals.find({'product_id': {'$eq': product_id}})
        for rental in rentals_all:
            rented_user_id.append(rental['user_id'])
        print(rented_user_id)
        rented_user_info = {}
        for user in rented_user_id:
            for rented_user in db.customers.find({'user_id': {'$eq': user}}):
                rented_user_info.update({rented_user["user_id"]: {rented_user["name"],
                                                                  rented_user["address"],
                                                                  rented_user["email"]}})
        return rented_user_info


def drop_collections():
    """Function to clean the collections created"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpnorton
        db.products.drop()
        print("deleted the products")
        db.customers.drop()
        print("deleted the customers")
        db.rentals.drop()
        print("deleted the rentals")


if __name__ == '__main__':
    directory_name = "/Users/guntur/PycharmProjects/uw/" \
               "p220/SP_Python220B_2019/students/g_rama/lesson05/src/data"
    imd1 = import_data(directory_name, "products.csv", "customers.csv", "rentals.csv")
    show_avail = show_available_products()
    print(show_avail)

    show_rentals("p101")
    test = show_rentals("p899")
    print(test)
    print(imd1)
    drop_collections()


