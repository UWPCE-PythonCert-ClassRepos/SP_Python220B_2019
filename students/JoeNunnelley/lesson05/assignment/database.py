#! /usr/bin/env python3

"""
Lesson 05 : Migrate CSV data to MongoDB and be able to report on it:

This week, you have been assigned to work on a prototype migration of product
data from a sample csv file into MongoDB. You will use the MongoDB API while
exploiting mongo’s ability to allow the Python module, not the database, to
specify the schema for the data to be stored.

You implementation should address the following requirements:

    As a HP Norton customer I want to see a list of all products available
    for rent so that I can make a rental choice.

    As a HP Norton salesperson I want to see a list of all of the different
    products, showing product ID, description, product type and quantity
    available.

    As a HP Norton salesperson I want to see a list of the names and contact
    details (address, phone number and email) of all customers who have rented
    a certain product.
"""
import json
from os import path
import pandas as pd
from pymongo import MongoClient


class MongoDBConnection():
    """
    Class to make connecting to and acting upon a mongo database a little
    easier
    """
    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def drop_database(database_name):
    """ Drop the a database in the mongo db """
    mongo = MongoDBConnection()
    with mongo:
        dblist = mongo.connection.list_database_names()
        if database_name in dblist:
            mongo.connection.drop_database(database_name)
            print("The database: {} dropped.".format(database_name))


def csv_to_json(directory_name, filename):
    """ Load a csv file to a list """
    path_file = directory_name + "/" + filename
    if path.isfile(path_file):
        data = pd.read_csv(path_file)
        return json.loads(data.to_json(orient='records'))

    return {}


def insert_to_mongo(collection_name, collection):
    """ Insert a collection into the Mongo db """
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpnorton

        db_collection = db[collection_name]
        result = db_collection.insert_many(collection)
        return result


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import the data into mongo from csv files

    This function takes a directory name three csv files as input,
    one with product data, one with customer data and the third one with
    rentals data and creates and populates a new MongoDB database with these
    data.
    It returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a
    count of any errors that occurred, in the same order.
    """
    record_counts = ()
    error_counts = ()

    # load the csv files
    products = csv_to_json(directory_name, product_file)
    for product in products:
        print(product)
    customers = csv_to_json(directory_name, customer_file)
    for customer in customers:
        print(customer)
    rentals = csv_to_json(directory_name, rentals_file)
    for rental in rentals:
        print(rental)

    product_results = insert_to_mongo('products', products)
    print(product_results)
    customer_results = insert_to_mongo('customers', customers)
    print(customer_results)
    rental_results = insert_to_mongo('rentals', rentals)
    print(rental_results)

    return {'record_counts': record_counts, 'error_counts': error_counts}


def print_mdb_collection(collection_name):
    """ Generic collection printer """
    for doc in collection_name.find():
        print(doc)


def show_available_products():
    """
    Output the available products from the database

    product_id.
    description.
    product_type.
    quantity_available.

    For example:

    {‘prd001’:{‘description’:‘60-inch TV stand’,’product_type’:’livingroom’,
    ’quantity_available’:‘3’},
    ’prd002’:{‘description’:’L-shaped sofa’,’product_type’:’livingroom’,
    ’quantity_available’:‘1’}}
    """
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.hpnorton

        products = db['products']
        print_mdb_collection(products)


def show_rentals(product_id=None):
    """
    Output the rental history for a/all products.

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
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.hpnorton
        rentals = db['rentals']

        if product_id:
            # special handling
            print("Finding product_id: %s", product_id)
        else:
            print_mdb_collection(rentals)


def show_customers():
    """
    Output all customers
    """
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.hpnorton

        customers = db['customers']
        print_mdb_collection(customers)


def main():
    """ The main function for the program """
    import_stats = import_data("/Users/joe.nunnelley/Documents/Node/git/"
                               "python_playground/SP_Python220B_2019/"
                               "students/JoeNunnelley/lesson05/assignment",
                               'products.csv',
                               'customers.csv',
                               'rentals.csv')
    print(import_stats)
    show_available_products()
    show_rentals(product_id='prd001')
    show_customers()
    drop_database('hpnorton')


if __name__ == "__main__":
    main()
