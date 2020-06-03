"""
Create Mongo Database
"""

import logging
from pymongo import MongoClient
import csv
import os

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

#Mongo boilerplate code
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


#functions
def import_data(directory_name, product_file, customer_file, rentals_file):
    """This function takes a directory name three csv files as input,
       one with product data, one with customer data and the third one
       with rentals data and creates and populates a new MongoDB
       database with these data. It returns 2 tuples: the first with
       a record count of the number of products, customers and rentals
       added (in that order), the second with a count of any errors
       that occurred, in the same order."""
    mongo = MongoDBConnection()
    
    with mongo:
        db = mongo.connection.hp_norton
        
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]
        
        coll_list = [products, customers, rentals]
        file_list = [product_file, customer_file, rentals_file]
        
        merged_list = tuple(zip(coll_list, file_list))

        for item in merged_list:
            with open(os.path.join(directory_name, item[1])) as file:
                result = item[0].insert_many(csv.DictReader(file))
                for doc in item[0].find():
                    LOGGER.info(doc)   

        prod_num = products.find().count()
        cust_num = customers.find().count()
        rent_num = rentals.find().count()
        return (prod_num, cust_num, rent_num)
        
def show_available_products():
    """Returns a Python dictionary of products listed as available"""
    pass




def show_rentals(product_id):
    """Returns a Python dictionary with the following user information
       from users that have rented products matching product_id"""
    pass

