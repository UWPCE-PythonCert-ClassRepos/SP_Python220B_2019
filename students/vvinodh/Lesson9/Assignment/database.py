"""
Program that uses MongoDB to store and access data
"""
import logging
import csv
import os
import pymongo
from pymongo import MongoClient

# pylint: disable=W0621,C0103,C0200,R0914,W1203
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBConnection():
    """Context Manager for MongoDB. Allows for connection to database as well
    as closing the connection to the database"""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Connects to MongoDB"""
        if self.connection is None:
            try:
                logger.info('Establishing Connection to MongoDB')
                self.connection = MongoClient(self.host, self.port)
                logger.info('Connected to MongoDB')
            except pymongo.errors.ConnectionFailure as error:
                logger.error(f'Error Connecting to MongoDB. {error}')
                raise
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Closes Connection to MongoDB"""
        self.connection.close()
        logger.info('Closed connection to MongoDB')

def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    This function takes a directory name three csv files as input,
    one with product data, one with customer data and the third one with
    rentals data and creates and populates a new MongoDB database
    with these data. It returns 2 tuples: the first with a record count
    of the number of products, customers and rentals added
    (in that order), the second with a count of any errors that
    occurred, in the same order.
    """
    client = MongoDBConnection()
    with client:
        db = client.connection.mydatabase

        logger.info('creating collections...')
        product = db['product']
        customer = db['customer']
        rentals = db['rentals']
        logger.info('collections successfully created')

        product_directory = os.path.join(directory_name, product_file)
        customer_directory = os.path.join(directory_name, customer_file)
        rentals_directory = os.path.join(directory_name, rentals_file)
        logger.info('directory and file paths successfully joined')

        logger.info('adding data from csv files to collections...')
        product_error = add_data(product, product_directory)
        customer_error = add_data(customer, customer_directory)
        rentals_error = add_data(rentals, rentals_directory)
        logger.info('data added to collections successfully')

        count = (product.count_documents({}), customer.count_documents({}),
                 rentals.count_documents({}))
        errors = (product_error, customer_error, rentals_error)
        return count, errors

def add_data(collection, file_directory):
    """Adds data to collection and returns the amount of errors found"""
    try:
        collection.insert_many(csv_convert(file_directory))
        return 0
    except pymongo.errors.BulkWriteError as bwe:
        print(bwe.details)
        return len(bwe.details['writeErrors'])

def csv_convert(f):
    """Converts csv file rows into a dict for use in database"""
    dict_list = []
    with open(f, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        row1 = next(csv_reader)
        for row in csv_reader:
            dict_row = {}
            for n in range(len(row1)):
                dict_row[row1[n]] = row[n]
            dict_list.append(dict_row)
        return dict_list

def show_available_products():
    """Returns a Python dictionary of products listed as available
    with the following fields:

        product_id.
        description.
        product_type.
        quantity_available.

    {‘prd001’:{‘description’:‘60-inch TV stand’,’product_type’:’livingroom’,
    ’quantity_available’:‘3’},’prd002’:{‘description’:’L-shaped sofa’,
    ’product_type’:’livingroom’,’quantity_available’:‘1’}}
    """
    client = MongoDBConnection()

    with client:
        db = client.connection.mydatabase
        d_item = {}
        for item in db.product.find({'quantity_available': {'$gt': '0'}}):
            item_spec = {'description': item['description'],
                         'product_type': item['product_type'],
                         'quantity_available': item['quantity_available']}
            d_item[item['product_id']] = item_spec
        return d_item


def show_rentals(product_id):
    """ Returns a Python dictionary with the following user information
    from users that have rented products matching product_id:

            user_id.
            name.
            address.
            phone_number.
            email.

        For example:

        {‘user001’:{‘name’:’Elisa Miles’,’address’:‘4490 Union Street’,
        ’phone_number’:‘206-922-0882’,’email’:’elisa.miles@yahoo.com’},
        ’user002’:{‘name’:’Maya Data’,’address’:‘4936 Elliot Avenue’,
        ’phone_number’:‘206-777-1927’,’email’:’mdata@uw.edu’}}
    """
    client = MongoDBConnection()
    with client:
        db = client.connection.mydatabase

        dict_rental = {}
        for item in db.rentals.find({'product_id': product_id}):
            query = {'user_id': item['user_id']}
            for user in db.customer.find(query):
                person = {'name': user['name'], 'address': user['address'],
                          'phone_number': user['phone_number'],
                          'email': user['email']}
                dict_rental[user['user_id']] = person
            return dict_rental

def drop_all():
    """Clears all collections"""
    client = MongoDBConnection()
    with client:
        db = client.connection.mydatabase
        db.product.drop()
        db.customer.drop()
        db.rentals.drop()
        logger.info('collections succesfully cleared')

if __name__ == "__main__":
    print(import_data('', 'products.csv', 'customers.csv',
                      'rentals.csv'))
    print(show_available_products())
    print(show_rentals('1234'))
    drop_all()
