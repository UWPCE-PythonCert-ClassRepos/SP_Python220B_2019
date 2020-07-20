# pylint: disable=invalid-name, too-many-locals
"""
Database abstraction functions
"""
import csv
import time
from pymongo import MongoClient


def perf_timer(func):
    """Decorator for timing function calls"""
    def wrapper(*args, **kwargs):
        # get starting time
        start_time = time.perf_counter()

        # run function and catch output
        output = func(*args, **kwargs)

        # get ending time and diff
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Function '{func.__name__}' ran in {run_time} seconds")

        return output
    return wrapper


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host="127.0.0.1", port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


@perf_timer
def import_data(directory_name, product_file, customer_file, rentals_file):
    """Import data into the database"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.test_database
        products = db['products']
        customers = db['customers']
        rentals = db['rentals']

        # variables for tracking count
        goodcount = [0, 0, 0]
        badcount = [0, 0, 0]

        # files to iterate over
        files = [
            {'table': products, 'filename': product_file},
            {'table': customers, 'filename': customer_file},
            {'table': rentals, 'filename': rentals_file}
        ]

        for idx, filedata in enumerate(files):
            try:
                with open(f"{directory_name}/{filedata['filename']}") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # this is very naive and will not enforce schema
                        filedata['table'].insert_one(row)
                        goodcount[idx] += 1
            except IOError:
                badcount[idx] += 1

        # return count
        return tuple(goodcount), tuple(badcount)


@perf_timer
def show_available_products():
    """Return dictionary of available products"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.test_database
        products = db['products']
        outdata = {}

        for rawproduct in products.find({'quantity_available': {'$gt': "0"}}):
            outdata[rawproduct['product_id']] = {
                'description': rawproduct['description'],
                'product_type': rawproduct['product_type'],
                'quantity_available': int(rawproduct['quantity_available'])
            }

        return outdata


@perf_timer
def show_rentals(product_id):
    """Return dictionary of users that rented a given product_id"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.test_database
        rentals = db['rentals']
        customers = db['customers']
        outdata = {}

        for rawrental in rentals.find({'product_id': product_id}):
            rawcustomer = customers.find_one(
                {'customer_id': rawrental['customer_id']})
            outdata[rawcustomer['customer_id']] = {
                'name': rawcustomer['name'],
                'address': rawcustomer['address'],
                'phone_number': rawcustomer['phone_number'],
                'email': rawcustomer['email']
            }

        return outdata
