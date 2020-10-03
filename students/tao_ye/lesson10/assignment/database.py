"""
Use mongoDB for data storage and decorator to record timing information
"""
import csv
import logging
import functools
import time
from pymongo import MongoClient

DATABASE = "norton_furniture"
PRODUCT_COLLECTION = "product"
CUSTOMER_COLLECTION = "customer"
RENTALS_COLLECTION = "rentals"


def setup_logging():
    """ setup logger """
    # Get the "root" logger.
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_file = 'timings.txt'

    log_format = "%(message)s"
    formatter = logging.Formatter(log_format)

    # Create a log message handler that sends output to log_file
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create a log message handler that sends output to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def timer(func):
    """
    Decorator function
    Print the runtime of the decorated function to a logging file
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        logger = logging.getLogger(__name__)
        start_time = time.perf_counter()
        record_processed = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.info(f"Function {func.__name__!r} processed {record_processed} records in "
                    f"{run_time:.4f} secs")
        return record_processed
    return wrapper_timer


class MongoDBConnection():
    """ MongoDB Connection context manager class """

    def __init__(self, host='127.0.0.1', port=27017, handle_error=False):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None
        self.handle_error = handle_error

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        # print('__exit__({}, {}, {})'.format(exc_type, exc_val, exc_tb))
        return self.handle_error


@timer
def import_data(directory_name, product_file, customer_file, rentals_file):
    """ Read data from CSV files and save to MongoDB """
    with MongoDBConnection() as mongo:
        database = mongo.connection[DATABASE]

        product_error_count = 0
        try:
            product_collection = database[PRODUCT_COLLECTION]
            product_count = 0
            with open(directory_name + '/' + product_file, 'r') as csv_file:
                product_reader = csv.DictReader(csv_file)  # return an ordered dictionary
                for row in product_reader:
                    product_collection.insert_one(row)
                    product_count += 1
        except (FileNotFoundError, TypeError):
            product_error_count += 1

        customer_error_count = 0
        try:
            customer_collection = database[CUSTOMER_COLLECTION]
            customer_count = 0
            with open(directory_name + '/' + customer_file, 'r') as csv_file:
                customer_reader = csv.DictReader(csv_file)
                for row in customer_reader:
                    customer_collection.insert_one(row)
                    customer_count += 1
        except (FileNotFoundError, TypeError):
            customer_error_count += 1

        rentals_error_count = 0
        try:
            rentals_collection = database[RENTALS_COLLECTION]
            rentals_count = 0
            with open(directory_name + '/' + rentals_file, 'r') as csv_file:
                rentals_reader = csv.DictReader(csv_file)
                for row in rentals_reader:
                    rentals_collection.insert_one(row)
                    rentals_count += 1
        except (FileNotFoundError, TypeError):
            rentals_error_count += 1

        return product_count + customer_count + rentals_count


@timer
def show_available_products():
    """ Return a dictionary of available products """
    available_product = {}

    if not collection_exist(DATABASE, PRODUCT_COLLECTION):
        return available_product

    with MongoDBConnection() as mongo:
        database = mongo.connection[DATABASE]

        available_product__count = 0
        for product in database[PRODUCT_COLLECTION].find({"quantity_available": {"$ne": '0'}}):
            available_product[product['product_id']] = \
                {'description': product['description'],
                 'product_type': product['product_type'],
                 'quantity_available': product['quantity_available']}
            available_product__count += 1

    return available_product__count


@timer
def show_rentals(product_id):
    """
    Return a dictionary with the information of users that have
    rented products matching product_id
    """
    rentals = {}

    if not collection_exist(DATABASE, RENTALS_COLLECTION) or \
       not collection_exist(DATABASE, CUSTOMER_COLLECTION):
        return rentals

    with MongoDBConnection() as mongo:
        database = mongo.connection[DATABASE]

        rental_count = 0
        for record in database[RENTALS_COLLECTION].find({"product_id": product_id}):
            customer = database[CUSTOMER_COLLECTION].find_one({"user_id": record["user_id"]})
            rentals[customer['user_id']] = {'name': customer['name'],
                                            'address': customer['address'],
                                            'phone_number': customer['phone_number'],
                                            'email': customer['email']}
            rental_count += 1

    return rental_count


def database_exist(database_name):
    """ Check whether a database exists in the MongoDB """
    with MongoDBConnection() as mongo:
        database_list = mongo.connection.list_database_names()

    exist_flag = True
    if database_name not in database_list:
        print(f'Database {database_name} not found.')
        exist_flag = False

    return exist_flag


def collection_exist(database_name, collection_name):
    """ Check whether a collection exists in the MongoDB """
    if not database_exist(database_name):
        return False

    with MongoDBConnection() as mongo:
        collection_list = mongo.connection[database_name].list_collection_names()

    exist_flag = True
    if collection_name not in collection_list:
        print(f'Collection {collection_name} not found.')
        exist_flag = False

    return exist_flag


def drop_database(database_name):
    """ Delete the database from the MongoDB """
    with MongoDBConnection() as mongo:
        mongo.connection.drop_database(database_name)


if __name__ == '__main__':
    setup_logging()
    import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
    show_available_products()
    show_rentals("prd002")
    drop_database(DATABASE)
