"""This is for lesson05"""

import os
import csv
import logging
import time
import queue as Queue
from threading import Thread
from pymongo import MongoClient


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class MongoDBConnection():
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


def access_csv(file_name):
    """Access csv files and read data, store them to python dictionary.
    and compile them to a list"""
    my_list = []

    #open csv with option as read only 
    with open(file_name, 'r') as my_csv:
        reader = csv.reader(my_csv, delimiter=',')
        header = next(reader)

        #read file row by row
        for row in reader:
            my_dict = dict(zip(header[:], row[:]))
            my_list.append(my_dict)
    return my_list


def import_data(directory_name, product_file, customer_file, rentals_file):
    """This function takes a directory name three csv files as input, 
    one with product data, one with customer data and the third one 
    with rentals data and creates and populates a new MongoDB database 
    with these data. It returns 2 tuples: the first with a record count of 
    the number of products, customers and rentals added (in that order), 
    the second with a count of any errors that occurred, in the same order."""

    #Setting up Mongo
    mongo = MongoDBConnection()
    with mongo:
        my_db = mongo.connection.media

        #Setting up DB categories for mongo
        customers = my_db['customers']
        products = my_db['products']
        rentals = my_db['rentals']

        products.drop()
        customers.drop()
        rentals.drop()

        #reading data from csv files
        #to do this, gotta define file name based on input
        customer_csv = os.path.join(directory_name, customer_file)
        products_csv = os.path.join(directory_name, product_file)
        rentals_csv = os.path.join(directory_name, rentals_file)

        #this function need to return counts of products and etc.
        #to do this, declare variables to collect number of counts.
        prod_count = 0
        cust_count = 0
        rentals_count = 0

        #also assignment wants to count errors
        prod_errors = 0
        cust_errors = 0
        rentals_errors = 0

        #now, reading data from csv files and writing them db via mongo
        try:
            customer_list = access_csv(customer_csv)
            LOGGER.info(f'customer_list is {customer_list}')
            #Writing to database using mongo
            customers.insert_many(customer_list)
            #Recording number of customer added
            cust_count = len(customer_list)
            LOGGER.info(f'Number of added customer is {cust_count}')

        except (FileNotFoundError, KeyError, IndexError) as my_e:
            cust_errors += 1
            LOGGER.error(my_e)

        try:
            prod_list = access_csv(products_csv)
            LOGGER.info(f'prod_list is {prod_list}')
            #Writing to database using mongo
            products.insert_many(prod_list)
            #Recording number of products added
            prod_count = len(prod_list)
            LOGGER.info(f'Number of added product is {prod_count}')

        except (FileNotFoundError, KeyError, IndexError) as my_e:
            prod_errors += 1
            LOGGER.error(my_e)

        try:
            rental_list = access_csv(rentals_csv)
            LOGGER.info(f'rental_list is {rental_list}')
            #Writing to database using mongo
            rentals.insert_many(rental_list)
            #Recording number of customer added
            rentals_count = len(rental_list)
            LOGGER.info(f'Number of added rentals is {rentals_count}')

        except (FileNotFoundError, KeyError, IndexError) as my_e:
            rentals_errors += 1
            LOGGER.error(my_e)

        return (prod_count, cust_count, rentals_count), (prod_errors, cust_errors, rentals_errors)


def show_available_products():
    """Returns a Python dictionary of products listed as available with the following fields:
    product_id
    description
    product_type
    quantity_available"""

    mongo = MongoDBConnection()
    prod_dict = {}
    with mongo:
        my_db = mongo.connection.media
        #finding products with availabilty. $gt means greater than.
        available_prod = my_db['products'].find({'quantity_available':{"$gt":'0'}})
        for prod in available_prod:
            prod_dict[prod['product_id']] = {
                'description':prod['description'],
                'product_type':prod['product_type'],
                'quantity_available':prod['quantity_available']}
    
    return prod_dict

def show_rentals(product_id):
    """Returns a Python dictionary with the following user information from users 
    that have rented products matching product_id:
    user_id.
    name.
    address.
    phone_number.
    email."""

    #product_id = 'prd002'
    mongo = MongoDBConnection()
    rental_dict = {}
    with mongo:
        my_db = mongo.connection.media
        #finding user that rented matching product id.
        renters = my_db['rentals'].find({'product_id':product_id})
        for renter in renters:
            user = my_db['customers'].find_one({'user_id':renter['user_id']})
            rental_dict[renter['user_id']] = {
                'name':user['name'],
                'address':user['address'],
                'phone_number':user['phone_number'],
                'email':user['email']}
     
    return rental_dict





