"""Mongo DB class to import the CSV data and to display the data"""
import csv
import os
import pymongo
from pymongo import MongoClient
from line_profiler import LineProfiler
import atexit
from threading import Thread
from queue import Queue
import time
profile = LineProfiler()
atexit.register(profile.print_stats)
# acquire_lock = threading.Lock()

class MongoDBConnection:
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


@profile
def import_data(directory_name, product_file, customer_file, rental_file):
    """Import data for inventory management"""

    # threads = []
    products_count, products_error = import_generic(directory_name, product_file, "products")
    #products_count, products_error = threads.append(Thread(target  =  import_generic(directory_name, product_file, "products")))
    customers_count, customers_error = import_generic(directory_name, customer_file, "customers")
    rentals_count, rentals_error = import_generic(directory_name, rental_file, "rentals")

    tuple1 = (products_count, customers_count, rentals_count)
    tuple2 = (products_error, customers_error, rentals_error)
    print(tuple1)
    print(tuple2)
    return tuple1, tuple2


@profile
def import_generic(directory_name, import_file, imported_table):
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        DB = mongo.connection.hpnorton
        imported_error = 0
        imported_table_count = 0
        try:
            import_file_csv = os.path.join(directory_name, import_file)
        except FileNotFoundError:
            imported_error += 1
        imported_table = imported_table
        imp_table = DB[imported_table]
        prior_imported_table_count = DB[imported_table].count()
        try:
            with open(import_file_csv, encoding='utf-8-sig') as file_csv:
                imported_table_csv = csv.DictReader(file_csv)
                for row in imported_table_csv:
                    try:
                        imp_table.insert_one(row)
                    except pymongo.errors.DuplicateKeyError:
                        imported_error += 1
                """ Python 3.7 supports coun_documents, python 3.7 has line_profiler compiling issues"""
                # if imported_table == 'products':
                #     imported_table_count = DB.products.count_documents({})
                # elif imported_table == 'customers':
                #     imported_table_count = DB.customers.count_documents({})
                # elif imported_table == 'rentals':
                #     imported_table_count = DB.rentals.count_documents({})
                after_imported_table_count = DB[imported_table].count()
                #
                # if imported_table == 'products':
                #     imported_table_count = DB.products.count()
                # elif imported_table == 'customers':
                #     imported_table_count = DB.customers.count()
                # elif imported_table == 'rentals':
                #     imported_table_count = DB.rentals.count()
        except FileNotFoundError:
            imported_error += 1
        imported_table_count = after_imported_table_count - prior_imported_table_count
        print(imported_table_count)
        print(imported_error)

        return imported_table_count, imported_error


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
