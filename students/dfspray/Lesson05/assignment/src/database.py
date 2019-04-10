"""
This program will read and write data to a mongoDB database
"""

import logging
import csv
from pymongo import MongoClient

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class MongoDBConnection():
    """MongoDB Connection"""
    def __init__(self, host='127.0.0.1', port=27017):
        """Initiates the connection settings"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Connects to MongoDB"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Disconnects from MongoDB"""
        self.connection.close()

def import_data(directory_name, product_file, customer_file, rentals_file):
    """This function takes a directory name and three csv files and creates/populates a new
       MongoDB database with the data. It then returns two tuples: The first contains a record
       count of the number of products, customers and rentals added. The second contains a count
       of any errors that occurred in products, customers, and rentals"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company

        product = database["product"]
        customer = database["customer"]
        rentals = database["rentals"]

        product_error_count = 0
        customer_error_count = 0
        rentals_error_count = 0


        LOGGER.debug("Importing %s", product_file)
        try:
            with open(directory_name+'/'+product_file, newline='') as products_csv:
                product_reader = csv.DictReader(products_csv)
                products_dict = {}
                try:
                    for row in product_reader:
                        products_dict[row['id']] = {'description': row['description'],
                                                    'product_type': row['product_type'],
                                                    'quantity_available': row['quantity_available']
                                                   }
                except Exception as ex:
                    product_error_count += 1
                    LOGGER.warning(ex)
                    LOGGER.warning("Something went wrong while reading product_file")

            LOGGER.debug("I imported: %s", products_dict)
            product.insert_one(products_dict)
            LOGGER.debug("Successfully imported %s", product_file)
        except FileNotFoundError:
            LOGGER.error("could not find %s", product_file)
            product_error_count += 1

        LOGGER.debug("Importing %s", customer_file)

        try:
            with open(directory_name+'/'+customer_file, newline='') as customers_csv:
                customer_reader = csv.DictReader(customers_csv)
                customers_dict = {}
                try:
                    for row in customer_reader:
                        customers_dict[row['id']] = {'name': row['name'],
                                                     'address': row['address'],
                                                     'phone_number': row['phone_number']}
                except Exception as ex:
                    customer_error_count += 1
                    LOGGER.warning(ex)
                    LOGGER.warning("Something went wrong while reading customer_file")
            LOGGER.debug("I imported: %s", customers_dict)
            customer.insert_one(customers_dict)
            LOGGER.debug("Successfully imported %s", customer_file)
        except FileNotFoundError:
            LOGGER.error("could not find %s", customer_file)
            customer_error_count += 1

        LOGGER.debug("Importing %s", rentals_file)

        try:
            with open(directory_name+'/'+rentals_file, newline='') as rentals_csv:
                rentals_reader = csv.DictReader(rentals_csv)
                rentals_dict = {}
                try:
                    for row in rentals_reader:
                        rentals_dict[row['id']] = {'name': row['name'],
                                                   'rentals': row['rentals'].split()}
                except Exception as ex:
                    rentals_error_count += 1
                    LOGGER.warning(ex)
                    LOGGER.warning("Something went wrong while reading rentals_file")

            LOGGER.debug("I imported: %s", rentals_dict)
            rentals.insert_one(rentals_dict)
            LOGGER.debug("Successfully imported %s", rentals_file)
        except FileNotFoundError:
            LOGGER.error("could not find %s", rentals_file)
            rentals_error_count += 1

        tuple1 = (database.product.count_documents({}), database.customer.count_documents({}),
                  database.rentals.count_documents({}))
        tuple2 = (product_error_count, customer_error_count, rentals_error_count)

        return tuple1, tuple2

def show_available_products():
    """Returns a Python dictionary of products listed as available"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        available_products = {}
        LOGGER.debug("Finding all available products...")
        for entry in database.product.find():
            LOGGER.debug('the entry in the product search is: %s', entry)
            for key, value in entry.items():
                if key != '_id':
                    LOGGER.debug('The variable "value" of entry.items() is: %s', value)
                    if value['quantity_available'] != '0':
                        available_products[key] = value
        LOGGER.debug("Search complete")
        return available_products

def show_rentals(product_id):
    """Return a Python dictionary from users that have rented products matching the product_id"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        renters_dict = {}
        LOGGER.debug("Finding rental %s", product_id)
        for entry in database.rentals.find():
            LOGGER.debug('the entry in the rentals search is: %s', entry)
            for key, value in entry.items():
                if key != '_id':
                    LOGGER.debug('The key and value of "entry.items()" are: %s %s', key, value)
                    if product_id in value['rentals']:
                        LOGGER.debug('I matched something for %s!', key)
                        for customer in database.customer.find():
                            LOGGER.debug('I found it in the customers database!')
                            renters_dict[key] = customer[key]
                    else:
                        LOGGER.debug("I didn't match anything for %s", key)

        LOGGER.debug('The returned rentals matched are: %s', renters_dict)
        return renters_dict


def delete_database():
    """This method deletes the database to reset for other tests"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        database.product.drop()
        database.customer.drop()
        database.rentals.drop()
    LOGGER.debug("Cleared database")
