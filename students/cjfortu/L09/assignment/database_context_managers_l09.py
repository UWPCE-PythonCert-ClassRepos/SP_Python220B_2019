#!/usr/bin/env python
"""
L05 baseline:

source directory during development =
'''/Users/fortucj/Documents/skoo/Python/220/SP_Python220B_2019/students/cjfortu/L05/assignment/
src_data/'''

source files =
'product_file.csv', 'customer_file.csv', 'rental_file.csv'


L09 changes:
The MongoDBConnection context manager now establishes the database connection and the appropriate
collections upon instantiation.

The collections are passed as bool arguments to MongoDBConnection.
"""
import sys
import os
import csv
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger initialized')


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='localhost', port=27017, products_init=False, customers_init=False,
                 rentals_init=False):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.products_init = products_init
        self.customers_init = customers_init
        self.rentals_init = rentals_init
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        self.db = self.connection['products_database']
        if self.products_init is True:
            self.products_collection = self.db['products']
        if self.customers_init is True:
            self.customers_collection = self.db['customers']
        if self.rentals_init is True:
            self.rentals_collection = self.db['rentals']
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def main_menu():
    """
    Provie the user with an input interface.

    Call functions based on the user's input.
    """

    valid_prompts = ['1', '2', '3', '4', '5', 'q']
    user_prompt = None

    while user_prompt not in valid_prompts:
        print("""Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              'q' - Quit""")
        user_prompt = input(": ")

    if user_prompt == '1':
        print_database()

    if user_prompt == '2':
        directory_response = input("Please provide the full path to the source files. Include "
                                   "closing '/',\nor press 'enter' to pass the current path with "
                                   "'/src_data/' added.\n: ")
        product_response = input("Please provide the filename of the product file. Include '.csv',"
                                 "\nor press 'enter' to pass 'product_file.csv'\n: ")
        customer_response = input("Please provide the filename of the customer file. Include "
                                  "'.csv',\nor press 'enter' to pass customer_file.csv'\n: ")
        rentals_response = input("Please provide the filename of the rental file. Include '.csv',"
                                 "\nor press 'enter' to pass 'rentals_file.csv'\n: ")

        if directory_response == "":
            directory_name = os.getcwd() + '/src_data/'
        else:
            directory_name = directory_response
        if product_response == "":
            product_file = 'product_file.csv'
        else:
            product_file = product_response
        if customer_response == "":
            customer_file = 'customer_file.csv'
        else:
            customer_file = customer_response
        if rentals_response == "":
            rentals_file = 'rental_file.csv'
        else:
            rentals_file = rentals_response

        import_data(directory_name, product_file, customer_file, rentals_file)

    if user_prompt == '3':
        clear_data()

    if user_prompt == '4':
        show_available_products()

    if user_prompt == '5':
        product_id = input("Please provide the product ID: ")
        show_rentals(product_id)

    if user_prompt == 'q':
        exit_program()


