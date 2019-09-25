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
import logging
import time
from os import path
import pandas as pd
from pymongo import MongoClient


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger('console')
FH = logging.FileHandler('mongodb.log', 'w+')
FH.setLevel(logging.DEBUG)
FORMATTER = logging.Formatter(FORMAT)
FH.setFormatter(FORMATTER)
LOGGER.addHandler(FH)


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
            LOGGER.debug("The database: %s dropped.", database_name)


def csv_to_json(directory_name, filename):
    """ Load a csv file to a list """
    path_file = directory_name + "/" + filename
    if path.isfile(path_file):
        LOGGER.debug('Loading file: %s', path_file)
        data = pd.read_csv(path_file)
        return json.loads(data.to_json(orient='records'))

    LOGGER.error('Failed to load file: %s', path_file)
    return {}


def insert_to_mongo(collection_name, collection):
    """ Insert a collection into the Mongo db """
    mongo = MongoDBConnection()
    insertions = 0
    errors = 0

    with mongo:
        database = mongo.connection.hpnorton

        db_collection = database[collection_name]
        baseline_count = db_collection.count_documents({})

        for item in collection:
            count = db_collection.count_documents({"ID": item['ID']})
            LOGGER.debug("ID: %s COUNT: %s", item['ID'], count)
            if count == 0:
                LOGGER.debug("Inserting: %s", item)
                db_collection.insert_one(item)
                insertions += 1
            elif count == 1:
                LOGGER.debug("Updating: %s", item)
                db_collection.update_one({"ID": item['ID']}, {"$set": item},
                                         upsert=False)
            else:
                LOGGER.error("Invalid data state. Too many entries for %s",
                             item['ID'])
                errors += 1

        total_records = baseline_count + insertions + errors
        return (baseline_count, insertions, errors, total_records)


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

    # load the csv files
    LOGGER.debug("Reading CSV Files")
    start_time = time.time()

    products = csv_to_json(directory_name, product_file)
    customers = csv_to_json(directory_name, customer_file)
    rentals = csv_to_json(directory_name, rentals_file)

    LOGGER.debug("Inserting Data Into Mongo")

    product_results = insert_to_mongo('products', products)
    customer_results = insert_to_mongo('customers', customers)
    insert_to_mongo('rentals', rentals)

    end_time = time.time()
    execution_time = end_time - start_time
    LOGGER.debug("Execution Time: %s", execution_time)

    products_tuple = ('products', execution_time,) + product_results
    customers_tuple = ('customers', execution_time,) + customer_results

    return [products_tuple, customers_tuple]


def print_mdb_collection(collection_name):
    """ Generic collection printer """
    for doc in collection_name.find():
        print(doc)


def print_raw_products():
    """ Print Raw List of Products """
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.hpnorton
        products = database['products']
        print_mdb_collection(products)


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
        database = mongo.connection.hpnorton
        products = database['products']
        dictionary = {}

        for product in products.find():
            value = {'description': product['DESCRIPTION'],
                     'product_type': product['PRODUCT_TYPE'],
                     'quantity_available': product['QUANTITY_AVAILABLE']}
            dictionary[product['ID']] = value

        for item in dictionary.items():
            print(item)


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
        database = mongo.connection.hpnorton
        customers = database['customers']
        rentals = database['rentals']
        dictionary = {}
        if product_id:
            # special handling
            LOGGER.debug("Finding product_id: %s", product_id)
            _rentals = rentals.find({"PRODUCT_ID": product_id})

            if _rentals is not None:
                LOGGER.debug("Searching for rentals of : '%s'", product_id)
                for rental in _rentals:
                    _customers = customers.find({"ID": rental['CUSTOMER_ID']})
                    for customer in _customers:
                        value = {'name': customer['NAME'],
                                 'address': customer['ADDRESS'],
                                 'phone_number': customer['PHONE_NUMBER'],
                                 'email': customer['EMAIL']}
                        dictionary[customer['ID']] = value

                for item in dictionary.items():
                    print(item)
            else:
                LOGGER.debug("%s not found", product_id)
        else:
            print_mdb_collection(rentals)


def show_customers():
    """
    Output all customers
    """
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.hpnorton

        customers = database['customers']
        print_mdb_collection(customers)


def main():
    """ The main function for the program """
    import_stats = import_data(".",
                               'products.csv',
                               'customers.csv',
                               'rentals.csv')

    print("\nProduct List")
    show_available_products()
    print("\nRaw Product List")
    print_raw_products()
    print("\nCustomer List")
    show_customers()
    print("\nShow Rentals")
    show_rentals(product_id='prd001')
    print("\nShow All Rentals")
    show_rentals()

    for stats in import_stats:
        print("\n\tCollection:\t{:>20}"
              "\n\tTime (seconds):\t{:>20}"
              "\n\tInitial Value:\t{:>20}"
              "\n\tInsertions:\t{:>20}"
              "\n\tErrors:\t\t{:>20}"
              "\n\tFinal Count:\t{:>20}"
              .format(stats[0],
                      stats[1],
                      stats[2],
                      stats[3],
                      stats[4],
                      stats[5]))

    print("Done")


if __name__ == "__main__":
    main()
    drop_database('hpnorton')
