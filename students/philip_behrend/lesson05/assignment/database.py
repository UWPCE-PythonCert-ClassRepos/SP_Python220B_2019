""" Database file for HP Norton furniture store """

import logging
import pandas as pd
from pymongo import MongoClient

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

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

def print_mdb_collection(collection_name):
    """ Print complete collection information """
    mongo = MongoDBConnection()
    with mongo:
    # Mongo database connection
        db = mongo.connection.NortonFurniture
        for doc in db[collection_name].find():
            print(doc)

def import_file(prod_file, cust_file, rent_file, sep=',', encoding='ISO-8859-1'):
    """ This module imports three CSV files into MongoDB"""
    mongo = MongoDBConnection()

    product_err = 0
    customer_err = 0
    rental_err = 0


    with mongo:
        # Mongo database connection
        db = mongo.connection.NortonFurniture

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


def show_available_products():
    """ Returns dict of available products """
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.NortonFurniture
        query = {'quantity_available': {'$gt': 0}}
        result = db.products.find(query)

        prod_dict = {}
        for item in result:
            prod_dict[item['id']] = {'description': item['description'],
                                     'product_type': item['product_type'],
                                     'quantity_available': item['quantity_available']}

    return prod_dict


def show_rentals(product_id):
    """ Return rental dict corresponding to customer id """
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.NortonFurniture
        rent_dict = {}
        rental_info = db.rentals.find({'productid': product_id})
        for item in rental_info:
            cust_info = db.customers.find_one({'id': item['userid']})
            rent_dict[cust_info['id']] = {'name': cust_info['name'],
                                          'address': cust_info['address'],
                                          'phone': cust_info['phone']
                                         }
    return rent_dict
