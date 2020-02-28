"""
Methods to allow processing of HP Norton inventory, including:

drop_data() to clear the inventory db
import_data(directory_name, product_file, customer_file, rentals_file) to intake existing CSV's
show_available_products() to show available products, accounting for existing rentals
show_rentals(product_id) to show all active rentals for product_id
"""
import csv
import datetime
import logging
from pathlib import Path
from pymongo import MongoClient

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'

FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(FILE_HANDLER)

class DBConnection():
    """
    Class to instantiate the connection to the Mongo DB.
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """
        Initialize the connection class.
        """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """
        Connect to the DB when entering the context manager.
        """
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the connection when exiting the context manager.
        """
        self.connection.close()

RECORDS_LOC = {'do_import': ('value', 0),
               'show_available_products': ('len',),
               'show_rentals': ('len',)}

def timed_func(func):
    """
    Decorator to time a function call.
    """
    def run_and_time(*args, **kwargs):
        """
        Wrapper function to run the function func and log performance data.
        """
        start_time = datetime.datetime.now()
        ret_val = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        processed_log = ''
        if func.__name__ in RECORDS_LOC:
            if RECORDS_LOC[func.__name__][0] == 'value':
                records = ret_val[RECORDS_LOC[func.__name__][1]]
            elif RECORDS_LOC[func.__name__][0] == 'len':
                records = len(ret_val)

            try:
                processed_log = ', {} records processed'.format(records)
            except NameError:
                pass
        with open('timings.txt', 'a') as file_io:
            timestamp = datetime.datetime.now().isoformat()
            run_duration = (end_time - start_time).total_seconds()
            file_io.write('{} Function {} ran in {} seconds{}\n'.format(timestamp,
                                                                        func.__name__,
                                                                        run_duration,
                                                                        processed_log))
        return ret_val
    return run_and_time

@timed_func
def drop_data():
    """
    Drop the existing data from the database to allow a fresh start.
    """
    mongo = DBConnection()

    with mongo:
        inv_db = mongo.connection.media

        inv_db['products'].drop()
        inv_db['customers'].drop()
        inv_db['rentals'].drop()

        logging.debug('Dropped all databases')

@timed_func
def do_import(file, data_type):
    """
    Function to perform actual CSV import and db insert.

    Pass in file, which should be a Path to the correct file, and data_type, which should be:
    customers, products, or rentals
    """
    analytics = {}
    analytics['starttime'] = datetime.datetime.now()

    with open(file, mode='r') as csv_input:
        import_list = list(csv.DictReader(csv_input))
        logging.debug('Read in %s data from %s: %s', data_type, file.name, import_list)
        analytics['processed'] = len(import_list)

    mongo = DBConnection()

    with mongo:
        inv_db = mongo.connection.media

        analytics['startcount'] = inv_db[data_type].count_documents({})
        import_res = inv_db[data_type].insert_many(import_list)
        if import_res.acknowledged is True:
            logging.debug('Wrote %d records to %s', len(import_res.inserted_ids), data_type)
        else:
            logging.warning('Failed to write records to %s', data_type)

        analytics['endcount'] = inv_db[data_type].count_documents({})

    analytics['runtime'] = (datetime.datetime.now() - analytics['starttime']).total_seconds()
    logging.debug('Database import complete in %d seconds', analytics['runtime'])

    return (analytics['processed'], analytics['startcount'], analytics['endcount'],
            analytics['runtime'])

@timed_func
def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import data from specified CSV's into the database.
    """
    analytics = {}
    analytics['start_time'] = datetime.datetime.now()

    data_directory = Path(directory_name)
    prod_import = do_import(data_directory/product_file, 'products')
    cust_import = do_import(data_directory/customer_file, 'customers')
    do_import(data_directory/rentals_file, 'rentals')

    return (prod_import, cust_import)

@timed_func
def show_available_products():
    """
    Return a dictionary of all available products of the following format:
    {'product_id': {'description': 'description',
                    'product_type': 'product_type',
                    'quantity_available': 'quantity_available*'
                   }
    }
    * NOTE: quantity_available will be the value of the total product quantity less current rentals
    """
    mongo = DBConnection()

    product_list = {}

    with mongo:
        inv_db = mongo.connection.media

        products = inv_db['products']
        rentals = inv_db['rentals']

        for item in products.find():
            logging.debug('Found product %s', item['product_id'])
            query = {'product_id': item['product_id']}
            rented_quantity = rentals.count_documents(query)
            quantity_available = int(item['quantity_available']) - rented_quantity
            for rental in rentals.find(query):
                logging.debug('Rented to %s', rental['user_id'])
            logging.debug('Total rentals: %d', rented_quantity)
            product_list[item['product_id']] = {'description': item['description'],
                                                'product_type': item['product_type'],
                                                'quantity_available': quantity_available}

    return product_list

@timed_func
def show_rentals(product_id):
    """
    Return a dictionary of all renters of product_id in the following format:
    {'user_id': {'name': 'name',
                 'address': 'address',
                 'phone_number': 'phone_number'
                 'email': 'email'
                }
    }
    """
    mongo = DBConnection()

    renter_list = {}

    with mongo:
        inv_db = mongo.connection.media

        rentals = inv_db['rentals']
        customers = inv_db['customers']

        logging.debug('Finding renters for %s', product_id)
        query_1 = {'product_id': product_id}
        for rental in rentals.find(query_1):
            logging.debug('Found renter %s', rental['user_id'])
            query_2 = {'user_id': rental['user_id']}
            for renter in customers.find(query_2):
                renter_list[renter['user_id']] = {'name': renter['name'],
                                                  'address': renter['address'],
                                                  'phone_number': renter['phone_number'],
                                                  'email': renter['email']}
                logging.debug('Renter info: %s', renter_list[renter['user_id']])

        return renter_list
