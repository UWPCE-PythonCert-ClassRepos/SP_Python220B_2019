#database.py
""" This module defines all the functions for HP Norton MongoDB database"""
import os
import csv
import logging
from pymongo import MongoClient

# set logging configuration
LOG_FORMAT = "%(levelname)s %(filename)s %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# using a context manager class to define the connection to a database.
class MongoDBConnection():
    """ This class defines the connetion to MongoDB."""
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def read_csv_file(dir_name, csv_file, collection, error_list):
    """ This function read a csv file into MongoDB database """
    count = 0
    try:
        filename = os.path.join(dir_name, csv_file)
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            # create the document for products collection
            for row in csv_reader:
                collection.insert_one(row)
    except FileNotFoundError:
        LOGGER.info('FileNotFoundError')
        count += 1
    except Exception as error:
        count += 1
        LOGGER.info('Exception:')
        LOGGER.info(error)
    error_list.append(count)


def import_data(dir_name, product_file, customer_file, rentals_file):
    """ This function takes a directory name three csv files as input, one with
        product data, one with customer data and the third one with rentals
        data and creates and populates a new MongoDB database with these data.
        It returns 2 tuples: the first with a record count of the number of
        products, customers and rentals added (in that order), the second with
        a count of any errors that occurred, in the same order.
    """
    client = MongoDBConnection()
    with client:
        LOGGER.info('Create A MongoDB database')
        hp_norton_db = client.connection.rental
        hp_norton_db.products.drop()
        hp_norton_db.customers.drop()
        hp_norton_db.rentals.drop()

        # create three collections.
        LOGGER.info('Create three collections')
        products = hp_norton_db['products']
        customers = hp_norton_db['customers']
        rentals = hp_norton_db['rentals']
        error_list = []

        # 1. load the products collection
        LOGGER.info('Load the products collection')
        read_csv_file(dir_name, product_file, products, error_list)
        for doc in products.find():
            LOGGER.debug(f'-- products:{doc}.')
        LOGGER.debug(f'Error_list:{error_list}')

        # 2. load the customers collection
        LOGGER.info('Load the customers collection')
        read_csv_file(dir_name, customer_file, customers, error_list)
        for doc in customers.find():
            LOGGER.debug(f'-- cusotmers:{doc}.')
        LOGGER.debug(f'Error_list:{error_list}')

        # 3. load the rentals collection
        LOGGER.info('Load the rentals collection')
        read_csv_file(dir_name, rentals_file, rentals, error_list)
        for doc in rentals.find():
            LOGGER.debug(f'-- rentals:{doc}.')
        LOGGER.debug(f'Error_list:{error_list}')
        for i in error_list:
            if i == 1:
                LOGGER.debug('!!! Error in importing csv files')
    LOGGER.info('Finish import three csv files')
    return [(products.count(), customers.count(), rentals.count()),
            tuple(error_list)]

def show_available_products():
    """ This function returns a Python dictionary of products listed as
        available with the following fields:product_id, description,
        product_type, quantity_available
    """
    client = MongoDBConnection()
    with client:
        hp_norton_db = client.connection.rental
        products = hp_norton_db['products']

        LOGGER.info('Find all the produtcs available for renting')
        the_dict = {}
        # find all the products that is available for renting.
        # $xne means not equal
        for pro in products.find({'quantity_available': {'$ne': '0'}}):
            the_dict[pro["product_id"]] = {'description': pro["description"],
                                           'product_type': pro["product_type"],
                                           'quantity_available':
                                           pro["quantity_available"]
                                           }

    LOGGER.info('Found all the produtcs available for renting')
    return the_dict

def show_rentals(product_id):
    """ This function returns a Python dictionary with the user information
        (user_id, name, address, phone_number, email) from users that have
        rented products matching product_id.
    """
    LOGGER.info(f'Find all the customers who rent the product:{product_id}')
    client = MongoDBConnection()
    with client:
        hp_norton_db = client.connection.rental
        # customers = hp_norton_db['customers']
        rentals = hp_norton_db['rentals']
        # using 'aggregate' pipline to integrate two collections 'rentals' and
        # 'customers' together.
        # Note: all the dict keys in python have to add quotation marks.
        # 'project' can specify the fields for the newly generate field
        # 'renters' and 'unset' can specify the fields for the left table
        # 'rentals'. 'lookup' performs left outer join. 'unset' must after
        # 'project'
        renter_list = rentals.aggregate([
            {'$match': {'product_id': product_id}},
            {'$lookup': {'from': 'customers', 'localField': "user_id",
                         'foreignField': "user_id", 'as': 'renters'}},
            {'$unwind': '$renters'}, # seperate each renter in renters.
            {'$project': {'renters._id': 0}},
            {'$unset': ['_id', 'product_id', 'user_id']}
        ])
        the_dict = {}
        for renter in renter_list:
            r = renter['renters']
            the_dict[r['user_id']] = {'name': r['name'],
                                      'address': r['address'],
                                      'phone_number': r['phone_number'],
                                      'email': r['email']}
        LOGGER.debug(the_dict)
    LOGGER.info(f'Finish show_rentals() successfully.')
    return the_dict
