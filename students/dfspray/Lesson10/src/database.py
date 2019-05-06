"""
This program imports the data in the csv files linearly
"""

import logging
import csv
import os
import sys
from timeit import timeit as timer
from pymongo import MongoClient
sys.path.append(os.path.join(os.path.dirname(__file__), 'csvs'))

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'database.log'
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

class ImportData():
    """This class contains the methods to import all the .csv info"""

    def __init__(self):
        """Initiates the dictionary items"""
        self.count_dict = {}
        self.count_dict.setdefault('product_errors', 0)
        self.count_dict.setdefault('customer_errors', 0)
        self.count_dict.setdefault('rentals_errors', 0)
        self.count_dict.setdefault('product_count_before', 0)
        self.count_dict.setdefault('product_count_after', 0)
        self.count_dict.setdefault('customer_count_before', 0)
        self.count_dict.setdefault('customer_count_after', 0)
        self.count_dict.setdefault('rentals_count_before', 0)
        self.count_dict.setdefault('rentals_count_after', 0)
        self.count_dict.setdefault('product_time', 0)
        self.count_dict.setdefault('product_time', 0)
        self.count_dict.setdefault('customer_time', 0)

    def import_all(self):
        """Imports everything without timing"""
        self.count_dict['product_time'] = timer(self.product_file_reader,
                                                globals=globals(), number=1)
        self.count_dict['customer_time'] = timer(self.customer_file_reader,
                                                 globals=globals(), number=1)
        self.count_dict['rentals_time'] = timer(self.rentals_file_reader,
                                                globals=globals(), number=1)

    def import_stats(self):
        """This function returns the statistical data on the import"""

        product_tuple = (self.count_dict['product_count_after'] -
                         self.count_dict['product_count_before'],
                         self.count_dict['product_count_before'],
                         self.count_dict['product_count_after'],
                         self.count_dict['product_time'])
        customer_tuple = (self.count_dict['customer_count_after'] -
                          self.count_dict['customer_count_before'],
                          self.count_dict['customer_count_before'],
                          self.count_dict['customer_count_after'],
                          self.count_dict['customer_time'])
        LOGGER.debug("%s, %s", product_tuple, customer_tuple)
        return product_tuple, customer_tuple

    def product_file_reader(self):
        """This method will loop through and read the product_file"""
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.rental_company
            product = database["product"]
            products_dict = {}
            self.count_dict['product_count_before'] = 0
            for entry in database.product.find():
                self.count_dict['product_count_before'] += len(entry)

            try:
                with open(os.path.join(os.path.dirname(__file__), 'csvs', 'product_data.csv'),
                          newline='') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        products_dict[row['id']] = {'description': row['description'],
                                                    'product_type': row['product_type'],
                                                    'quantity_available': row['quantity_available']}
                    product.insert_one(products_dict)
            except FileNotFoundError:
                LOGGER.error("Could not find product_data.csv")

            self.count_dict['product_count_after'] = 0
            for entry in database.product.find():
                self.count_dict['product_count_after'] += len(entry)

    def customer_file_reader(self):
        """This method will loop through and read the product_file"""
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.rental_company
            customer = database["customer"]
            customer_dict = {}
            self.count_dict['customer_count_before'] = 0
            for entry in database.customer.find():
                self.count_dict['customer_count_before'] += len(entry)

            try:
                with open(os.path.join(os.path.dirname(__file__), 'csvs', 'customer_data.csv'),
                          newline='') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        customer_dict[row['id']] = {'name': row['name'], 'address': row['address'],
                                                    'phone_number': row['phone_number']}
                    customer.insert_one(customer_dict)
            except FileNotFoundError:
                LOGGER.error("Could not find customer_data.csv")

            self.count_dict['customer_count_after'] = 0
            for entry in database.customer.find():
                self.count_dict['customer_count_after'] += len(entry)

    def rentals_file_reader(self):
        """This method will loop through and read the product_file"""
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.rental_company
            rentals = database["rentals"]
            rentals_dict = {}

            self.count_dict['rentals_count_before'] = 0
            for entry in database.rentals.find():
                self.count_dict['rentals_count_before'] += len(entry)

            try:
                with open(os.path.join(os.path.dirname(__file__), 'csvs', 'rentals_data.csv'),
                          newline='') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        rentals_dict[row['id']] = {'name': row['name'],
                                                   'rentals': row['rentals'].split()}
                    rentals.insert_one(rentals_dict)
            except FileNotFoundError:
                LOGGER.error("Could not find rentals_data.csv")

            self.count_dict['rentals_count_after'] = 0
            for entry in database.rentals.find():
                self.count_dict['rentals_count_after'] += len(entry)

def delete_database():
    """This function deletes the database to reset for other tests"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.rental_company
        database.product.drop()
        database.customer.drop()
        database.rentals.drop()
    LOGGER.debug("Cleared database")

def unobstructive_timing_method(self):
    """This method will not be a part of the ImportData class, but will return timing data
       on the imports"""
    timing_info = []

    import_all_time = timer(self.import_all, globals=globals(), number=1)
    import_all_count = (self.count_dict['product_count_after'] +
                        self.count_dict['customer_count_after'] +
                        self.count_dict['rentals_count_after'] -
                        self.count_dict['product_count_before'] -
                        self.count_dict['customer_count_before'] -
                        self.count_dict['rentals_count_before'])
    timing_info.append(['Function: import_all',
                        'Time: {} seconds'.format(import_all_time),
                        'Records Processed: {}'.format(import_all_count)])

    import_stats_time = timer(self.import_stats, globals=globals(), number=1)
    timing_info.append(['Function: import_stats',
                        'Time: {} seconds'.format(import_stats_time),
                        'Records Processed: N/A'])

    product_file_reader_time = timer(self.product_file_reader, globals=globals(), number=1)
    product_file_reader_count = (self.count_dict['product_count_after'] -
                                 self.count_dict['product_count_before'])
    timing_info.append(['Function: product_file_reader',
                        'Time: {} seconds'.format(product_file_reader_time),
                        'Records Processed: {}'.format(product_file_reader_count)])

    customer_file_reader_time = timer(self.customer_file_reader, globals=globals(), number=1)
    customer_file_reader_count = (self.count_dict['customer_count_after'] -
                                  self.count_dict['customer_count_before'])
    timing_info.append(['Function: customer_file_reader',
                        'Time: {} seconds'.format(customer_file_reader_time),
                        'Records Processed: {}'.format(customer_file_reader_count)])

    rentals_file_reader_time = timer(self.rentals_file_reader, globals=globals(), number=1)
    rentals_file_reader_count = (self.count_dict['rentals_count_after'] -
                                 self.count_dict['rentals_count_before'])
    timing_info.append(['Function: rentals_file_reader',
                        'Time: {} seconds'.format(rentals_file_reader_time),
                        'Records Processed: {}'.format(rentals_file_reader_count)])

    delete_database_time = timer(delete_database, globals=globals(), number=1)
    timing_info.append(['Function: delete_database',
                        'Time: {} seconds'.format(delete_database_time),
                        'Records Processed: N/A'])

    with open(os.path.join(os.path.dirname(__file__), 'timings.txt'), 'a') as timings:
        timings.write("Results:\n")
        for item in timing_info:
            timings.write("{}\n".format(", ".join(item)))
        timings.write("\n")

    return timing_info

if __name__ == '__main__':
    setattr(ImportData, "unobstructive_timing_method", unobstructive_timing_method)
    INSTANCE1 = ImportData()
    INSTANCE1.unobstructive_timing_method()
