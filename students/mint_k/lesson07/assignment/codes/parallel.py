"""This is for lesson05"""

import os
import csv
import logging
import time
import threading
import queue
from pymongo import MongoClient
#pylint: disable = W1202

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


class MyThread(threading.Thread):
    """my thread class that can be used to run things in parallel"""

    def __init__(self, myqueue, category_name, file_name):
        """setting up initial variables"""
        self.queue = myqueue
        self.category_name = category_name
        self.file_name = file_name
        super().__init__()


    def run(self):
        """create db, do the counts"""
        start_time = time.time()
        mongo = MongoDBConnection()
        with mongo:
            my_db = mongo.connection.media
            categories = my_db[self.category_name]
            categories.drop()
            start_count = categories.count_documents({})
            my_errors = 0


            try:
                categ_list = access_csv(self.file_name)
                LOGGER.info(f'{self.category_name} is {categ_list}')
                #Writing to database using mongo
                categories.insert_many(categ_list)
                #Recording number of customer added
                categ_count = len(categ_list)
            except (FileNotFoundError, KeyError, IndexError) as my_e:
                my_errors += 1
                LOGGER.error(my_e)

            end_count = categories.count_documents({})
            end_time = time.time() - start_time
            my_output = (self.category_name, categ_count, start_count,
                         end_count, end_time)
        self.queue.put(my_output)
        self.queue.task_done()



def import_data(directory_name, product_file, customer_file, rentals_file):
    """This function takes a directory name three csv files as input,
    one with product data, one with customer data and the third one
    with rentals data and creates and populates a new MongoDB database
    with these data. It returns 2 tuples: the first with a record count of
    the number of products, customers and rentals added (in that order),
    the second with a count of any errors that occurred, in the same order."""

    results = queue.Queue()
    customer_csv = os.path.join(directory_name, customer_file)
    products_csv = os.path.join(directory_name, product_file)
    rentals_csv = os.path.join(directory_name, rentals_file)

    customer_thread = MyThread(results, 'customers', customer_csv)
    product_thread = MyThread(results, 'products', products_csv)
    rentals_thread = MyThread(results, 'rentals', rentals_csv)

    threads = [customer_thread, product_thread, rentals_thread]

    for thread in threads:
        thread.start()

    results.join()

    my_output = [results.get() for things in range(len(threads))]

    return my_output


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

if __name__ == "__main__":
    START_TIME = time.time()
    DIRECTORY_NAME = ''
    PRODUCT_FILE = 'products.csv'
    CUSTOMER_FILE = 'customers.csv'
    RENTALS_FILE = 'rentals.csv'
    RESULTS = import_data(DIRECTORY_NAME, PRODUCT_FILE, CUSTOMER_FILE, RENTALS_FILE)
    END_TIME = time.time()
    print('Run time: {}'.format(END_TIME - START_TIME))
    print(RESULTS)
