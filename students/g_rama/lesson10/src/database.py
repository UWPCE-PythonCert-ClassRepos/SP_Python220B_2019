"""Mongo DB class to import the CSV data and to display the data"""
import csv
import os
import pymongo
import time
from pymongo import MongoClient
import types


function_times = 'timings.txt'
# reference: https://stackabuse.com/python-metaclasses-and-metaprogramming/
def timefunc(fn, *args, **kwargs):
    """A timer to calculate the time of elapsed time for a function"""

    def fncomposite(*args, **kwargs):
        start_timer = time.time()
        rt = fn(*args, **kwargs)
        elapsed_time = time.time() - start_timer
        print("Executing %s took %s seconds." % (fn.__name__, elapsed_time), file=open("timings.txt", "a"))
        return rt
    # return the composite function
    return fncomposite


class Timed(type):
    """Timing of the passed class functions"""

    def __new__(cls, name, bases, attr):
        # replace each function with
        # a new function that is timed
        # run the computation with the provided args and return the computation result
        for name, value in attr.items():
            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = timefunc(value)

        return super(Timed, cls).__new__(cls, name, bases, attr)


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


class Timing(metaclass=Timed):

    def import_data(self, directory_name, product_file, customer_file, rental_file):
        """Import data for inventory management"""

        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            DB = mongo.connection.hpnorton
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

            products = DB["products"]
            customers = DB["customers"]
            rentals = DB["rentals"]

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

            products_count = DB.products.count_documents({})
            customers_count = DB.customers.count_documents({})
            rentals_count = DB.rentals.count_documents({})

            tuple1 = (products_count, customers_count, rentals_count)
            tuple2 = (products_error, customers_error, rentals_error)
            return tuple1, tuple2

    def show_available_products(self):
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

    def show_rentals(self, product_id):
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

    def drop_collections(self):
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

