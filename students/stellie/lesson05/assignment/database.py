# Stella Kim
# Assignment 5: Consuming APIs with NoSQL

"""Migrate product data from a sample CSV file into MongoDB"""

import csv
import os
import logging
from pymongo import MongoClient

# Format logs
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
logging.basicConfig(filename='database.log', filemode='a',
                    format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger()
LOGGER.info('Logger has initiated.')


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """Initiate connection"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Establish connection to MongoDB"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits connection"""
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import data file and return 2 tuples: the first with a record count of
    the number of products, customers and rentals added (in that order);
    the second with a count of any errors that occurred, in the same
    order.
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        product_count, product_errors = import_csv(directory_name,
                                                   product_file, database)
        LOGGER.debug('%s database successfully created.', product_file)
        customer_count, customer_errors = import_csv(directory_name,
                                                     customer_file, database)
        LOGGER.debug('%s database successfully created.', customer_file)
        rentals_count, rentals_errors = import_csv(directory_name,
                                                   rentals_file, database)
        LOGGER.debug('%s database successfully created.', rentals_file)

    return ((product_count, customer_count, rentals_count),
            (product_errors, customer_errors, rentals_errors))


def import_csv(directory_name, collection_file, database):
    """Create collection in DB and import CSV file to insert into collection"""
    LOGGER.debug('Importing %s CSV file...', collection_file)
    count = 0
    errors = 0
    try:
        filename = f'{collection_file}.csv'
        collection = database[collection_file]
        with open(os.path.join(directory_name, filename)) as file:
            collection.insert_many(data_convert(csv.DictReader(file)))
            count = collection.count_documents({})
    except OSError as err:
        print(f'OS error: {err}')
        LOGGER.error('Error reading %s file: %s', collection_file, err)
        errors = 1

    return count, errors


def data_convert(items):
    """Convert quantity available column in products file to integer form"""
    for item in items:
        converted_item = item.copy()
        if 'quantity_available' in item:  # convert columns
            converted_item['quantity_available'] =\
                int(item['quantity_available'])

        yield converted_item


def show_available_products():
    """Show all available products as a Python dictionary"""
    LOGGER.debug('Listing all available products.')
    mongo = MongoDBConnection()
    available_products = {}
    with mongo:
        database = mongo.connection.hp_norton
        for product in database.products.find(
                        {'quantity_available': {'$gt': 0}}):
            available_products[product['product_id']] = {
                'description': product['description'],
                'product_type': product['product_type'],
                'quantity_available': product['quantity_available']}
    return available_products


def show_rentals(product_id):
    """Return user information for rented products matching product_id"""
    LOGGER.debug('Listing all rentals for specified product: %s.', product_id)
    mongo = MongoDBConnection()
    rented_products = {}
    with mongo:
        database = mongo.connection.hp_norton
        for rental in database.rentals.find({'product_id': product_id}):
            for customer in database.customers.find(
                    {'user_id': rental['user_id']}):
                rented_products[customer['user_id']] = {
                    'name': customer['name'],
                    'address': customer['address'],
                    'phone_number': customer['phone_number'],
                    'email': customer['email']}
    return rented_products


def clear_collections():
    """Clear all collections from DB"""
    LOGGER.debug('Clearing all collections from database.')
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        database.products.drop()
        database.customers.drop()
        database.rentals.drop()


if __name__ == "__main__":
    clear_collections()
    import_data('./data/', 'products', 'customers', 'rentals')
