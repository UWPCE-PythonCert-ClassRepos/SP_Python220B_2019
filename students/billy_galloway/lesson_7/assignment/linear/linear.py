'''
Database
interacts with the database via files formatted from csv files
'''
# import sys
# sys.path.append("./hp_norton_inventory")
import logging
import time
import cProfile, pstats
import linear_csv_handler as csvh
from mongo_connect import *
from timeit import timeit as timer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def import_data(directory_name, customer_file, product_file, rentals_file):
    ''' import data from csv files into database to be used in functions '''
    mongo = MongoDBConnection()
    csv_handler = csvh.CsvHandler()

    ERROR_COUNT = {
        'PRODUCT_ERROR': 0,
        'CUSTOMER_ERROR': 0,
        'RENTALS_ERROR': 0
    }

    INVENTORY_COUNT = {
        'product_totals': 0,
        'customer_totals': 0,
        'rental_totals': 0
    }

    product_file = f'{directory_name}/{product_file}'
    customer_file = f'{directory_name}/{customer_file}'
    rentals_file = f'{directory_name}/{rentals_file}'

    with mongo:
        # generate hpnorton_db
        hpnorton_db = mongo.connection.hpnorton_db

        # collections in database
        product_db = hpnorton_db['product']
        customer_db = hpnorton_db['customer']
        rentals_db = hpnorton_db['rental']


        try:
            products = csv_handler.generate_document_list(product_file, "product")
        except FileNotFoundError as error:
            logger.info(f' File not found {error}')
            ERROR_COUNT['PRODUCT_ERROR']+=1
        

        try:
            customers = csv_handler.generate_document_list(customer_file, "customer")
        except FileNotFoundError as error:
            logger.info(f' File not found {error}')
            ERROR_COUNT['CUSTOMER_ERROR']+=1

        try:
            rentals = csv_handler.generate_document_list(rentals_file, "rental")
        except FileNotFoundError as error:
            logger.info(f' File not found {error}')
            ERROR_COUNT['RENTALS_ERROR']+=1

        # write to database
        try:
            product_db.insert_many(products)
            product_totals = [product_id for product_id in product_db.find()]
            INVENTORY_COUNT['product_totals'] = len(product_totals)
        except UnboundLocalError as error:
            logger.info(f' {error}')
            ERROR_COUNT['PRODUCT_ERROR']+=1

        try:
            customer_db.insert_many(customers)
            customer_totals = [customer_id for customer_id in customer_db.find()]
            INVENTORY_COUNT['customer_totals'] = len(customer_totals)
        except UnboundLocalError as error:
            logger.info(f' {error}')
            logger.info(ERROR_COUNT['CUSTOMER_ERROR'])
            ERROR_COUNT['CUSTOMER_ERROR']+=1

        try:
            rentals_db.insert_many(rentals)
            rental_totals = [rental_id for rental_id in rentals_db.find()]
            INVENTORY_COUNT['rental_totals'] = len(rental_totals)
        except UnboundLocalError as error:
            logger.info(f' {error}')
            ERROR_COUNT['RENTALS_ERROR']+=1

        inventory_count = [INVENTORY_COUNT['product_totals'],
                           INVENTORY_COUNT['customer_totals'],
                           INVENTORY_COUNT['rental_totals']]

        error_count = [ERROR_COUNT['PRODUCT_ERROR'],
                       ERROR_COUNT['CUSTOMER_ERROR'],
                       ERROR_COUNT['RENTALS_ERROR']]
                      
        return [tuple(inventory_count), tuple(error_count)]

  
def show_available_products():
    ''' returns a list of items available for rent '''
    mongo = MongoDBConnection()
    #available_units = {}

    with mongo:
        hpnorton_db = mongo.connection.hpnorton_db
        product_totals = [product for product in hpnorton_db.products.find()]
        available = list(filter(lambda units: int(units['quantity_available']) > 0, product_totals))

        return available

def show_rentals(product_id):
    ''' returns the matching fields information based on product id '''
    mongo = MongoDBConnection()

    with mongo:
        hpnorton_db = mongo.connection.hpnorton_db
        rental_totals = [rental for rental in hpnorton_db.rentals.find()]
        rented_unit = list(filter(lambda units: units['product_id'] == product_id, rental_totals))

        return rented_unit

def main():
    ''' main method to interact with mongodb '''
    mongo = MongoDBConnection()          
    output = import_data('data', 'customer.csv', 'product.csv', 'rental.csv')
 
    logger.info(f' Total number of invetory and errors {output}')

    with mongo:
        database = mongo.connection.hpnorton_db
        yorn = input("Drop data?")
        if yorn.upper() == 'Y':
            database['customers'].drop()
            database['rentals'].drop()
            database['products'].drop()

if __name__ == "__main__":
    output_code = '''
output = import_data('data', 'customer.csv','product.csv','rental.csv')
    '''
    print(timer(output_code,globals=globals(),number=1))
    main()
    # profiler = cProfile.Profile()
    # profiler.run('main()')
    # profiler.print_stats()
    # pstats.Stats(profiler).sort_stats('time').print_stats() 
                          