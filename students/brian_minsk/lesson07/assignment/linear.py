""" Code for lesson07 assignment, adapted from the lesson05 assignment.
"""

import os
import csv
import logging
from time import process_time
from pymongo import MongoClient

logging.basicConfig(level=logging.ERROR)
LOGGER = logging.getLogger(__name__)

class MongoDBConnection():
    """ MongoDB Connection

    This class's code is swiped from "Part 5: Python code" from the lesson05 materials.
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

MONGO = MongoDBConnection()
with MONGO:
    DB = MONGO.connection.media
    PRODUCT_COLLECTION = DB['product']
    CUSTOMER_COLLECTION = DB['customers']
    RENTAL_COLLECTION = DB['rentals']

def import_data(directory_name="csv_files", product_file="product.csv",
                customer_file="customers.csv"):
    """ Note: For lesson07 we are no longer interested in the rentals data.

    Take a directory name and two csv files as input, one with product data, one with customer
    data. Create and populate a MongoDB database with these data. Returns two tuples, one for
    products, the other for customers, containing: number of products processed, tuple with a
    document count of the number documents processed, the number of documents in the collection at
    the beginning, the number of documents in the collection at the end, and the time spent
    importing the documents (in that order).

    Keyword arguments:
    directory_name - the directory that contains the csv_files
    product_file - a csv file with product data with the first line containing the field names
    customer_file - a csv file with customer data with the first line containing the field
                    names
    """
    n_docs_start_products, n_docs_start_customers = count_documents()

    t_import_start = process_time()
    n_products = populate_collection(os.path.join(directory_name, product_file),
                                     PRODUCT_COLLECTION)
    t_product_import_time = process_time() - t_import_start

    t_import_start = process_time()
    n_customers = populate_collection(os.path.join(directory_name, customer_file),
                                      CUSTOMER_COLLECTION)
    t_customer_import_time = process_time() - t_import_start

    n_docs_end_products, n_docs_end_customers = count_documents()

    return (n_products, n_docs_start_products, n_docs_end_products, t_product_import_time),\
           (n_customers, n_docs_start_customers, n_docs_end_customers, t_customer_import_time)


def count_documents():
    """ Return the number of documents in the product and customer collections.
    """
    return PRODUCT_COLLECTION.count_documents({}), CUSTOMER_COLLECTION.count_documents({})


def populate_collection(file_path, hpn_collection):
    """ Populate a collection with data from a CSV file. Return the number of documents added to
    the collection.

    Arguments:
    file_path - the path to the CSV file, including the file name.
    hpn_collection - a MongoDB collection
    """
    docs = 0

    with open(file_path, newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            with MONGO:
                hpn_collection.insert_one(row)
                docs += 1
    return docs


def main():
    """ Time the program and save the results to a file.
    """
    with open("linear_performance.csv", 'w', newline='') as file:
        times = []
        for i in range(1000):
            product_results, customer_results = import_data()

            times.append("{}.,{},{}\n".format(i + 1, product_results[3], customer_results[3]))

        file.writelines(times)


if __name__ == "__main__":
    main()
