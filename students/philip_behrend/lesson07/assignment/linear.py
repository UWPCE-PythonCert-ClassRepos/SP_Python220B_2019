""" Database file for HP Norton furniture store """

import logging
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ Be sure to use the ip address not name for local windows"""
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

def reset_db():
    """ This module deletes all records in the database"""
    mongo = MongoDBConnection()

    start_prod = 0
    end_prod = 0
    start_cust = 0
    end_cust = 0

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

    LOGGER.info("Successfully deleted documents")


def import_file(prod_file, cust_file, rent_file, sep=',', encoding='ISO-8859-1'):
    """ This module imports three CSV files into MongoDB"""
    start = datetime.now()
    mongo = MongoDBConnection()

    with mongo:
        # Mongo database connection
        db = mongo.connection.NortonFurniture

        # Add collections in database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        # Count initial entries
        start_prod = db.products.estimated_document_count()
        start_cust = db.customers.estimated_document_count()

        # Insert product data from csv
        prod_init_time = datetime.now()
        try:
            product_data = pd.read_csv(prod_file)
            product_records = product_data.iloc[:, 0].count()
            product_data = product_data.to_dict('records')
            products.insert_many(product_data)
        except FileNotFoundError as e:
            LOGGER.error(f'Error importing {prod_file}\nThe following exception occurred {e}')
        prod_elapsed_time = (datetime.now() - prod_init_time).total_seconds()

        # Insert customer data from csv
        cust_init_time = datetime.now()
        try:
            cust_data = pd.read_csv(cust_file)
            cust_records = cust_data.iloc[:, 0].count()
            cust_data = cust_data.to_dict('records')
            customers.insert_many(cust_data)
        except FileNotFoundError as e:
            LOGGER.error(f'Error importing {cust_file}\nThe following exception occurred {e}')
        cust_elapsed_time = (datetime.now() - cust_init_time).total_seconds()

        # Insert rental data from csv
        try:
            rental_data = pd.read_csv(rent_file)
            rental_records = rental_data.iloc[:, 0].count()
            rental_data = rental_data.to_dict('records')
            rentals.insert_many(rental_data)
        except FileNotFoundError as e:
            LOGGER.error(f'Error importing {rent_file}\nThe following exception occurred {e}')
    
    end_prod = db.products.estimated_document_count()
    end_cust = db.customers.estimated_document_count()
    end = datetime.now()
    elapsed_time = (end - start).total_seconds()
    return (end_prod - start_prod, start_prod, end_prod, prod_elapsed_time), \
           (end_cust - start_cust, start_cust, end_cust, cust_elapsed_time)


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


if __name__ == '__main__':
    result = import_file('products.csv', 'customers.csv', 'rentals.csv')
    logging.info(f"Product metrics: {result[0]}")
    logging.info(f"Customer metrics: {result[1]}")
