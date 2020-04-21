"""Import and read customers, products and rentals databases from csv."""

# pylint: disable=W1202, W0621, C0103, R0914

import logging
import time
import csv
import os
from pymongo import MongoClient


# Set logging level at info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class MongoDBConnection():
    """Establish MongoDB connection."""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def timer(func):
    """Decorator to calculate and return runtime for wrapped functions."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function_result = func(*args, **kwargs)
        print(f'{func.__name__} runtime: {time.time() - start_time}.')
        return function_result
    return wrapper


@timer
def csv_to_dict(path):
    """Converts data from csv to mongo-readable dict."""

    table_data = []

    # Get csv data and return as dict
    with open(path) as csv_file:
        for row in csv.DictReader(csv_file):
            table_data.append(row)

    logging.info(f"{path} converted from csv to mongo-readable dict.")

    return table_data


@timer
def import_data(directory_name, product_file, customer_file, rentals_file):
    """Import HP Norton csv data to MongoDB."""

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media

        # Create collections
        products = database['products']
        customers = database['customers']
        rentals = database['rentals']

        # Create iterable list for the for loop below
        collections = [{'db': products, 'file_name': product_file, 'order': 0},
                       {'db': customers, 'file_name': customer_file, 'order': 1},
                       {'db': rentals, 'file_name': rentals_file, 'order': 2}]

        record_counts = [0, 0, 0]
        error_counts = [0, 0, 0]

        for collection in collections:
            error_count = 0

            try:
                # Populate collections with csv data
                path = os.path.join(directory_name, collection['file_name'])
                data = csv_to_dict(path)
                collection['db'].insert_many(data)

                logging.info(f"Data from {path} added to database.")

                # Count the number of records in the db
                record_counts[collection['order']] = collection['db'].count_documents({})

            except FileNotFoundError as err:
                logging.error(err)
                error_count += 1

            error_counts[collection['order']] = error_count

        return tuple(record_counts), tuple(error_counts)


@timer
def show_available_products():
    """Return dict listing all available products."""

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media

        logging.info("Retrieving data for all available products.")
        products = database['products'].find({'quantity_available': {'$ne': '0'}})
        products_dict = {}

        logging.info("Building dict of available products.")
        for product in products:
            products_dict[product['product_id']] = {
                'description': product['description'],
                'product_type': product['product_type'],
                'quantity_available': int(product['quantity_available'])}

        logging.info("Build successful. Returning dict.")
        return products_dict


@timer
def show_rentals(product_id):
    """Return dict listing users who have rented the given product."""

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media

        logging.info("Querying rentals db for list of unique renters.")
        renters = database['rentals'].\
                  find({'product_id': product_id}, {'customer_id': 1}).\
                  distinct('customer_id')

        logging.info("Retrieving info for each renter.")
        renter_data = database['customers'].find({'customer_id': {'$in': renters}})

        renters_dict = {}
        for customer in renter_data:
            renters_dict[customer['customer_id']] = {
                'name': f"{customer['first_name']} {customer['last_name']}",
                'address': customer['home_address'],
                'phone': customer['phone_number'],
                'email': customer['email_address']}

        logging.info("Retrieval successful. Returning info for each renter.")
        return renters_dict


def drop_data():
    """Clear data from the database."""

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media

    for name in ['customers', 'products', 'rentals']:
        database[name].drop()

    logging.info("All data has been cleared from the database.")


if __name__ == "__main__":
    drop_data()
    print("Time with 5 product and customer records.")
    import_data('data', 'products_5.csv', 'customers_5.csv', 'rentals.csv')
    show_available_products()
    show_rentals('prod_4')

    drop_data()
    print("Time with 50,000 product and customer records.")
    import_data('data', 'products_50000.csv', 'customers_50000.csv', 'rentals.csv')
    show_available_products()
    show_rentals('prod_4')

    drop_data()
    print("Time with 1,000,000 product and customer records.")
    import_data('data', 'products_1000000.csv', 'customers_1000000.csv', 'rentals.csv')
    show_available_products()
    show_rentals('prod_4')
