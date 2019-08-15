""""
download mongodb
create the following directories for your project
data
data/db

must use 127.0.0.1 on windows
pip install pymongo

"""
import logging
import os
import time
import datetime
import types
from os.path import join, abspath
from functools import wraps
from pymongo import MongoClient
from pymongo import errors
import pandas as pd
# noqa # pylint: disable=too-few-public-methods, too-many-locals

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def diagnose(func):
    """
    decorator for the HPNortonDatabase class method
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        function to write to a text file with processed time, records
        """
        start = time.time()
        b_counts, a_counts = 0, 0
        mongo = args[0].mongo

        # counts = products.count_documents({}) + customers.count_documents({})
        #         rentals.count_documents({}))

        with mongo:
            db_hp = mongo.connection.HPNorton

            for col in db_hp.collection_names():
                b_counts += db_hp[col].count_documents({})

            result = func(*args, **kwargs)
            end = time.time()

            for col in db_hp.collection_names():
                a_counts += db_hp[col].count_documents({})

        with open('timings.txt', mode='a+') as file:
            file.write('current_time: {}, function_name: {}, processed_time: {}, \
number_records_before: {}, number_records_after: \
{}\n'.format(datetime.datetime.now(),
             func.__name__, end-start,
             b_counts, a_counts))
        return result
    return wrapper


class DiagnosticMeta(type):
    """Metaclass to do diagnostic"""
    def __new__(cls, name, bases, attr):
        """Replace each function with a decorated version of the function for
            name, value in attr.items()"""

        for method_name, value in attr.items():
            if isinstance(value, (types.FunctionType, types.MethodType)):
                attr[method_name] = diagnose(value)

        # Return a new type called DiagnosticMeta
        return super(DiagnosticMeta, cls).__new__(cls, name, bases, attr)


class MongoDBConnection(object):
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        print('__init__()')

    def __enter__(self):
        """enter executin of the with block"""
        self.connection = MongoClient(self.host, self.port)
        print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        "exit execution of the with block"
        print('__exit__()')
        self.connection.close()


class HPNortonDatabase(metaclass=DiagnosticMeta):
    """Class to instantiate mongo db connection and methods"""
    mongo = MongoDBConnection()
    # with mongo:
    #     db_hp = mongo.connection.HPNorton

    # def print_collection(self, collection_name):
    #     '''
    #     function to print a given table (collection_name)
    #     '''
    #     with self.mongo:
    #         db_hp = self.mongo.connection.HPNorton
    #         collection = db_hp.collection_name
    #         for col in collection.find({}):
    #             for keys in col.keys():
    #                 print('{', keys, ":", col[keys], '}')

    def delete_database(self):
        '''
        function to delete all tables
        '''
        with self.mongo:
            db_hp = self.mongo.connection.HPNorton

            customers = db_hp["customers"]
            inventory = db_hp["inventory"]
            rental = db_hp["rental"]

            customers.drop()
            inventory.drop()
            rental.drop()

    def import_data(self, directory_name, product_file, customer_file,
                    rental_file):

        """function to imports data from csv files and puts in database"""

        inventory_error, customer_error, rental_error = 0, 0, 0
        inventory_count, customer_count, rental_count = 0, 0, 0

        with self.mongo:
            # mongodb database; it all starts here
            db_hp = self.mongo.connection.HPNorton

            # collection in database
            customers = db_hp["customers"]
            inventory = db_hp["inventory"]
            rental = db_hp["rental"]

            # notice how easy these are to create and that they are "schemaless"
            # that is, the Python module defines the data structure in a dict,
            # rather than the database which just stores what it is told

            try:
                inventory_df = pd.read_csv(join(abspath(directory_name), product_file))
                inventory_input = inventory_df.to_dict('records')
                inventory.insert_many(inventory_input)
                inventory_count = inventory_df.shape[0]

            except (FileNotFoundError, errors.PyMongoError) as exc:
                inventory_error += 1
                LOGGER.error(f"Can not load {product_file} file.  Exception {exc}")

            try:
                customers_df = pd.read_csv(join(abspath(directory_name), customer_file))
                customers_input = customers_df.to_dict('records')
                customers.insert_many(customers_input)
                customer_count = customers_df.shape[0]

            except (FileNotFoundError, errors.PyMongoError) as exc:
                customer_error += 1
                LOGGER.error(f"Can not load {customer_file} file. Exception {exc}")

            try:
                rental_df = pd.read_csv(join(abspath(directory_name),
                                             rental_file))
                rental_input = rental_df.to_dict('records')
                rental.insert_many(rental_input)
                rental_count = rental_df.shape[0]

            except (FileNotFoundError, errors.PyMongoError) as exc:
                rental_error += 1
                LOGGER.error(f"Can not load {rental_file} file.  \
                             Exception {exc}")

            error_count = (inventory_error, customer_error, rental_error)
            record_count = (inventory_count, customer_count, rental_count)

            return (record_count, error_count)

    def show_rentals(self, product_id):
        '''
        function to show all users for a given product_id
        '''
        # related data

        with self.mongo:
            db_hp = self.mongo.connection.HPNorton
            result = []
            rental = db_hp['rental']
            customers = db_hp['customers']

            for product in rental.find({'Product_ID': product_id}):
                query = {"Customer_ID": product["Customer_ID"]}
                for a_customer in customers.find(query):
                    a_customer.pop("Credit_Limit", None)
                    a_customer.pop("Status", None)
                    a_customer.pop("_id", None)
                    result.append(a_customer)
        return result

    def show_customers(self):
        '''
        function to show all customers
        '''
        results = {}

        with self.mongo:
            # mongodb database; it all starts here
            db_hp = self.mongo.connection.HPNorton
            customers = db_hp['customers']
            for a_customer in customers.find():
                a_customer.pop("_id", None)
                results[a_customer['Customer_ID']] = a_customer

        return results

    def show_available_products(self):
        '''
        function to show all available products
        '''
        results = {}

        with self.mongo:
            # mongodb database; it all starts here
            db_hp = self.mongo.connection.HPNorton
            inventory = db_hp["inventory"]
            for a_product in inventory.find():
                a_product.pop("_id", None)
                results[a_product['Product_ID']] = a_product

        return results


if __name__ == "__main__":

    #test for Mongo database.py
    CWD = os.getcwd()
    FOLDER_NAME = os.path.join(os.path.abspath(CWD), "data")

    hp_norton = HPNortonDatabase()

    hp_norton.delete_database()

    print(hp_norton.import_data(FOLDER_NAME, 'inventory.csv',
                                'customers.csv', 'rental.csv'))

    #print(hp_norton.show_rentals('p00001'))

    print(hp_norton.show_customers())
