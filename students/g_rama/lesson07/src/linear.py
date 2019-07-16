"""Mongo DB class to import the CSV data and to display the data"""
import csv
import os
import atexit
import pymongo
from pymongo import MongoClient
from line_profiler import LineProfiler
PROFILE = LineProfiler()
atexit.register(PROFILE.print_stats)


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


@PROFILE
def import_data(directory_name, customer_file, product_file, rental_file):
    """Import data for inventory management"""

    prod_pri_imp_table_count, prod_imp_table_count, prod_after_imp_table_count = \
        import_generic(directory_name, product_file, "products")
    cust_prior_imported_table_count, cust_imported_table_count, cust_after_imported_table_count = \
        import_generic(directory_name, customer_file, "customers")
    #rentals_count, rentals_error = import_generic(directory_name, rental_file, "rentals")

    customer_tuple = (cust_prior_imported_table_count, cust_imported_table_count,
                      cust_after_imported_table_count)
    product_tuple = (prod_pri_imp_table_count, prod_imp_table_count,
                     prod_after_imp_table_count)
    print(customer_tuple)
    print(product_tuple)
    return customer_tuple, product_tuple



@PROFILE
def import_generic(directory_name, import_file, imported_table):
    """A generic function to import data to mongo DB"""
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        hpdb = mongo.connection.hpnorton
        imported_error = 0
        #imported_table_count = 0
        try:
            import_file_csv = os.path.join(directory_name, import_file)
        except FileNotFoundError:
            imported_error += 1
        imported_table = imported_table
        imp_table = hpdb[imported_table]
        prior_imported_table_count = hpdb[imported_table].count()
        try:
            with open(import_file_csv, encoding='utf-8-sig') as file_csv:
                imported_table_csv = csv.DictReader(file_csv)
                for row in imported_table_csv:
                    try:
                        imp_table.insert_one(row)
                    except pymongo.errors.DuplicateKeyError:
                        imported_error += 1

                after_imported_table_count = hpdb[imported_table].count()

        except FileNotFoundError:
            imported_error += 1
        imported_table_count = after_imported_table_count - prior_imported_table_count
        print(imported_table_count)
        print(imported_error)

        return prior_imported_table_count, imported_table_count, after_imported_table_count


def show_available_products():
    """Display the products in inventory"""
    mongo = MongoDBConnection()
    with mongo:
        hpdb = mongo.connection.hpnorton
        print(hpdb.list_collection_names())
        available_products = {}
        for prod in hpdb.products.find():
            if int(prod["quantity_available"]) > 0:
                available_products.update({prod["product_id"]: {prod["description"],
                                                                prod["product_type"],
                                                                prod["quantity_available"]}})

        return available_products


def show_rentals(product_id):
    """Display the users who rented a product"""
    mongo = MongoDBConnection()
    with mongo:
        hpdb = mongo.connection.hpnorton
        rented_user_id = []
        rentals_all = hpdb.rentals.find({'product_id': {'$eq': product_id}})
        for rental in rentals_all:
            rented_user_id.append(rental['user_id'])
        print(rented_user_id)
        rented_user_info = {}
        for user in rented_user_id:
            for rented_user in hpdb.customers.find({'user_id': {'$eq': user}}):
                rented_user_info.update({rented_user["user_id"]: {rented_user["name"],
                                                                  rented_user["address"],
                                                                  rented_user["email"]}})
        return rented_user_info


def drop_collections():
    """Function to clean the collections created"""
    mongo = MongoDBConnection()
    with mongo:
        hpdb = mongo.connection.hpnorton
        hpdb.products.drop()
        print("deleted the products")
        hpdb.customers.drop()
        print("deleted the customers")
        hpdb.rentals.drop()
        print("deleted the rentals")
