'''
Database 
interacts with the database via files formatted from csv files
'''

import json
import logging
import csv_handler as csvh
from mongo_connect import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def csv_file_list(customer_file, product_file, rentals_file):
    ''' returns list of csv files to loop over '''
    return [customer_file, product_file, rentals_file]

def import_data(directory_name, customer_file, product_file, rentals_file):
    ''' import data from csv files into database to be used in functions '''
    mongo = MongoDBConnection()
    csv_handler = csvh.CsvHandler()
    customer = []
    product = []
    rentals = []

    ERROR_COUNT = {
        'CUSTOMER_ERROR': 0,
        'PRODUCT_ERROR': 0,
        'RENTALS_ERROR': 0
    }

    INVENTORY_COUNT = {
        'customer_totals': [],
        'product_totals': [],
        'rental_totals': []
    }

    try:
        customer_file = f'{directory_name}/{customer_file}'
        product_file = f'{directory_name}/{product_file}'
        rentals_file = f'{directory_name}/{rentals_file}'

        csv_list = csv_file_list(customer_file, product_file, rentals_file)
        # document_type = [customer, product, rentals] 
        # for i in document_type:
        #     i = generate_document_list(csv_file_list)

        # for filename in csv_list:
        #     documents = csv_handler.csv_reader(filename)
        #     csv_format_method = f'csv_handler.{item}_format({documents})'
        #     output_list = csv_format_method
        print(output_list)
        # documents = csv_handler.csv_reader(product_file)
        # product = [product for product in csv_handler.product_format(documents)]

        # documents = csv_handler.csv_reader(rentals_file)
        # rental = [rental for rental in csv_handler.rentals_format(documents)]

    except FileNotFoundError as error:
        logger.info(f'File not found {error}')
        if product_file != 'old_database/product.csv':
            ERROR_COUNT['PRODUCT_ERROR']+=1
        if customer_file != 'old_database/customer.csv':
            ERROR_COUNT['CUSTOMER_ERROR']+=1
        if rentals_file != 'old_database/rentals.csv':
            ERROR_COUNT['RENTALS_ERROR']+=1
    # with mongo:
    #     try:
    #         # generate hpnorton_db
    #         hpnorton_db = mongo.connection.hpnorton_db

    #         # collections in database
    #         customers = hpnorton_db['customers']
    #         rentals = hpnorton_db['rentals']
    #         products = hpnorton_db['products']

    #         # write to database
    #         customers.insert_many(customer)
    #         products.insert_many(product)
    #         rentals.insert_many(rental)

    #         customer_totals = [customer_id for customer_id in customers.find()]
    #         product_totals = [product_id for product_id in products.find()]
    #         rental_totals = [rental_id for rental_id in rentals.find()]

    #         INVENTORY_COUNT['customer_totals'] = len(customer_totals)
    #         INVENTORY_COUNT['product_totals'] = len(product_totals)
    #         INVENTORY_COUNT['rental_totals'] = len(rental_totals)

    #     except UnboundLocalError:
    #         pass
    #     return [INVENTORY_COUNT, ERROR_COUNT]
    

# def show_available_products():
#     mongo = MongoDBConnection()

#     product_totals = [product_id for product_id in products.find() if int(product_id['quantity_available']) > 0]

#     with mongo:
#         avaiable_totals = {
#             'product_id': '',
#             'description': '',
#             'product_type': '',
#             'quanity_available': ''
#         }

#     return avaiable_totals

# def show_rentals(product_id):
#     mongo = MongoDBConnection()

#     with mongo:
#         rental_totals = {
#             'user_id': '',
#             'name': '',
#             'address': '',
#             'phone_number': '',
#             'email': ''
#         }

#     return rental_totals


def main():
    ''' main method to interact with mongodb '''
    mongo = MongoDBConnection()

    output = import_data('old_database', 'customer.csv', 'product.csv', 'rentals.csv')
    print(output)

    with mongo:
        database = mongo.connection.hpnorton_db
        yorn = input("Drop data?")
        if yorn.upper() == 'Y':
            database['customers'].drop()
            database['rentals'].drop()
            database['products'].drop()

if __name__ == "__main__":
    main()
