'''Contains funcitons to manipulate Norton Furniture db.'''

import csv
import os
import time
import functools
import logging
from pymongo import MongoClient

# Set up Logger
logging.basicConfig(filename='timings.txt',
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(message)s')


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


CLIENT = MongoDBConnection()


def timer(func):
    """Log the runtime and count of records process of decorated function."""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = round(end_time - start_time, 5)
        if isinstance(value[0], tuple):
            records_processed = sum([int(val) for val in value[0]])
        else:
            records_processed = value[0]
        logging.info("%s successfully processed %i records in %s seconds",
                     func.__name__, records_processed, str(run_time))
        return value
    return wrapper_timer


@timer
def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    Takes a directory name and three csv files as input, one with product data,
    one with customer data and the third one with rentals data and creates
    and populates a new MongoDB database with these data. Returns 2 tuples:
    the first with a record count of the number of products, customers and
    rentals added (in that order), the second with a count of any errors that
    occurred, in the same order.
    '''

    with CLIENT:

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

    return tuple(counts), tuple(error_counts)


@timer
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

    with CLIENT:

        # Create/open collections (AKA tables in RDBMS)
        products = db['products']

        available_products = dict()
        count = 0

        myquery = {"quantity_available": {"$gt": "0"}}
        product_iterator = products.find(myquery)
        for product in product_iterator:
            count += 1
            del product['_id']
            prod_id = product['product_id']
            del product['product_id']
            available_products[prod_id] = product
        return count, available_products


@timer
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

    with CLIENT:

        # Create/open collections (AKA tables in RDBMS)
        customers = db['customers']
        rentals = db['rentals']

        users_dict = dict()
        count = 0

        myquery = {"product_id": product_id}
        rental_iterator = rentals.find(myquery)
        for rental in rental_iterator:
            count += 1
            user_query = {"user_id": rental["user_id"]}
            user = customers.find_one(user_query)
            del user['_id']
            del user['user_id']
            users_dict[rental["user_id"]] = user
    return count, users_dict


if __name__ == '__main__':
    # Remove all Collections from DB
    with CLIENT:
        db = CLIENT.connection.hp_norton
        db['products'].drop()
        db['customers'].drop()
        db['rentals'].drop()

    # Small number of records
    logging.info('--- Small Number of Records ---')
    import_data('testfiles', 'prod_file.csv',
                'cust_file.csv', 'rental_file.csv')
    show_rentals('prd002')
    show_available_products()

    # Remove all Collections from DB
    with CLIENT:
        db = CLIENT.connection.hp_norton
        db['products'].drop()
        db['customers'].drop()
        db['rentals'].drop()

    # Medium number of records
    logging.info('--- Medium Number of Records ---')
    import_data('testfiles', 'prod_file_med.csv',
                'cust_file_med.csv', 'rental_file_med.csv')
    show_rentals('prd002')
    show_available_products()

    # Remove all Collections from DB
    with CLIENT:
        db = CLIENT.connection.hp_norton
        db['products'].drop()
        db['customers'].drop()
        db['rentals'].drop()

    # Large number or records
    logging.info('--- Large Number of Records ---')
    import_data('testfiles', 'prod_file_long.csv',
                'cust_file_long.csv', 'rental_file_long.csv')
    show_rentals('prd001')
    show_available_products()
