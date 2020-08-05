#!/usr/bin/env python
""""
Lesson 10 version - using MetaProgramming to time functions

Database using MongoDB to store HP Norton data
must use 127.0.0.1 on windows
pip install pymongo
pylint exceptions - invalid_name (for 'db')

"""
import logging
import csv
import time
import functools
from pymongo import MongoClient



logger = logging.getLogger()
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('db.log')
file_handler.setLevel(logging.INFO)

file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


DIRECTORY_NAME = 'data/'
PRODUCT_FILE = 'products.csv'
PRODUCTS = []
''' Product Code, Description, Product Type, Quantity Available, Rental Price'''
RENTALS_FILE = 'rentals.csv'
RENTALS = []
''' User ID, Product Code, Units Rented, Rental Start, Rental End'''
CUSTOMER_FILE = 'customers.csv'
CUSTOMERS = []
'''User ID, First Name, Last Name, Address, Phone, Emails, Is_active, Credit Limit'''

IMPORTED = []
FAILED = []

class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        logger.debug('Initializing MongoDBConnection with host = %s'
                     ' and port = %s', self.host, self.port)

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        logger.debug('Beginning connection with MongoDB')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug('Shutting down the connection to MongoDB')
        self.connection.close()




def timing(func):
    '''Logs the run time of each function decorated'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        func_time = end - start
        logger.info(f'{func_time:.6f} secs || TIME for function {func.__name__!r}\n')
        return value
    return wrapper

@timing
def import_data(directory, product_csv, customer_csv, rentals_csv):
    '''Imports three CSV files to put in the database'''
    logger.debug('IMPORTING DATA')
    import_single_file(directory, product_csv, PRODUCTS)
    import_single_file(directory, customer_csv, CUSTOMERS)
    import_single_file(directory, rentals_csv, RENTALS)
    insert_in_mongo()
    logging.debug('Done with importing all 3 files.')
    return [tuple(IMPORTED), tuple(FAILED)]

@timing
def import_single_file(directory, chosen_csv, chosen_data):
    '''Imports a single csv and puts data in the chosen_data'''
    with open(directory + chosen_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            chosen_data.append(row) #need to append on the dictionary object
        logger.debug('Holding data from %s', chosen_data)

@timing
def insert_in_mongo():
    '''Runs mongo and imports the files into the MongoDB'''
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        logger.debug('db has been instantiated')
        #instantiate the collections
        rentals_col = db['rentals']
        customers_col = db['customers']
        products_col = db['products']

        logger.info('Adding in [ %s ] records in PRODUCTS collection', len(PRODUCTS))
        add_to_database(products_col, PRODUCTS)

        logger.info('Adding in [ %s ] records in CUSTOMERS collection', len(CUSTOMERS))
        add_to_database(customers_col, CUSTOMERS)

        logger.info('Adding in [ %s ] records in RENTALS collection', len(RENTALS))
        add_to_database(rentals_col, RENTALS)

        logger.debug('Added: %s', str(IMPORTED))

@timing
def add_to_database(collection, chosen_data):
    '''Adds a single group of data to the database'''
    logger.debug('Adding %s this collection to the database: \n', str(chosen_data))
    count = 0
    error = 0
    for row in chosen_data:
        try:
            ins = collection.insert_one(dict(row))
            logger.debug(ins)
            count += 1
        except TypeError:
            error += 1
    IMPORTED.append(count)
    FAILED.append(error)

@timing
def show_available_products():
    '''List out all products with Quantity Available > 0'''
    avProd = {}
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        for row in db['products'].find():
            if int(row['Quantity Available']) > 0:
                avProd[row['Product Code']] = {'Product Code': row['Product Code'],
                                               'Quantity Available': row['Quantity Available'],
                                               'Description': row['Description'],
                                               'Product Type': row['Product Type']}
            else:
                logger.debug('Quantity is not available for %s \n', row['Product Code'])

            logger.debug(row)
        logger.debug('\n')
        logger.debug(avProd)
    return avProd

@timing
def delete_db():
    '''Open connection to db and drop() products, customers, rentals'''
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        logger.info('Deleting all 3 collections')
        db['products'].drop()
        db['customers'].drop()
        db['rentals'].drop()

@timing
def show_all_products():
    '''This prints out every product in the product collection'''
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        all_products = {}
        for row in db['products'].find():
            logger.debug(row)
            all_products[row['Product Code']] = {'Product Code': row['Product Code'],
                                                 'Quantity Available': row['Quantity Available'],
                                                 'Description': row['Description'],
                                                 'Product Type': row['Product Type']}
    logger.debug('These are all the Products: %s \n\n', str(all_products))
    return all_products

@timing
def show_rentals(product_code):
    '''This searches a product_code for rental history of the product'''
    mongo = MongoDBConnection()
    with mongo:
        rental_history = {}
        db = mongo.connection.media
        query = {"Product Code": product_code}
        for row in db['rentals'].find(query):
            for renter in db['customers'].find({"User ID": row['User ID']}):
                name = renter['First Name'] + ' ' + renter['Last Name']
                new_row = dict([('User ID', row['User ID']), ('Name', name),
                                ('Address', renter['Address']), ('Phone', renter['Phone']),
                                ('Email', renter['Email'])])
                logger.debug(new_row)
                rental_history[renter['User ID']] = new_row
    logger.debug('These are the found rental history of product %s :\n\n%s',
                 str(product_code), str(rental_history))
    return rental_history

if __name__ == '__main__':
    #This segment is to run through each of the functions for timing characterization
    logger.info('\n%s\nIn main/name statement -> To test timing functionality \n%s\n',
                '-'*100, '-'*100)
    import_data(DIRECTORY_NAME, PRODUCT_FILE, CUSTOMER_FILE, RENTALS_FILE)
    show_all_products()
    show_available_products()
    show_rentals('SLD2')
    delete_db()
