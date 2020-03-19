'''
Database
interacts with the database via files formatted from csv files
'''
import sys
sys.path.append("./hp_norton_inventory")
import logging
import csv_handler as csvh
from mongo_connect import *
import threading
from queue import Queue
import os.path
import pymongo
import time
from timeit import timeit as timer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_data(directory_name, customer_file, product_file, rental_file, db_queue):
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
            db_collections = hpnorton_db[name]
            try:
                # verify that the file exists first
                if os.path.isfile(f'{directory_name}/{file_names[i]}'):
                    generate_thread = threading.Thread(target=csv_handler.generate_document_list,
                                                       args=[f'{directory_name}/{file_names[i]}', name, db_queue])
                    # start thread and send the
                    # return value to the queue
                    generate_thread.start()
                    # generate_thread.join()
                    # get data from the queue
                    documents = db_queue.get()
            except FileNotFoundError as error:
                logger.info(f' File not found {error}!')
                ERROR_COUNT[name]+=1
                pass
            # write to the database with data returned from the queue
            try:
                db_collections.insert_many(documents)
                document_totals = [document_id for document_id in db_collections.find()]
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


def show_available_products():
    ''' returns a list of items available for rent '''
    mongo = MongoDBConnection()

    with mongo:
        hpnorton_db = mongo.connection.hpnorton_db
        product_totals = [product for product in hpnorton_db.product.find()]
        available = list(filter(lambda units: int(units['quantity_available']) > 0, product_totals))

        return available

def show_rentals(product_id):
    ''' returns the matching fields information based on product id '''
    mongo = MongoDBConnection()

    with mongo:
        hpnorton_db = mongo.connection.hpnorton_db
        rental_totals = [rental for rental in hpnorton_db.rental.find()]
        rented_unit = list(filter(lambda units: units['product_id'] == product_id, rental_totals))
        
        return rented_unit

def main():
    ''' main method to interact with mongodb '''
    start = time.perf_counter()
    mongo = MongoDBConnection()
    db_queue = Queue()
    
    output = import_data('data', 'customer.csv','product.csv','rental.csv', db_queue)
    logger.info(f' Total number of invetory and errors {output}')
    available = show_available_products()
    logger.info(f' Current list of available items: {len(available)}')

    rentals = show_rentals('prd006')
    logger.info(f" Returning item: {rentals}")
    end = time.perf_counter()
    print(end-start)

    with mongo:
        database = mongo.connection.hpnorton_db
        yorn = input("Drop data?")
        if yorn.upper() == 'Y':
            database['customer'].drop()
            database['rental'].drop()
            database['product'].drop()

if __name__ == "__main__":
#     output_code = '''
# db_queue = Queue()
# output = import_data('data', 'customer.csv','product.csv','rental.csv', db_queue)
#     '''
#     print(timer(output_code,globals=globals(),number=100))
    main()
