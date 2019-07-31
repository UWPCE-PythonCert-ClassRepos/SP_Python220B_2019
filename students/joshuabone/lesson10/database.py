"""Functions for using the MongoDB backend for our rentals app."""

import csv
import logging
import time
import types
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

DATABASE = None


class Stopwatch:  # pylint: disable=too-few-public-methods
    """Simple stopwatch for timing events."""
    def __init__(self):
        self.last = time.time_ns()
        self.start = self.last

    def mark(self):
        """Reset the clock time and return (total time, split time)."""
        now = time.time_ns()
        total_diff = (now - self.start) / 1_000_000_000
        split_diff = (now - self.last) / 1_000_000_000
        self.last = now
        return total_diff, split_diff


class MongoDBConnection():
    """MongoDB Connection (copied from assignment example)"""

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


def import_csv_to_mongodb(collection, csv_file_path):
    """Import a single CSV file into MongoDB."""
    with open(csv_file_path) as csv_file:
        result = collection.insert_many(csv.DictReader(csv_file))
        return len(result.inserted_ids)


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import data from multiple CSV files into MongoDB.
    """
    customer = DATABASE['customer']
    product = DATABASE['product']
    rental = DATABASE['rental']

    counts = (
        import_csv_to_mongodb(product, f"{directory_name}/{product_file}"),
        import_csv_to_mongodb(customer, f"{directory_name}/{customer_file}"),
        import_csv_to_mongodb(rental, f"{directory_name}/{rentals_file}")
    )
    return counts


def show_available_products():
    """List all products that have quantity available != 0"""
    products = DATABASE['product'].find({'quantity_available': {'$ne':'0'}})
    products_dict = {prod['product_id']:
                     {'description': prod['description'],
                      'product_type': prod['product_type'],
                      'quantity_available': int(prod['quantity_available'])}
                     for prod in products}
    return products_dict


def show_rentals(product_id):
    """List all customers that have rented a given product id.s"""
    rentals = DATABASE['rental']\
        .find({'product_id': product_id})\
        .sort('customer_id')
    rental_list = [rental['customer_id'] for rental in rentals]
    customers = DATABASE['customer'].find({'customer_id':
                                           {'$in': rental_list}})
    cust_dict = {cust['customer_id']:
                 {'name': f'{cust["first_name"]} {cust["last_name"]}',
                  'address': cust["address"],
                  'phone_number': cust["phone"],
                  'email': cust["email"]}
                 for cust in customers}
    return cust_dict


def drop_data():
    """Drop all data from the currently selected database."""
    DATABASE['product'].drop()
    DATABASE['customer'].drop()
    DATABASE['rental'].drop()


# Unobtrusive way to time our method calls.
# pylint: disable=global-statement
FUNCTION_LOGS = list()


def time_func(func):
    """
    Decorator for a function to store function name, args, and timing info.
    """
    def return_fn(*args, **kwargs):
        global FUNCTION_LOGS
        stopwatch = Stopwatch()
        result = func(*args, **kwargs)
        split = stopwatch.mark()[1]
        FUNCTION_LOGS.append((func.__name__, args, kwargs, split))
        return result

    return return_fn


def process_datasets(size, counts):
    """
    Import datasets, call two methods on the data, and then drop the data. This
    allows profiling the other code in the module to look for bottlenecks.
    """
    global FUNCTION_LOGS
    FUNCTION_LOGS.append((f"-----> Processing size {size}", counts))
    # process small data sets
    counts = import_data('data',
                         f'products_{size}.csv',
                         f'customers_{size}.csv',
                         f'rentals_{size}.csv')
    logging.info('Imported %d products, %d customers, and %d rentals', *counts)

    show_available_products()
    show_rentals('prd0000')

    drop_data()


if __name__ == "__main__":
    # Unobtrusively decorate all functions in current namespace.
    for global_pair in list(globals().items()):
        name, obj = global_pair
        if isinstance(obj, types.FunctionType) and obj is not time_func \
                and obj is not process_datasets:
            globals()[name] = time_func(obj)

    MONGO = MongoDBConnection()

    with MONGO:
        DATABASE = MONGO.connection.rentals

    for sizes in (('small', 1000), ('med', 10_000), ('large', 100_000)):
        process_datasets(*sizes)

    with open('timings.txt', 'w') as log_file:
        for entry in FUNCTION_LOGS:
            if len(entry) == 2:
                log_file.write("-------------------------------------------\n")
                log_file.write(str(entry))
                log_file.write("\n\n")
            else:
                log_file.write("-------------------------------------------\n")
                log_file.write(f"Called function {entry[0]}\n")
                if entry[1]:
                    log_file.write(f"args: {str(entry[1])}\n")
                if entry[2]:
                    log_file.write(f"kwargs: {str(entry[2])}\n")
                log_file.write(f"Call took {entry[3]} seconds in total.\n\n")
