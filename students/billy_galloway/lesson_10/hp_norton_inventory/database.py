'''
Database
interacts with the database via files formatted from csv files
'''
import logging
import csv_handler as csvh
import os.path
import pymongo
import time
from function_timer import timer
from mongo_connect import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@timer
def import_data(directory_name, product_file, customer_file, rental_file):
    ''' import data from csv files into database to be used in functions '''
    mongo = MongoDBConnection()
    csv_handler = csvh.CsvHandler()

    ERROR_COUNT = {
        'product': 0,
        'customer': 0,
        'rental': 0
    }

    INVENTORY_COUNT = {
        'product': 0,
        'customer': 0,
        'rental': 0
    }

    file_names = [f'{product_file}',
                  f'{customer_file}',
                  f'{rental_file}']

    with mongo:
        # generate hpnorton_db
        hpnorton_db = mongo.connection.hpnorton_db
        collection_names = ['product', 'customer', 'rental']

        i = 0
        for name in collection_names:
            # create collections in database
            try:
                # verify that the file exists first
                if os.path.isfile(f'{directory_name}/{file_names[i]}'):
                    documents = csv_handler.generate_document_list(f'{directory_name}/{file_names[i]}', name)
            except FileNotFoundError as error:
                logger.info(f' File not found {error}!')
                ERROR_COUNT[name]+=1
                pass
            try:
                # create the collections
                db_collection = hpnorton_db[name]
                # write to collection to database
                db_collection.insert_many(documents)
                document_totals = [document_id for document_id in db_collection.find()]
                INVENTORY_COUNT[name] = len(document_totals)
            except pymongo.errors.InvalidOperation as error:
                logger.info(f' {error} {file_names[i]}')
                ERROR_COUNT[name]+=1
            except UnboundLocalError:
                ERROR_COUNT[name]+=1
                pass
            finally:
                i+=1

        inventory_count = [INVENTORY_COUNT['product'],
                           INVENTORY_COUNT['customer'],
                           INVENTORY_COUNT['rental']]

        error_count = [ERROR_COUNT['product'],
                       ERROR_COUNT['customer'],
                       ERROR_COUNT['rental']]

        return [tuple(inventory_count), tuple(error_count)]

@timer
def show_available_products():
    ''' returns a list of items available for rent '''
    mongo = MongoDBConnection()

    with mongo:
        hpnorton_db = mongo.connection.hpnorton_db
        product_totals = [product for product in hpnorton_db.product.find()]
        available = str(filter(lambda units: int(units['quantity_available']) > 0, product_totals))

        return available

@timer
def show_rentals(products_id):
    ''' returns the matching fields information based on product id '''
    mongo = MongoDBConnection()

    with mongo:
        hpnorton_db = mongo.connection.hpnorton_db
        rental_totals = [rental for rental in hpnorton_db.rental.find()]
        rented_unit = list(filter(lambda units: units['product_id'] == products_id, rental_totals))

        return rented_unit

def main():
    ''' main method to interact with mongodb '''
    mongo = MongoDBConnection()
    print()
    start = time.perf_counter()

    # output = import_data('data', 'product_small.csv', 'customer_small.csv', 'rentals_small.csv')
    # output = import_data('data', 'product.csv', 'customer.csv', 'rentals.csv')
    output = import_data('data', 'product_large.csv', 'customer_large.csv', 'rentals_large.csv')
    available = show_available_products()
    rentals = show_rentals('prd006')

    end = time.perf_counter()
    total_time = end-start
    
    print(f'total time to finish {total_time}')

    with mongo:
        database = mongo.connection.hpnorton_db
        yorn = input("Drop data?")
        if yorn.upper() == 'Y':
            database['product'].drop()
            database['customer'].drop()
            database['rental'].drop()

if __name__ == "__main__":
    main()