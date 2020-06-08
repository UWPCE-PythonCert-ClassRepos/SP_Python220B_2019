"""
Create Mongo Database
"""

# pylint: disable=R0914
# pylint: disable=C0301
# pylint: disable=C0103
# pylint: disable=W


import logging
import csv
import os
from pymongo import MongoClient
from pymongo import errors


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

    try:
        with mongo:
            db = mongo.connection.hp_norton
            products = db["products"]
            customers = db["customers"]
            rentals = db["rentals"]

            error_dict = {product_file: 0, customer_file: 0, rentals_file: 0}

            coll_list = [products, customers, rentals]
            file_list = [product_file, customer_file, rentals_file]


            merged_list = tuple(zip(coll_list, file_list))

            for item in merged_list:
                with open(os.path.join(directory_name, item[1])) as file:
                    result = item[0].insert_many(csv.DictReader(file))
                    for doc in item[0].find():
                        LOGGER.info("Added record: {} to collection {}".format(doc, item[0]))

    except errors.PyMongoError as error:
        LOGGER.error("Error creating record: {}". format(error))
        error_dict[item[1]] += 1

    prod_num = products.find().count()
    cust_num = customers.find().count()
    rent_num = rentals.find().count()

    return ((prod_num, cust_num, rent_num),
            (error_dict[product_file], error_dict[customer_file], error_dict[rentals_file]))


def show_available_products():
    """Returns a Python dictionary of products listed as available"""
    mongo = MongoDBConnection()
    avail_dict = {}

    with mongo:
        db = mongo.connection.hp_norton
        products = db["products"]

        myquery = {"quantity_available": {"$gt": "0"}}

        mydoc = products.find(myquery)

        for prod in mydoc:
            LOGGER.info("Available Product: {}".format(prod))
            avail_dict[prod["product_id"]] = {k: v for k, v in prod.items() if k not in ("_id", "product_id")}
    LOGGER.info("All Available Prods: {}".format(avail_dict))
    return avail_dict


def show_rentals(product_id):
    """Returns a Python dictionary with the following user information
       from users that have rented products matching product_id"""
    mongo = MongoDBConnection()
    result_dict = {}

    with mongo:
        db = mongo.connection.hp_norton
        rentals = db["rentals"]
        customers = db["customers"]

        for doc in rentals.find({"product_id": product_id}):
            for customer in customers.find({"user_id": doc["user_id"]}):
                result_dict[customer["user_id"]] = {k: v for k, v in customer.items() if k not in ("_id", "user_id")}
                LOGGER.info("Product id: {}, Renter: {}".format(product_id, customer))

    return result_dict
