# Stella Kim
# Assignment 10: Metaprogramming

"""
Migrate product, customer, rentals data from sample CSV files into MongoDB.
Add timing information all functions of the HP application.

"""

import csv
import os
import logging
import types
from datetime import datetime
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
        print('MongoDB__init__:\nHost: {}\nPort: {}'.format(
            self.host, self.port))

    def __enter__(self):
        """Establish connection to MongoDB"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits connection"""
        print('MongoDB__exit__:\nexc_type: {}\nexc_val: {}\nexc_tb: {}'.format(
            exc_type, exc_val, exc_tb))
        self.connection.close()


def timing_decorator(func):
    """
    Write timing data to file: function name, time taken, number of
    records processed
    """
    def timer(*args):
        start_time = datetime.now()
        run_timer = func(*args)
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()

        with open('./timings.txt', 'a', newline='') as file:
            # Check for function type so as to not process function(s)
            if isinstance(run_timer, types.GeneratorType):  # if data_convert()
                pass
            elif not run_timer or run_timer is None:  # if no results
                count = 0
                line = f'Function: {func.__name__:<30} Time(s): '\
                       f'{total_time:<20.8f} Records Processed: '\
                       f'{count:<20}\n'
                file.write(line)
            elif isinstance(run_timer, dict):  # if dictionary
                count = len(run_timer.keys())
                line = f'Function: {func.__name__:<30} Time(s): '\
                       f'{total_time:<20.8f} Records Processed: '\
                       f'{count:<20}\n'
                file.write(line)
            elif isinstance(run_timer, tuple):  # if tuple within tuple
                for i in run_timer:
                    if isinstance(i, tuple) and sum(i) > 1:
                        count = sum(i)
                        line = f'Function: {func.__name__:<30} Time(s): '\
                               f'{total_time:<20.8f} Records Processed: '\
                               f'{count:<20}\n'
                        file.write(line)
        return run_timer
    return timer


class DataTimer(type):
    """Metaclass for timing decorator for all data"""

    def __new__(cls, clsname, bases, clsdict):
        for name, value in clsdict.items():
            if not name.startswith('__'):
                clsdict[name] = timing_decorator(value)  # time decorator
        return super(DataTimer, cls).__new__(cls, clsname, bases, clsdict)


class HPNortonData(metaclass=DataTimer):
    """Class to insert data into database"""

    def import_data(self, directory_name, product_file,
                    customer_file, rentals_file):
        """
        Import data file and return 2 tuples: the first with a record count of
        the number of products, customers and rentals added (in that order);
        the second with a count of any errors that occurred, in the same
        order.
        """
        with MongoDBConnection() as mongo:
            database = mongo.connection.hp_norton
            product_count, product_errors = self.import_csv(
                directory_name, product_file, database)
            LOGGER.debug('%s database successfully created.', product_file)
            customer_count, customer_errors = self.import_csv(
                directory_name, customer_file, database)
            LOGGER.debug('%s database successfully created.', customer_file)
            rentals_count, rentals_errors = self.import_csv(
                directory_name, rentals_file, database)
            LOGGER.debug('%s database successfully created.', rentals_file)

        return ((product_count, customer_count, rentals_count),
                (product_errors, customer_errors, rentals_errors))

    def import_csv(self, directory_name, collection_file, database):
        """Create collection in DB, import CSV to insert into collection"""
        LOGGER.debug('Importing %s CSV file...', collection_file)
        count = 0
        errors = 0
        try:
            filename = f'{collection_file}.csv'
            collection = database[collection_file]
            with open(os.path.join(directory_name, filename)) as file:
                collection.insert_many(self.data_convert(csv.DictReader(file)))
                count = collection.count_documents({})
        except OSError as err:
            print(f'OS error: {err}')
            LOGGER.error('Error reading %s file: %s', collection_file, err)
            errors = 1

        return count, errors

    def data_convert(self, items):
        """Convert quantity_available column in products file to integer"""
        for item in items:
            converted_item = item.copy()
            if 'quantity_available' in item:  # convert columns
                converted_item['quantity_available'] =\
                    int(item['quantity_available'])

            yield converted_item

    def show_available_products(self):
        """Show all available products as a Python dictionary"""
        LOGGER.debug('Listing all available products.')
        available_products = {}
        with MongoDBConnection() as mongo:
            database = mongo.connection.hp_norton
            for product in database.products.find(
                    {'quantity_available': {'$gt': 0}}):
                available_products[product['product_id']] = {
                    'description': product['description'],
                    'product_type': product['product_type'],
                    'quantity_available': product['quantity_available']}
        return available_products

    def show_rentals(self, product_id):
        """Return user information for rented products matching product_id"""
        LOGGER.debug('Listing all rentals for specified product: %s.',
                     product_id)
        rented_products = {}
        with MongoDBConnection() as mongo:
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

    def clear_collections(self, products, customers, rentals):
        """Clear all collections from DB"""
        LOGGER.debug('Clearing all collections from database.')
        with MongoDBConnection() as mongo:
            database = mongo.connection.hp_norton
            database[products].drop()
            database[customers].drop()
            database[rentals].drop()


if __name__ == "__main__":
    RUN = HPNortonData()
    RUN.clear_collections('products', 'customers', 'rentals')
    RUN.import_data('./data', 'products', 'customers', 'rentals')
    RUN.show_available_products()
    RUN.show_rentals('prd0001')
