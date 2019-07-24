""""
download mongodb
create the following directories for your project
data
data/db

must use 127.0.0.1 on windows
pip install pymongo

"""
import logging
from os.path import join, abspath
from functools import partial
from multiprocessing import Pool
import timeit
import time
import os
import threading
from pymongo import MongoClient
from pymongo import errors
import pandas as pd
# import queue
# noqa # pylint: disable=too-few-public-methods, too-many-locals

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


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


def print_collection(collection_name):
    '''
    function to print a given table (collection_name)
    '''
    for doc in collection_name.find():
        print(doc)


def delete_database():
    '''
    function to delete all tables
    '''

    mongo = MongoDBConnection()

    with mongo:
        db_hp = mongo.connection.HPNorton
        customers = db_hp["customers"]
        inventory = db_hp["inventory"]
        rental = db_hp["rental"]

        customers.drop()
        inventory.drop()
        rental.drop()


def import_data(directory_name, file_names):
    '''
    function to import an input file given a file path and file_name
    '''
    with Pool(processes=len(file_names)) as pool:
        func = partial(import_file, directory_name)
        result = pool.map(func, file_names)

    # for file in argv:
    #     worker = threading.Thread(name=file, target=import_file,
    #                               args=(directory_name, file))
    #     #worker.setDaemon(True)
    #     procs.append(worker)
    #     worker.start()
    #     # result.append(my_queue.get())

    # for proc in procs:
    #     proc.join()
    #     result.append(MY_QUEUE.get())

    return result


def import_file(*args):

    """function to imports data from csv files and puts in database"""
    start_time = time.time()
    mongo = MongoDBConnection()
    directory_name = args[0]
    input_file = args[1]
    error_count, inserted_count = 0, 0

    print('Starting', threading.currentThread().getName(), os.getpid())

    with mongo:
        # mongodb database; it all starts here
        db_hp = mongo.connection.HPNorton

        # collection in database
        if "customer" in input_file:
            table_entity = db_hp["customers"]
        elif "inventory" in input_file:
            table_entity = db_hp["inventory"]
        elif "rental" in input_file:
            table_entity = db_hp["rental"]
        else:
            print("Bad import file")
            Exception("Bad import file")

        old_count = table_entity.count_documents({})

        # notice how easy these are to create and that they are "schemaless"
        # that is, the Python module defines the data structure in a dict,
        # rather than the database which just stores what it is told
        try:
            input_df = pd.read_csv(join(abspath(directory_name), input_file))
            input_dict = input_df.to_dict('records')
            table_entity.insert_many(input_dict)
            inserted_count = input_df.shape[0]

        except (FileNotFoundError, errors.PyMongoError) as exc:
            error_count += 1
            LOGGER.error(f"Can not load {input_file} file.  Exception {exc}")

        # MY_QUEUE.put((inserted_count, old_count, inserted_count+old_count,
        #               time.time() - start_time))

        return (inserted_count, old_count, inserted_count+old_count,
                time.time() - start_time)


def show_rentals(product_id):
    '''
    function to show all users for a given product_id
    '''
    # related data
    mongo = MongoDBConnection()

    with mongo:
        db_hp = mongo.connection.HPNorton
        result = []
        rental = db_hp['rental']
        customers = db_hp['customers']

        for product in rental.find({'Product_ID':product_id}):
            query = {"Customer_ID": product["Customer_ID"]}
            for a_customer in customers.find(query):
                a_customer.pop("Credit_Limit", None)
                a_customer.pop("Status", None)
                a_customer.pop("_id", None)
                result.append(a_customer)
    return result


def show_customers():
    '''
    function to show all customers
    '''
    results = {}
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        db_hp = mongo.connection.HPNorton
        customers = db_hp['customers']
        for a_customer in customers.find():
            a_customer.pop("_id", None)
            results[a_customer['Customer_ID']] = a_customer

    return results


def show_available_products():
    '''
    function to show all available products
    '''
    results = {}
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        db_hp = mongo.connection.HPNorton
        inventory = db_hp["inventory"]
        for a_product in inventory.find():
            a_product.pop("_id", None)
            results[a_product['Product_ID']] = a_product

    return results


def import_data_into_mango():

    """test import all good data"""
    # delete_database()

    data_files = ['customers.csv', 'inventory.csv', 'rental.csv']

    folder_name = ""
    cwd = os.getcwd()
    folder_name = os.path.join(os.path.abspath(cwd), "data")

    test_import = import_data(folder_name, data_files)

    print(test_import)


if __name__ == "__main__":

    print(timeit.timeit("import_data_into_mango()",
                        setup="from __main__ import import_data_into_mango",
                        number=1))
