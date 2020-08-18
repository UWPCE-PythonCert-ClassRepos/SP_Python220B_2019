'''
table = collection.
row = document.
column = field.
Database = database
index = index
'''
import csv
# import logging
from pymongo import MongoClient
from pprint import pprint
import logging
import time
import datetime


class MongoDBConnection(object):
    """MongoDB Connection"""
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


def timer_decoration(func):
    def wrapper(*args, **kwargs):
        # define the format and tell the logging module about your format
        formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s')
        # tell the logging module HOW to save in its file (saves in current dir)
        FH = logging.FileHandler(datetime.datetime.now().strftime('%Y-%m-%d')+'.log')
        FH.setFormatter(formatter)
        # activate logger
        LOGGER = logging.getLogger()
        LOGGER.addHandler(FH)
        # LOGGER.propagate = False
        # set base level logger
        LOGGER.setLevel(logging.DEBUG)

        start = time.time()
        result = func(*args)
        total_time = time.time() - start
        logging.info("{} took {} seconds.".format(func.__name__, total_time))
        return result
    return wrapper


@timer_decoration
def import_data(directory_name,  product_file,  customer_file,  rentals_file):
    '''This function takes a directory name three csv files as input,  one with
product data,  one with customer data and the third one with rentals data and
creates and populates a new MongoDB database with these data. It returns 2
tuples:  the first with a record count of the number of products,  customers
rentals added (in that order),  the second with a count of any errors that
occurred,  in the same order.'''
    product_file_error, customer_file_error, rentals_file_error = 0, 0, 0

    mongo = MongoDBConnection()
    # why does this need a 'with'
    with mongo:
        # creating the DB
        db = mongo.connection.norton
        # creating the tables/collections
        product_file_table = db['products']
        customer_file_table = db['customers']
        rentals_file_table = db['rentals']
    try:
        with open(f'{directory_name}/{product_file}', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # how do I set the ID?
                try:
                    product_file_table.insert_one(row)
                except NameError:
                    product_file_error += 1
    except FileNotFoundError:
        product_file_error += 1

    try:
        with open(f'{directory_name}/{customer_file}', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # how do I set the ID?
                try:
                    customer_file_table.insert_one(row)
                except NameError:
                    customer_file_error += 1
    except FileNotFoundError:
        customer_file_error += 1

    try:
        with open(f'{directory_name}/{rentals_file}', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # how do I set the ID?
                try:
                    rentals_file_table.insert_one(row)
                except NameError:
                    rentals_file_error += 1
    except FileNotFoundError:
        rentals_file_error += 1

    error_count = (product_file_error, customer_file_error, rentals_file_error)

# https://docs.mongodb.com/manual/reference/method/db.collection.count/
    with mongo:
        record_count = (db.products.count(),
                        db.customers.count(),
                        db.rentals.count())
    return (error_count, record_count)


@timer_decoration
def print_mdb_collection():

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.norton

    for document in db.products.find():
        pprint(document)

    for document in db.customers.find():
        pprint(document)

    for document in db.rentals.find():
        pprint(document)


@timer_decoration
def show_available_products():
    ''' Returns a Python dictionary of products listed as available
-product_id.
-description.
-product_type.
-quantity_available.'''
    mongo = MongoDBConnection()
    show_available_products = {}
    with mongo:
        db = mongo.connection.norton
        find_them = db.products.find({"quantity_available": {"$gt": "0"}})
        for x in find_them:
            show_available_products[x['product_id']] = {
                  'description': x['description'],
                  'product_type': x['product_type'],
                  'quantity_available': x['quantity_available']}
    return show_available_products


def show_rentals(enter_product_id):
    '''Returns a Python dictionary with the following user information from
users that have rented products matching product_id:
-user_id.
-name.
-address.
-phone_number.```
-email.'''

    mongo = MongoDBConnection()
    rental_list = {}
    with mongo:
        db = mongo.connection.norton
        for each in db.rentals.find({'product_id': enter_product_id}):
            for pers in db.customers.find({'customer_id': each['customer_id']}):
                rental_list[pers['customer_id']] = {'name': pers['name'],
                                             'address': pers['address'],
                                             'phone_number': pers['phone_number'],
                                             'email': pers['email']}
    return rental_list


@timer_decoration
def cleanup():
    """empties databases"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.norton
        # creating the tables/collections
        products = db['products']
        customers = db['customers']
        rentals = db['rentals']
        products.drop()
        customers.drop()
        rentals.drop()


if __name__ == '__main__':
    import_data('csv_files', 'products.csv', 'customers.csv', 'rentals.csv')
    show_available_products()
    import_data('csv_files', 'products.csv', 'customers.csv', 'rentals.csv')
