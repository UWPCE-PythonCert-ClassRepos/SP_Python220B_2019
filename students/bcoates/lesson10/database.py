""" Module to initialize and access MongoDB from CSV files """

import csv
import logging
import time
from pymongo import MongoClient

# Disabling invalid-name due to 'db' varaible name
# pylint: disable=logging-fstring-interpolation, invalid-name, too-many-locals

logging.basicConfig(level=logging.INFO)

class MongoDBConnection():
    """ MongoDB Connection """

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def configure_logging():
    """ Configure logging to timings.txt file """

    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = "timings.txt"
    formatter = logging.Formatter(log_format)
    logger = logging.getLogger()
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

def time_this(func):
    """ Timing decorator """

    def func_with_time(*args, **kwargs):
        """ Calculate time to run given function """

        start_time = time.time()
        func_return = func(*args, **kwargs)
        end_time = time.time()
        func_time = end_time - start_time

        if isinstance(func_return, tuple):
            record_count = 0
            for value in func_return[0]:
                record_count += value
            logging.info(f"{func.__name__} took {func_time:.4} seconds for {record_count} records")
        else:
            logging.info(f"{func.__name__} took {func_time:.4} seconds")

    return func_with_time

@time_this
def import_data(directory_name, product_file, customer_file, rentals_file):
    """ Creates and populates a new MongoDB database from csv files """

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpn

        logging.info("Creating MongoDB Collections...")
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]

        logging.info("Dropping existing Collections...")
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()

        add_list = []
        error_list = []

        for file_path, collection_name in [(f"{directory_name}/{product_file}", products),
                                           (f"{directory_name}/{customer_file}", customers),
                                           (f"{directory_name}/{rentals_file}", rentals)]:

            # Initialize the counter variables
            add_count = 0
            error_count = 0

            # Process each file and count adds and errors
            try:
                logging.info(f"Importing {file_path}")
                with open(file_path) as csv_file:
                    csv_data = csv.DictReader(csv_file)
                    for row in csv_data:
                        try:
                            collection_name.insert_one(row)
                            add_count += 1
                        except MongoClient.OperationFailure:
                            error_count += 1
            except FileNotFoundError:
                logging.error(f"{file_path} does not exist")
                error_count += 1

            # Update the return lists
            add_list.append(add_count)
            error_list.append(error_count)

        # Return tuples
        return tuple(add_list), tuple(error_list)

@time_this
def show_available_products():
    """ Returns a Python dictionary of products listed as available """

    # Initialize return dictionary
    available_products = {}

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpn

        logging.info("Finding available products...")
        for product in db.products.find({"quantity_available": {"$gt": "0"}}):
            available_products[product["product_id"]] = {
                'description': product["description"],
                'product_type': product["product_type"],
                'quantity_available': product["quantity_available"]}

    return available_products

@time_this
def show_rentals(product_id):
    """ Returns a Python dictionary of users that have rented products matching product_id """

    # Initialize return dictionary
    users_who_rented = {}

    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hpn

        logging.info(f"Finding rentals for {product_id}...")
        for rental in db.rentals.find({"product_id": product_id}):
            user_to_find = rental["user_id"]
            logging.info(f"Finding user details for {user_to_find}")
            for user in db.customers.find({"user_id": user_to_find}):
                users_who_rented[user_to_find] = {'name': user["name"],
                                                  'address': user["address"],
                                                  'phone_number': user["phone_number"],
                                                  'email': user["email"]}

    return users_who_rented

if __name__ == '__main__':
    configure_logging()
    import_data("csv_files", "products_1000.csv", "customers_1000.csv", "rentals_1000.csv")
    show_available_products()
    show_rentals("prd001")
    import_data("csv_files", "products_10000.csv", "customers_10000.csv", "rentals_10000.csv")
    show_available_products()
    show_rentals("prd001")
    import_data("csv_files", "products_100000.csv", "customers_100000.csv", "rentals_100000.csv")
    show_available_products()
    show_rentals("prd001")
