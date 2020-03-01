'''
Database 
interacts with the database via files formatted from csv files
'''

import json
import logging
import csv_handler
from mongo_connect import *
# from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def csv_file_list(customer_file, product_file, rentals_file):
    ''' returns list of csv files to loop over '''
    return [customer_file, product_file, rentals_file]

def import_data(directory_name, customer_file, product_file, rentals_file):
    ''' import data from csv files into database to be used in functions '''
    mongo = MongoDBConnection()

    customer_file = f'{directory_name}/{customer_file}'
    product_file = f'{directory_name}/{product_file}'
    rentals_file = f'{directory_name}/{rentals_file}'

    csv_list = csv_file_list(customer_file, product_file, rentals_file)

    try:
        # for i in csv_list:
        documents = csv_handler.csv_reader(customer_file)
        customer = [customer for customer in csv_handler.customer_format(documents)]
   
        documents = csv_handler.csv_reader(product_file)
        product = [product for product in csv_handler.product_format(documents)]

        documents = csv_handler.csv_reader(rentals_file)
        rental = [rental for rental in csv_handler.rentals_format(documents)]

    except FileNotFoundError:
        logger.info(f'File not found')
    

    with mongo:
        # generate hpnorton_db
        hpnorton_db = mongo.connection.hpnorton_db

        # collections in database
        customers = hpnorton_db['customers']
        rentals = hpnorton_db['rentals']
        products = hpnorton_db['products']

        # write to database
        customers.insert_many(customer)
        products.insert_many(product)
        rentals.insert_many(rental)

        customer_totals = [customer_id for customer_id in customers.find()]
        product_totals = [product_id for product_id in products.find()]
        rental_totals = [rental_id for rental_id in rentals.find()]
      
    # inventory count (products, customers, rentals)
    inventory_count = (len(customer_totals), len(product_totals), len(rental_totals))
    # error count ()
    error_count = ("A", "B", "C")

    yorn = input("Drop data?")
    if yorn.upper() == 'Y':
        customers.drop()
        rentals.drop()
        products.drop()

    return [inventory_count, error_count]

def show_available_products():
    mongo = MongoDBConnection()

    product_totals = [product_id for product_id in products.find() if int(product_id['quantity_available']) > 0]

    with mongo:
        avaiable_totals = {
            'product_id': '',
            'description': '',
            'product_type': '',
            'quanity_available': ''
        }

    return avaiable_totals

def show_rentals(product_id):
    mongo = MongoDBConnection()

    with mongo:
        rental_totals = {
            'user_id': '',
            'name': '',
            'address': '',
            'phone_number': '',
            'email': ''
        }

    return rental_totals


def main():
    ''' main method to interact with mongodb '''
    output = import_data('old_database', 'customer.csv', 'product.csv', 'rentals.csv')
    print(output)
if __name__ == "__main__":
    main()    

