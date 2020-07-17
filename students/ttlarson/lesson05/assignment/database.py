""""
must use 127.0.0.1 on windows
pip install pymongo

"""
import logging
import os
import pandas as pd
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

# pylint: disable=broad-except
# pylint: disable=too-many-locals

class MongoDBConnection():
    """ MongoDB Connection """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows """
        self.host = host
        self.port = port
        self.connection = None
        logging.info('Starting Mongo connection ...')

    def __enter__(self):
        """ On entering: creating the connection to Mongo  """
        self.connection = MongoClient(self.host, self.port)
        logging.info('Mongo connected.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ On exiting: closing the connection to Mongo  """
        self.connection.close()
        logging.info('Mongo connection closed.')

def print_mdb_collection(collection_name):
    """ print everything in collection_name """
    for doc in collection_name.find():
        print(doc)

def import_data_csv(directory_name, data_file):
    """ import data from csv files """
    file_path = os.path.join(directory_name, data_file)
    logging.info('Opening file: %s', file_path)

    data = pd.DataFrame()

    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        logging.error('Cannot find file: %s', file_path)

    logging.info('Done with file: %s', file_path)

    return data

def import_data(directory_name, product_file, customer_file, rentals_file):
    """ import data from CSV files, then insert into MongoDB """
    record_count = {
        "customers": 0,
        "products": 0,
        "rentals": 0
    }
    err_count = {
        "customers": 0,
        "products": 0,
        "rentals": 0
    }

    mdb = MongoDBConnection()
    with mdb:
        mongo = mdb.connection.HPNorton

        # create collections if not exist
        logging.info('Creating collections ...')
        customers = mongo["customers"]
        products = mongo["products"]
        rentals = mongo["rentals"]

        # clear out the collections and start fresh
        logging.info('Clearing collection data ...')
        customers.drop()
        products.drop()
        rentals.drop()

        logging.info('Start loading customer data from CSV file ...')
        data_customer = import_data_csv(directory_name, customer_file)
        dict_customer = data_customer.to_dict('records')

        try:
            insert_result_customers = customers.insert_many(dict_customer)
            record_count['customers'] = len(insert_result_customers.inserted_ids)
        except Exception as err:
            err_count['customers'] += 1
            logging.info('Customer error count incremented by 1.')
            logging.error('%s', err)

        logging.info('Start loading product data from CSV file ...')
        data_product = import_data_csv(directory_name, product_file)
        dict_product = data_product.to_dict('records')

        try:
            insert_result_products = products.insert_many(dict_product)
            record_count['products'] = len(insert_result_products.inserted_ids)
        except Exception as err:
            err_count['products'] += 1
            logging.info('Product error count incremented by 1.')
            logging.error('%s', err)

        logging.info('Start loading rental data from CSV file ...')
        data_rental = import_data_csv(directory_name, rentals_file)
        dict_rental = data_rental.to_dict('records')

        try:
            insert_result_rentals = rentals.insert_many(dict_rental)
            record_count['rentals'] = len(insert_result_rentals.inserted_ids)
        except Exception as err:
            err_count['rentals'] += 1
            logging.info('Rental error count incremented by 1.')
            logging.error('%s', err)

        tup_record_count = (record_count['products'],
                            record_count['customers'],
                            record_count['rentals'])
        tup_error_count = (err_count['products'],
                           err_count['customers'],
                           err_count['rentals'])

    return tup_record_count, tup_error_count

def show_available_products():
    """ function to show all the products avalable """
    available = dict()

    mdb = MongoDBConnection()
    with mdb:
        mongo = mdb.connection.HPNorton

        for product in mongo.products.find():
            if product['quantity_available'] > 0:
                key = product['product_id']
                product = {'description': product['description'],
                           'product_type': product['product_type'],
                           'quantity_available': product['quantity_available']}

                available[key] = product

    return available

def show_rentals(product_id):
    """ function to show the list of user information by using product_id  """
    user_info = dict()

    mdb = MongoDBConnection()
    with mdb:
        mongo = mdb.connection.HPNorton

        for rental in mongo.rentals.find({"product_id": product_id}):
            user_id = rental['user_id']
            for customer in mongo.customers.find():
                if user_id == customer['user_id']:
                    user = {'name': customer['name'],
                            'address': customer['address'],
                            'phone_number': customer['phone_number'],
                            'email': customer['email']}

                    user_info[user_id] = user

        return user_info

if __name__ == '__main__':
    DATA_FILE_CUSTOMER = 'customers.csv'
    DATA_FILE_PRODUCT = 'products.csv'
    DATA_FILE_RENTAL = 'rentals.csv'
    DATA_FILE_PATH = os.getcwd()
    logging.info('Current directory: %s', DATA_FILE_PATH)

    import_data(DATA_FILE_PATH, DATA_FILE_PRODUCT, DATA_FILE_CUSTOMER, DATA_FILE_RENTAL)
    products_available = show_available_products()
    logging.info(products_available)

    users_E0001 = show_rentals('E0001')
    logging.info(users_E0001)

    users_F0001 = show_rentals('F0001')
    logging.info(users_F0001)

    users_I0003 = show_rentals('I0003')
    logging.info(users_I0003)

    users_F0002 = show_rentals('F0002')
    logging.info(users_F0002)
