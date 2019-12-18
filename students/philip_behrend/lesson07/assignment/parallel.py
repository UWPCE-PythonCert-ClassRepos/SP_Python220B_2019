""" Database file for HP Norton furniture store """

import logging
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from threading import Thread
from multiprocessing import Queue 

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

def read_csv_file(filename, collect_name):
    result_data = pd.read_csv(filename)
    result_records = result_data.iloc[:, 0].count()
    result_data = result_data.to_dict('records')
    return result_data

def write_to_mongo(filename, collect_name):
    #init_time = datetime.now()
    try:
        input_data = read_csv_file(filename, collect_name)
        collect_name.insert_many(input_data)
    except FileNotFoundError as e:
        LOGGER.error(f'Error importing {filename}\nThe following exception occurred {e}')
    #elapsed_time = (datetime.now() - init_time).total_seconds()
    return input_data



def import_file(data_queue, filename, collect_no=0, sep=',', encoding='ISO-8859-1'):
    """ This module imports three CSV files into MongoDB"""
    start = datetime.now()
    mongo = MongoDBConnection()

    with mongo:
        # Mongo database connection
        db = mongo.connection.NortonFurniture

        # Add collections in database
        if collect_no == 0:
            collection = db.products
        elif collect_no == 1:
            collection = db.customers
        else:
            collection = db.rentals

        # Count initial entries
        start_ct = collection.estimated_document_count()

        # Insert file data from csv
        records = write_to_mongo(filename, collection)
    
    end_ct = collection.estimated_document_count()
    end = datetime.now()
    elapsed_time = (end - start).total_seconds()
    out_data = (end_ct - start_ct, start_ct, end_ct, elapsed_time)
    data_queue.put(out_data)

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
    t1 = import_file('products.csv')
    out_data = Queue()
    prod_thread = Thread(target=import_file, args=(out_data, 'products.csv',0))
    prod_thread.start()
    cust_thread = Thread(target=import_file, args=(out_data, 'customers.csv',1))
    cust_thread.start()
    rent_thread = Thread(target=import_file, args=(out_data, 'rentals.csv',2))
    rent_thread.start()

    prod_thread.join()
    cust_thread.join()
    rent_thread.join()
    prod_output = out_data.get()
    cust_output = out_data.get()
    rent_output = out_data.get()

    logging.info(f'Product entry elapsed time: {prod_output[3]}')
    logging.info(f'Customer entry elapsed time: {cust_output[3]}')
    logging.info(f'Rental entry elapsed time: {rent_output[3]}')

