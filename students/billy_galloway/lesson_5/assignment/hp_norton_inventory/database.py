'''
Database 
interacts with the database via files formatted from csv files
'''

import json
import logging
import csv_converter 
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBConnection():
    ''' mongodb connection '''

    def __init__(self, host='127.0.0.1', port=27017):
        ''' initialize host and port '''
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        ''' start connection '''
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ''' close connection when finished '''
        self.connection.close()

def import_data(directory_name, customer_file, product_file, rentals_file):
    ''' import data from csv files into database to be used in functions '''
    customer_file = f'{directory_name}/{customer_file}'
    product_file = f'{directory_name}/{product_file}'
    rentals_file = f'{directory_name}/{rentals_file}'

    try:
        documents = csv_converter.csv_reader(customer_file)
        customer = [customer for customer in csv_converter.customer_format(documents)]
   
        documents = csv_converter.csv_reader(product_file)
        product = [product for product in csv_converter.product_format(documents)]

        documents = csv_converter.csv_reader(rentals_file)
        rental = [rental for rental in csv_converter.rentals_format(documents)]

    except FileNotFoundError:
        logger.info(f'File not found')
    
    mongo = MongoDBConnection()

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

        for name in customers.find():
            print(f'List for {name["name"]}')
            query = {"name": name["name"]}
            for customer in customers.find(query):
                print(f'{name["name"]} has collected {customer}')

    yorn = input("Drop data?")
    if yorn.upper() == 'Y':
        customers.drop()
        rentals.drop()
        products.drop()

def main():
    ''' main method to interact with mongodb '''
    import_data('old_database', 'customer.csv', 'product.csv', 'rentals.csv')
     
if __name__ == "__main__":
    main()    

