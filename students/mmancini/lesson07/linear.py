'''
    sp_py220 assignment 7, concurrency and async
'''

#pylint: disable=too-many-statements
#pylint: disable=invalid-name
#pylint: disable=too-many-locals
#pylint: disable=no-else-continue

import csv
import os
import logging
import time
from pymongo import MongoClient


logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class MongoDBConnection():
    """ MongoDB Connection """
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

def import_data(directory_name, product_file, customer_file, rentals_file):

    '''
        des:
            read 3 csv data files and insert data into mongo db
        in:
            path to csv, products file, customers file, rentals files
        out:
            tuple total records count, errors count
    '''
    
    product_count = 0
    customer_count = 0
    rental_count = 0

    product_errors = 0
    customer_errors = 0
    rental_errors = 0

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        product_collection = database["Products"]
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   directory_name, product_file)) as csvfile:
                product_file = csv.reader(csvfile)

                for product in product_file:
                    product_info = {'product_id': product[0],
                                    'description': product[1],
                                    'product_type': product[2],
                                    'quantity_available': product[3]}
                    product_collection.insert_one(product_info)
                    product_count += 1

                    for data in product:
                        if data == '':
                            product_errors += 1
        except FileNotFoundError:
            LOGGER.error('Cannot find product_file')
            LOGGER.debug('Unable to locate product_file')
            product_errors += 1

        customer_collection = database["Customers"]
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   directory_name, customer_file)) as csvfile:
                customer_file = csv.reader(csvfile)

                for customer in customer_file:
                    customer_info = {'user_id': customer[0],
                                     'name': customer[1],
                                     'address': customer[2],
                                     'phone_number': customer[3],
                                     'email': customer[4]}
                    customer_collection.insert_one(customer_info)
                    customer_count += 1

                    for data in customer:
                        if data == '':
                            customer_errors += 1
        except FileNotFoundError:
            LOGGER.error('Cannot find customer_file')
            LOGGER.debug('Unable to locate customer_file')
            customer_errors += 1


        rental_collection = database["Rentals"]
        try:
            with open(os.path.join(os.path.dirname(__file__),
                                   directory_name, rentals_file)) as csvfile:
                rentals_file = csv.reader(csvfile)

                for rental in rentals_file:
                    rental_info = {'rid': rental[0],
                                   'product_id': rental[1],
                                   'user_id': rental[2]}
                    rental_collection.insert_one(rental_info)
                    rental_count += 1

                    for data in rental:
                        if data == '':
                            rental_errors += 1
        except FileNotFoundError:
            LOGGER.error('Cannot find rentals_file')
            LOGGER.debug('Unable to locate rentals_file')
            rental_errors += 1

    record_count = (product_count, customer_count, rental_count)
    errors_occurred = (product_errors, customer_errors, rental_errors)
    return record_count, errors_occurred

def import_products(directory_name, product_file):
    """import product data"""
    prod_start = time.time()
    error_prod = 0
    product_file_path = os.path.join(directory_name, product_file)
    mongo = MongoDBConnection()
    num_prod_processed = 0
    with mongo:
        db = mongo.connection.hp_norton
        #A collection of products, customers, rentals in the database
        products = db['Products']
        db_prod_init_count = db.products.count_documents({})
        try:
            with open(product_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    num_prod_processed += 1
                    prod_add = {'product_id': row['product_id'],
                                'description': row['description'],
                                'product_type': row['product_type'],
                                'quantity_available': row['quantity_available']}
                    try:
                        products.insert_one(prod_add)
                    except pyerror.DuplicateKeyError as error:
                        LOGGER.info('Product already in database')
                        error_prod += 1

        except FileNotFoundError:
            LOGGER.info('Product file not found')
            error_prod += 1
        db_prod_after_count = products.estimated_document_count()
        prod_end = time.time()
        return (num_prod_processed, db_prod_init_count, db_prod_after_count,
                prod_end-prod_start, error_prod)
                
def import_customers(directory_name, customer_file):
    """import customer data"""
    cust_start = time.time()
    error_cust = 0
    customer_file_path = os.path.join(directory_name, customer_file)
    mongo = MongoDBConnection()
    num_cust_processed = 0
    with mongo:
        db = mongo.connection.hp_norton
        customers = db['Customers']
        db_init_cust_count = db.customers.count_documents({})
        try:
            with open(customer_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    num_cust_processed += 1
                    cust_add = {'customer_id': row['_id'],
                                'name': row['name'],
                                'address': row['address'],
                                'phone_number': row['phone_number'],
                                'email': row['email']}
                    try:
                        customers.insert_one(cust_add)
                    except pyerror.DuplicateKeyError as error:
                        LOGGER.info('customer already in database')
                        error_cust += 1

        except FileNotFoundError:
            LOGGER.info('Customer file not found')
            error_cust += 1
    db_after_cust_count = customers.estimated_document_count()
    cust_end = time.time()
    return (num_cust_processed, db_init_cust_count, db_after_cust_count,
            cust_end-cust_start, error_cust)

def show_available_products():
    '''
        des:
            show product inventories with avaialable quanties
        in:
        out:
            dictionary of available product quantities
    '''

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        product_collection = database["Products"]
        py_dict = {}
        for product in product_collection.find():
            if product['quantity_available'] == '0':
                continue
            elif product['quantity_available'] == '':
                continue
            elif product['quantity_available'] == 'quantity_available':
                continue
            else:
                py_dict[product['product_id']] = dict([('description',
                                                        product['description']),
                                                       ('product_type',
                                                        product['product_type']),
                                                       ('quantity_available',
                                                        product['quantity_available'])])
        return py_dict

def show_rentals(product_id):
    '''
        des:
            show customer products rented for given product id
        in:
            product id
        out:
            dictionary of customers who rented given product
    '''
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        customer_collection = database["Customers"]
        rental_collection = database["Rentals"]
        py_dict = {}
        for renter in rental_collection.find():
            if product_id == renter['product_id']:
                for customer in customer_collection.find():
                    if renter['user_id'] == customer['user_id']:
                        py_dict[customer['user_id']] = dict([('name',
                                                              customer['name']),
                                                             ('address',
                                                              customer['address']),
                                                             ('phone_number',
                                                              customer['phone_number']),
                                                             ('email',
                                                              customer['email'])])
    return py_dict

def dbs_cleanup():
    '''drop the db'''
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        database["Customers"].drop()
        database["Products"].drop()
        database["Rentals"].drop()
    return 'databases dropped'

def main():

    '''
        process import data for products and customers (linear).
    '''
   
    dbs_cleanup()
    
    start_time = time.time()
    path = ('csv_files')
    products_result = import_products(path, 'product_file.csv')
    customers_result = import_customers(path, 'customer_file.csv')
    end_time = time.time()

    LOGGER.info("Product Process Results = %s" , products_result)
    LOGGER.info("Customer Process Results = %s", customers_result)
    LOGGER.info("Total Process Time = %s", end_time-start_time)
    
    return products_result, customers_result

if __name__ == "__main__":

    results_main = main()
