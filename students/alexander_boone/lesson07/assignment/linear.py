'''Contains funcitons to manipulate Norton Furniture db.'''

import csv
import os
import time
from pymongo import MongoClient

class MongoDBConnection():
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """Initialize MongoDB Database"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data_linear(directory_name, product_file, customer_file, rentals_file):
    '''
    Takes a directory name and three csv files as input, one with product data,
    one with customer data and the third one with rentals data and creates
    and populates a new MongoDB database with these data. Returns 2 tuples:
    the first with a record count of the number of products, customers and
    rentals added (in that order), the second with a count of any errors that
    occurred, in the same order.
    '''
    START = time.time()
    client = MongoDBConnection()

    with client:
        db = client.connection.hp_norton

        # Create/open collections (AKA tables in RDBMS)
        products = db['products']
        customers = db['customers']
        rentals = db['rentals']

        # Assemble file paths
        product_path = os.path.join(directory_name, product_file)
        customer_path = os.path.join(directory_name, customer_file)
        rentals_path = os.path.join(directory_name, rentals_file)

        # Prepare function return counts
        counts = [0, 0, 0]
        error_counts = [0, 0, 0]

        # Load product data into db
        with open(product_path) as prod_file:
            product_reader = csv.reader(prod_file)

            # Iterate over first row to grab product data headers
            product_headers = next(product_reader)

            # Iterate over remaining rows to insert product data
            for row in product_reader:
                try:
                    products.insert_one(
                        {
                            product_headers[0]: row[0],
                            product_headers[1]: row[1],
                            product_headers[2]: row[2],
                            product_headers[3]: row[3]
                        }
                    )
                    counts[0] += 1
                except IndexError:
                    error_counts[0] += 1

        # Load customer data into db
        with open(customer_path) as cust_file:
            customer_reader = csv.reader(cust_file)

            # Iterate over first row to grab customer data headers
            customer_headers = next(customer_reader)

            # Iterate over remaining rows to insert customer data
            for row in customer_reader:
                try:
                    customers.insert_one(
                        {
                            customer_headers[0]: row[0],
                            customer_headers[1]: row[1],
                            customer_headers[2]: row[2],
                            customer_headers[3]: row[3],
                            customer_headers[4]: row[4]
                        }
                    )
                    counts[1] += 1
                except IndexError:
                    error_counts[1] += 1

        # Load rental data into db
        with open(rentals_path) as rent_file:
            rentals_reader = csv.reader(rent_file)

            # Iterate over first row to grab customer data headers
            rentals_headers = next(rentals_reader)

            # Iterate over remaining rows to insert rentals data
            for row in rentals_reader:
                try:
                    rentals.insert_one(
                        {
                            rentals_headers[0]: row[0],
                            rentals_headers[1]: row[1]
                        }
                    )
                    counts[2] += 1
                except IndexError:
                    error_counts[2] += 1
    RUNTIME = time.time() - START

    return tuple(counts), tuple(error_counts), RUNTIME


def show_available_products():
    '''
    Return a Python dictionary with the following user information
    from users that have rented products matching product_id:
    - user_id
    - name
    - address
    - phone number
    - email
    '''
    client = MongoDBConnection()

    with client:
        db = client.connection.hp_norton

        # Create/open collections (AKA tables in RDBMS)
        products = db['products']

        available_products = dict()

        myquery = {"quantity_available": {"$gt": "0"}}
        product_iterator = products.find(myquery)
        for product in product_iterator:
            del product['_id']
            prod_id = product['product_id']
            del product['product_id']
            available_products[prod_id] = product
        return available_products


def show_rentals(product_id):
    '''
    Return a Python dictionary with the following user information
    from users that have rented products matching product_id:
    - user_id
    - name
    - address
    - phone number
    - email
    '''
    client = MongoDBConnection()

    with client:
        db = client.connection.hp_norton

        # Create/open collections (AKA tables in RDBMS)
        customers = db['customers']
        rentals = db['rentals']

        users_dict = dict()

        myquery = {"product_id": product_id}
        rental_iterator = rentals.find(myquery)
        for rental in rental_iterator:
            user_query = {"user_id": rental["user_id"]}
            user = customers.find_one(user_query)
            del user['_id']
            del user['user_id']
            users_dict[rental["user_id"]] = user
    return users_dict
