#!/usr/bin/env python3
"""
Import csv to MongoDB and create queries to MongoDB
"""
import csv
import os
import logging
import types
import time
# import pprint
from pymongo import MongoClient
from pymongo import errors as pyerror

# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=unidiomatic-typecheck
# pylint: disable=undefined-loop-variable
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-function-args
# pylint: disable=no-self-use
# pylint: disable=unused-import



logging.basicConfig(filename="db.log", filemode="w", level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
LOGGER.info("Started logger")

directory_name = ".\\assignment"
file_name = "timings.txt"
file_path = os.path.join(directory_name, file_name)


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        "init to create connection"
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Connect"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit connection"""
        self.connection.close()


def timely_decorator(func, *args, **kwargs):
    """Decorator to time methods"""
    def wrapper(*args, **kwargs):
        start_timer = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_timer
        print(f'"{func.__name__}": {elapsed_time:.3f},', file=open(file_path, "a"))
        return result
    # return the composite function
    return wrapper


class Timely(type):
    """Metaclass to wrap 'timely_decorator' over every method in some class"""
    def __new__(cls, name, bases, attr):
        functions = [(method_name, method_object)
                     for method_name, method_object
                     in attr.items()
                     if type(method_object) is types.FunctionType]
        for method_name, method_object in functions:
            #print(f"{method_name} {type(method_object)}")
            attr[method_name] = timely_decorator(method_object)
        return super(Timely, cls).__new__(cls, method_name, bases, attr)


class HpData(metaclass=Timely):
    """All data access for HpNorton"""

    def import_data(self, directory_name, product_file, customer_file, rental_file, limit):
        """Manage results of import. Count number of records to add and any errors"""

        errors = {f"{product_file}_errors": 0,
                  f"{customer_file}_errors": 0,
                  f"{rental_file}_errors": 0}

        counts = {f"{product_file}_count": 0,
                  f"{customer_file}_count": 0,
                  f"{rental_file}_count": 0}

        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hp_norton_prototype
            self.import_csv(directory_name, product_file, counts, errors, db, limit)
            self.import_csv(directory_name, customer_file, counts, errors, db, limit)
            self.import_csv(directory_name, rental_file, counts, errors, db, limit)

        return (tuple(counts.values()), tuple(errors.values()))


    def import_csv(self, directory_name, collection_name, counts, errors, db, limit):
        """Insert data into collections"""
        try:
            file_name = f"{collection_name}.csv"
            collection = db[collection_name]
            with open(os.path.join(directory_name, file_name)) as file:
                lines = file.readlines()[:limit]
                result = collection.insert_many(csv.DictReader(lines))
                counts[f'{collection_name}_count'] = len(result.inserted_ids)

        except pyerror.BulkWriteError:
            errors[f'{collection_name}_errors'] += 1
            LOGGER.debug("BulkWriteError", exc_info=1)


    def show_available_products(self, product_table='product'):
        """
        Look for available products in the product database and
        return products available for rent
        """
        result = dict()
        with MongoDBConnection() as mongo:
            db = mongo.connection.hp_norton_prototype
            for doc in db[product_table].find({'quantity_available': {"$gt": "0"}}):
                LOGGER.info(doc)
                result[doc["_id"]] = {k: v for k, v in doc.items() if k != '_id'}
                LOGGER.info(result[doc["_id"]])
        return result


    def show_rentals(self, product_id, rental_table="rental", customer_table="customer"):
        """
        Based on product_id return the customer information on
        customers who rented the product.
        """
        result = dict()
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hp_norton_prototype
            for doc in db[rental_table].find({'product_id': product_id}):
                LOGGER.info(doc)
                for cust in db[customer_table].find({'_id': doc['customer_id']}):
                    LOGGER.info(cust)
                    result[cust["_id"]] = {k: v for k, v in cust.items() if k != '_id'}
                    LOGGER.info(result[cust["_id"]])
        return result


    def clear(self, product, customer, rental):
        """Clear the database for each collection"""
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.hp_norton_prototype
            db[product].drop()
            db[customer].drop()
            db[rental].drop()

# The decorator can be applied via the metaclass,
# or directly on some method, as seen here.
@timely_decorator
def run(product='product', customer='customer', rental='rental', limit=1000000):
    """Run script with limit"""
    hp_data = HpData()
    hp_data.clear(product, customer, rental)
    hp_data.import_data(directory_name, product, customer, rental, limit)
    #pprint.pprint(hp_data.show_available_products(product_table=product))
    #pprint.pprint(hp_data.show_rentals('P00023'))
    hp_data.clear(product, customer, rental)


if __name__ == "__main__":
    print(f'100 Rows', file=open(file_path, "w"))
    run(limit=100)
    print(f'1000 Rows', file=open(file_path, "a"))
    run(limit=1000)
    print(f'10000 Rows', file=open(file_path, "a"))
    run(limit=10000)
    print(f'100000 Rows', file=open(file_path, "a"))
    run(limit=100000)
