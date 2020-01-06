""" Database file for HP Norton furniture store 
    @wraps documentation here:
    https://nickcdryan.com/2017/02/17/decorators-and-metaprogramming-in-python/
"""

import logging
from datetime import datetime
import pandas as pd
from pymongo import MongoClient
from math import sqrt
from functools import wraps
import inspect

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def diagnostic_decorator(func):
    """ Decorator for timing """
    @wraps(func)
    def timing_wrapper(*args, **kwargs):
        db_collections = {}
        before_count = {}
        start = datetime.now()
        for collection in db.collection_names():
            before_count[collection] = db[collection].count_documents({})
        out_data = func(*args, **kwargs)
        for collection in db.collection_names():
            db_collections[collection] = db[collection].count_documents({}) - before_count[collection]
        end = datetime.now()

        with open('findings.txt', 'a') as f:
            f.write('Function: '+ func.__name__ + '\n')
            f.write('Time elapsed: ' + str(end-start) + '\n')
            f.write('Records Processed:\n')
            for key, val in db_collections.items():
                f.write('\t' + str(key) + ': ' + str(val) + ' \n') 
            f.write('\n')       
        return out_data
    return timing_wrapper

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

class MongoDBMethods():
    """Mongo DB for Norton Furniture, with associated methods """
    
    mongo = MongoDBConnection()

    @diagnostic_decorator
    def print_mdb_collection(self, collection_name):
        """ Print complete collection information """
        with self.mongo:
        # Mongo database connection
            db = self.mongo.connection.NortonFurniture
            for doc in db[collection_name].find():
                print(doc)

    @diagnostic_decorator
    def import_file(self, prod_file, cust_file, rent_file, sep=',', encoding='ISO-8859-1'):
        """ This module imports three CSV files into MongoDB"""

        product_err = 0
        customer_err = 0
        rental_err = 0


        with self.mongo:
            # Mongo database connection
            db = self.mongo.connection.NortonFurniture

            # Add collections in database
            products = db["products"]
            customers = db["customers"]
            rentals = db["rentals"]

            # Start with empty collections
            products.drop()
            customers.drop()
            rentals.drop()

            # Insert product data from csv
            try:
                product_data = pd.read_csv(prod_file)
                product_records = product_data.iloc[:, 0].count()
                product_data = product_data.to_dict('records')
                products.insert_many(product_data)
            except FileNotFoundError as e:
                product_err += 1
                LOGGER.error(f'Error importing {prod_file}\nThe following exception occurred {e}')

            # Insert customer data from csv
            try:
                cust_data = pd.read_csv(cust_file)
                cust_records = cust_data.iloc[:, 0].count()
                cust_data = cust_data.to_dict('records')
                customers.insert_many(cust_data)
            except FileNotFoundError as e:
                customer_err += 1
                LOGGER.error(f'Error importing {cust_file}\nThe following exception occurred {e}')

            # Insert rental data from csv
            try:
                rental_data = pd.read_csv(rent_file)
                rental_records = rental_data.iloc[:, 0].count()
                rental_data = rental_data.to_dict('records')
                rentals.insert_many(rental_data)
            except FileNotFoundError as e:
                rental_err += 1
                LOGGER.error(f'Error importing {rent_file}\nThe following exception occurred {e}')

            return (product_records, cust_records, rental_records), \
                (product_err, customer_err, rental_err)

    @diagnostic_decorator
    def show_available_products(self):
        """ Returns dict of available products """

        with self.mongo:
            db = self.mongo.connection.NortonFurniture
            query = {'quantity_available': {'$gt': 0}}
            result = db.products.find(query)

            prod_dict = {}
            for item in result:
                prod_dict[item['id']] = {'description': item['description'],
                                        'product_type': item['product_type'],
                                        'quantity_available': item['quantity_available']}

        return prod_dict

    @diagnostic_decorator
    def show_rentals(self, product_id):
        """ Return rental dict corresponding to customer id """

        with self.mongo:
            db = self.mongo.connection.NortonFurniture
            rent_dict = {}
            rental_info = db.rentals.find({'productid': product_id})
            for item in rental_info:
                cust_info = db.customers.find_one({'id': item['userid']})
                rent_dict[cust_info['id']] = {'name': cust_info['name'],
                                            'address': cust_info['address'],
                                            'phone': cust_info['phone']
                                            }
        return rent_dict

if __name__ == "__main__":
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.NortonFurniture 
        db["products"].remove({})
        db["customers"].remove({})
        db["rentals"].remove({})

        mongo_test = MongoDBMethods()
        mongo_test.import_file('products.csv', 'customers.csv', 'rentals.csv')
        mongo_test.print_mdb_collection('products')
        mongo_test.show_available_products()
        mongo_test.show_rentals(99)