def print_database():
    """
    Additional function to present full database.
    """
    # streamlined database connection and collection establishment
    with MongoDBConnection(products_init=True, customers_init=True, rentals_init=True) as mongo:
        collections = [mongo.products_collection, mongo.customers_collection,
                       mongo.rentals_collection]

    for collection in collections:
        print(collection)
        for document in collection.find():
            document.pop('_id', None)
            print(document)


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Populate the new MongoDB database with source data, and return two tuples:

    1: A record count of the number of products, customers, and rentals added (in this order)
    2: A count of any errors that occured, in the same order.
    """
    # streamlined database connection and collection establishment
    with MongoDBConnection(products_init=True, customers_init=True, rentals_init=True) as mongo:
        collections = [mongo.products_collection, mongo.customers_collection,
                       mongo.rentals_collection]

    files = [product_file, customer_file, rentals_file]
    error_counts = [0, 0, 0]

    bad_file_path = False
    for i, file in enumerate(files):
        product_file_full_path = directory_name + file
        try:
            with open(product_file_full_path, 'r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.reader(csv_file)
                fields = next(csv_reader)
                extracted_data = []
                for row in csv_reader:
                    row_dict = {}
                    for j, field in enumerate(fields):
                        error = True
                        if row[j].strip() == '' and field != 'end_date':
                            error = False
                            break
                        row_dict[field] = row[j]
                    if error:
                        extracted_data.append(row_dict)
                    else:
                        error_counts[i] += 1
        except FileNotFoundError as err:
            bad_file_path = True
            print(err)
            LOGGER.info(f'{collections[i]} not added due to FileNotFoundError.')
        else:
            collections[i].insert_many(extracted_data)
            LOGGER.info(f'{collections[i]} successfully added.')

    if bad_file_path:
        LOGGER.info("Recommend clearing and reloading database due to unsuccessful insertion of"
                    " collection")

    products_count = mongo.products_collection.count_documents({})
    customers_count = mongo.customers_collection.count_documents({})
    rentals_count = mongo.rentals_collection.count_documents({})

    print('valid rows/documents =', (products_count, customers_count, rentals_count), ' ',
          'invalid rows/documents(blank entries aside from end_date) =', (error_counts[0],
                                                                          error_counts[1],
                                                                          error_counts[2]))
    return (products_count, customers_count, rentals_count), (error_counts[0], error_counts[1],
                                                              error_counts[2])


def clear_data():
    """
    Clear the database.
    """
    mongo_client = MongoClient('mongodb://localhost:27017')
    mongo_client.drop_database('products_database')
    remaining_databases = mongo_client.list_database_names()
    print('products_database dropped')
    return remaining_databases


def show_available_products():
    """
    Returns a Python dictionary of products listed as available in the following format:

    {‘prd001’:{‘description’:‘60-inch TV stand’,’product_type’:’livingroom’,
    ’quantity_available’:‘3’},’prd002’:{‘description’:’L-shaped sofa’,’product_type’:’livingroom’,
    ’quantity_available’:‘1’}}
    """
    # streamlined database connection and collection establishment
    with MongoDBConnection(products_init=True) as mongo:
        available_products = {}
        for document in mongo.products_collection.find():
            keys, values = [], []
            for key, value in document.items():
                available = True
                if key == 'quantity_available' and value == '0':
                    available = False
                    break
                else:
                    keys.append(key)
                    values.append(value)
            if available:
                available_products[values[1]] = {keys[2]: values[2], keys[3]: values[3],
                                                 keys[4]: values[4], keys[5]: values[5]}

    entries = (" {:^7}|{:^30}|{:^18}|{:^5}|{:^4}".
               format(key, value['description'], value['product_type'],
                      value['quantity_available'], value['daily_rate']) for key, value in
               available_products.items())
    print(" {:^7}|{:^30}|{:^18}|{:^5}|{:^4}".
          format('P_ID', 'DESCRIPTION', 'PRODUCT TYPE',
                 'QTY', 'RATE'))
    print('-' * 69)
    for entry in entries:
        print(entry)

    return available_products


def show_rentals(product_id):
    """
    Return a Python dictionary from users that have rented products matching product_id in the
    following format:

    {‘user001’:{‘name’:’Elisa Miles’,’address’:‘4490 Union Street’,’phone_number’:‘206-922-0882’,
    ’email’:’elisa.miles@yahoo.com’},’user002’:{‘name’:’Maya Data’,’address’:‘4936 Elliot Avenue’,
    ’phone_number’:‘206-777-1927’,’email’:’mdata@uw.edu’}}
    """
    # streamlined database connection and collection establishment
    with MongoDBConnection(customers_init=True, rentals_init=True) as mongo:
        users_of_product = {}
        for rental in mongo.rentals_collection.find({'product_id': product_id}):
            query = {'user_id': rental['user_id']}
            for document in mongo.customers_collection.find(query):
                keys, values = [], []
                for key, value in document.items():
                    keys.append(key)
                    values.append(value)
                users_of_product[values[1]] = {keys[2]: values[2], keys[3]: values[3],
                                               keys[4]: values[4], keys[5]: values[5]}

    entries = (" {:^7}|{:^30}|{:^50}|{:^12}|{:^25}".
               format(key, value['name'], value['address'],
                      value['phone_number'], value['email']) for key, value in
               users_of_product.items())
    print(" {:^7}|{:^30}|{:^50}|{:^12}|{:^25}".
          format('usrID', 'NAME', 'ADDRESS',
                 'PHONE', 'EMAIL'))
    print('-' * 129)
    for entry in entries:
        print(entry)

    return users_of_product


def exit_program():
    """
    Close the database and exit the program.
    """
    sys.exit()


if __name__ == "__main__":
    while True:
        main_menu()
        print(" \n")
