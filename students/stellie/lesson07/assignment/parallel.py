# Stella Kim
# Assignment 7: Concurrency & Async

"""
Migrate product, customer, rentals data from sample CSV files into MongoDB
"""

import csv
import os
import logging
import threading
from datetime import datetime
from timeit import timeit as timer
from pymongo import MongoClient

# Set up and format logging
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
    Import data file and return 2 tuples, one for customer and one for
    products.  Each tuple will contain 4 values:
    - the number of records processed (int)
    - the record count in the database prior to running (int)
    - the record count after running (int)
    - the time taken to run the module (float)
    """
    mongo = MongoDBConnection()
    threads = []
    results = {}

    def threaded_worker(directory_name, collection_file, database):
        output = import_csv(directory_name, collection_file, database)
        results[output[0]] = output[1:]

    with mongo:
        database = mongo.connection.hp_norton
        customers_thread = threading.Thread(
            target=threaded_worker, args=(directory_name, customer_file, database))
        customers_thread.start()
        threads.append(customers_thread)
        products_thread = threading.Thread(
            target=threaded_worker, args=(directory_name, product_file, database))
        products_thread.start()
        threads.append(products_thread)
        rentals_thread = threading.Thread(
            target=threaded_worker, args=(directory_name, rentals_file, database))
        rentals_thread.start()
        threads.append(rentals_thread)

        for thread in threads:
            thread.join()

        LOGGER.debug('%s, %s, %s databases successfully created.',
                     customer_file, product_file, rentals_file)

    print(results)
    # return results


def import_csv(directory_name, collection_file, database):
    """Create collection in DB and import CSV file to insert into collection"""
    LOGGER.debug('Importing %s CSV file...', collection_file)
    start_time = datetime.now()

    try:
        filename = f'{collection_file}.csv'
        collection = database[collection_file]
        initial_count = collection.count_documents({})
        with open(os.path.join(directory_name, filename)) as file:
            rec_processed = collection.insert_many(
                data_convert(csv.DictReader(file)))
            rec_processed = len(rec_processed.inserted_ids)
        final_count = collection.count_documents({})
    except OSError as err:
        print(f'OS error: {err}')
        LOGGER.error('Error reading %s file: %s', collection_file, err)

    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()

    return (collection_file, rec_processed, initial_count,
            final_count, total_time)


def data_convert(items):
    """Convert quantity_available column in products file to integer form"""
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
    """Clear all collections from DB and dropping DB"""
    LOGGER.debug('Clearing all collections and database.')
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        database.products.drop()
        database.customers.drop()
        database.rentals.drop()
        # database.dropDatabase()


def _code_timer():
    """Measure time it takes to run code"""
    print(timer("import_data('./data/', 'products', 'customers', 'rentals')",
                globals=globals(), number=1))


if __name__ == "__main__":
    clear_collections()
    import_data('./data/', 'products', 'customers', 'rentals')
    # _code_timer()
