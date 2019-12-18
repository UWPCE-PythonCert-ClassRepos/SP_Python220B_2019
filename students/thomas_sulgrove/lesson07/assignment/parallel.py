"""
parallel process to compare with linear
"""

import csv
import logging
import json
from os import path
from multiprocessing import Pool
from pymongo import MongoClient
import pymongo

# Set up the logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("logger active")

class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def drop_collections():
    """Drop all the collections"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.myDB
        for collection in database.list_collection_names():
            database[collection].drop()


def import_csv(file_path):
    """Do you like json?  Do you hate csvs? Well I have a function for you!"""
    data = []
    err_count = 0
    if path.exists(file_path):
        with open(file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if any(row[key] in (None, "") for key in row):
                    LOGGER.info("inserted file has missing values")
                    err_count += 1
                else:
                    data.append(json.loads(json.dumps(row)))
                    out = {}
                    for key, val in data[0].items():
                        try:
                            out[key] = int(val)
                        except ValueError:
                            out[key] = val
                    data = [out]
            return {'data': data, 'errors': err_count}
    else:
        LOGGER.info("file DNE! path: %s", file_path)
        return {'data': [], 'errors': 0}


def insert_into_table(table_name, data):
    """takes an iterable with dictionaries and inserts them to a table"""
    err_count = 0
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.myDB

    table = database[table_name]

    for dictionary in data:
        try:
            table.insert_one(dictionary)
        except (TypeError, pymongo.errors.OperationFailure):
            err_count += 1
            LOGGER.info("error when inserting: %s", dictionary)
    return err_count


def async_import(directory_name, file_name, table_name):
    """imports the files"""
    errors = 0
    file_import = import_csv(directory_name + file_name)
    errors += file_import['errors']
    errors += insert_into_table(table_name, file_import['data'])
    records_processed = len(file_import['data'])
    return records_processed, errors


def import_data(directory_name, product_file, customer_file, rentals_file):
    """This function takes a directory name three csv files as input,
    one with product data, one with customer data and the third one with rentals data
     and creates and populates a new MongoDB database with these data.
     It returns 2 tuples: the first with a record count of the number of"""

    with Pool(processes=3) as pool:
        r_1 = pool.apply_async(async_import, (directory_name, product_file, 'product',))
        r_2 = pool.apply_async(async_import, (directory_name, customer_file, 'customer',))
        r_3 = pool.apply_async(async_import, (directory_name, rentals_file, 'rentals',))
        product_results = r_1.get()
        customer_results = r_2.get()
        rental_results = r_3.get()
    return ((product_results[0], customer_results[0], rental_results[0]),
            (product_results[1], customer_results[1], rental_results[1]))


def show_available_products():
    """Returns a Python dictionary of products listed as available"""

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.myDB

    products = database.product.find(
        {"$expr": {"$gte": [{"$toDouble": "$quantity_available"}, 0]}},
        projection={'_id': False})
    return {product.pop('product_id'): product for product in products}


def show_rentals(product_id):
    """Returns a Python dictionary with the following user information
     from users that have rented products matching product_id"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.myDB

    rentals = database.rentals.find(filter={"product_id": product_id},
                                    projection={'_id': False})

    customers = database.customer.find(filter={'user_id':
                                                   {'$in': [rental["customer_id"]
                                                            for rental in rentals]}},
                                       projection={'_id': False})

    return {customer.pop('user_id'): customer for customer in customers}
