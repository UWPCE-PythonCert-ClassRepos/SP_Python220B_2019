import csv
import json
import logging
import os
os.chdir('../old_database/')
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


def format_data(csv_file):
    ''' import data from csv files into database to be used in functions '''
    try:
        with open(csv_file, newline='') as csvfile:
            hpnorton_db_reader = csv.DictReader(csvfile, delimiter=',')
            documents = list(hpnorton_db_reader)

            if csv_file == 'customer.csv':
                for document in documents:
                    customer = {
                        'customer_id': document['customer_id'],
                        'name': document['name'],
                        'home_address': document['home_address'],
                        'email_address': document['email_address'],
                        'phone_number': document['phone_number'],
                        'status': document['status'],
                        'credit_limit': document['credit_limit']
                    }

                    yield customer

            elif csv_file == 'product.csv':
                for document in documents:
                    product = {
                        'product_id': document['product_id'],
                        'description': document['description'],
                        'product_type': document['product_type'],
                        'quantity_available': document['quantity_available']
                    }

                    yield product

            elif csv_file == 'rentals.csv':
                for document in documents:
                    rental = {
                        'customer_id': document['customer_id'],
                        'name': document['name'],
                        'home_address': document['home_address'],
                        'phone_number': document['phone_number'],
                        'email_address': document['email_address']
                    }

                    yield rental

    except FileNotFoundError:
        logger.info(f'File not found')


def main():
    ''' main method to interact with mongodb '''
    mongo = MongoDBConnection()

    with mongo:
        # generate hpnorton_db
        hpnorton_db = mongo.connection.hpnorton_db

        # collections in database
        customers = hpnorton_db['customers']
        rentals = hpnorton_db['rentals']
        products = hpnorton_db['products']

        customer = [customer for customer in format_data('customer.csv')]
        product = [product for product in format_data('product.csv')]
        rental = [rental for rental in format_data('rentals.csv')]

        # write to database
        customers.insert_many(customer)
        products.insert_many(product)
        rentals.insert_many(rental)

        
        # for name in customers.find():
        #     print(f'List for {name["name"]}')
        #     query = {"name": name["name"]}
        #     for customer in customers.find(query):
        #         print(f'{name["name"]} has collected {customer}')

        # # start afresh next time?
        # yorn = input("Drop data?")
        # if yorn.upper() == 'Y':
        #     customers.drop()
        #     rentals.drop()
        #     products.drop()

if __name__ == "__main__":
    main()    

