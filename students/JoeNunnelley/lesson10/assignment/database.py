#! /usr/bin/env python3

"""
Lesson 05 : Migrate CSV data to MongoDB and be able to report on it:

This week, you have been assigned to work on a prototype migration of product
data from a sample csv file into MongoDB. You will use the MongoDB API while
exploiting mongo’s ability to allow the Python module, not the database, to
specify the schema for the data to be stored.

You implementation should address the following requirements:

    As a HP Norton customer I want to see a list of all products available
    for rent so that I can make a rental choice.

    As a HP Norton salesperson I want to see a list of all of the different
    products, showing product ID, description, product type and quantity
    available.

    As a HP Norton salesperson I want to see a list of the names and contact
    details (address, phone number and email) of all customers who have rented
    a certain product.
"""
import json
import logging
from os import path
import time
import pandas as pd
from pymongo import MongoClient

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger('console')
TIMING = logging.getLogger('timing')
FH = logging.FileHandler('mongodb.log', 'w+')
FH.setLevel(logging.DEBUG)
TH = logging.FileHandler('timing.txt', 'w')
TH.setLevel(logging.INFO)
FORMATTER = logging.Formatter(FORMAT)
FH.setFormatter(FORMATTER)
TH.setFormatter(FORMATTER)
LOGGER.addHandler(FH)
TIMING.addHandler(TH)


class Timer:
    """ The timer function """
    def __init__(self, func=time.perf_counter):
        """ Initialize the timer object """
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        """ Start the timer """
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        """ Stop the timer """
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None


def records_processed(result):
    """ Get record count from a results tuple """
    if isinstance(result, tuple):
        return sum(result)

    if isinstance(result, int):
        return result

    return 0


def timing(func):
    """ The timing decorate definition """
    def wrapper(*args, **kwargs):
        timer = Timer()
        timer.start()
        result = func(*args, **kwargs)
        timer.stop()
        message = (f"Function={func.__name__},"
                   f"Duration={timer.elapsed},"
                   f"Records={records_processed(result)}")
        TIMING.info(message)
        return result

    return wrapper


class MongoDBConnection():
    """
    Class to make connecting to and acting upon a mongo database a little
    easier
    """
    @timing
    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    @timing
    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    @timing
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


@timing
def drop_database(database_name):
    """ Drop the a database in the mongo db """
    mongo = MongoDBConnection()
    with mongo:
        dblist = mongo.connection.list_database_names()
        if database_name in dblist:
            mongo.connection.drop_database(database_name)
            LOGGER.debug("The database: %s dropped.", database_name)


@timing
def csv_to_json(directory_name, filename):
    """ Load a csv file to a list """
    path_file = directory_name + "/" + filename
    if path.isfile(path_file):
        LOGGER.debug('Loading file: %s', path_file)
        data = pd.read_csv(path_file)
        return json.loads(data.to_json(orient='records'))

    LOGGER.error('Failed to load file: %s', path_file)
    return {}


@timing
def insert_to_mongo(collection_name, collection):
    """ Insert a collection into the Mongo db """
    mongo = MongoDBConnection()
    insertions = 0
    errors = 0

    with mongo:
        database = mongo.connection.hpnorton

        db_collection = database[collection_name]
        for item in collection:
            count = db_collection.find({"ID": item['ID']}).count()
            LOGGER.debug("ID: %s COUNT: %s", item['ID'], count)
            if count == 0:
                LOGGER.debug("Inserting: %s", item)
                db_collection.insert_one(item)
                insertions += 1
            elif count == 1:
                LOGGER.debug("Updating: %s", item)
                db_collection.update_one({"ID": item['ID']}, {"$set": item},
                                         upsert=False)
            else:
                LOGGER.error("Invalid data state. Too many entries for %s",
                             item['ID'])
                errors += 1

        return (insertions, errors)


@timing
def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import the data into mongo from csv files

    This function takes a directory name three csv files as input,
    one with product data, one with customer data and the third one with
    rentals data and creates and populates a new MongoDB database with these
    data.
    It returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a
    count of any errors that occurred, in the same order.
    """

    # load the csv files
    LOGGER.debug("Reading CSV Files")
    products = csv_to_json(directory_name, product_file)
    customers = csv_to_json(directory_name, customer_file)
    rentals = csv_to_json(directory_name, rentals_file)

    LOGGER.debug("Inserting Data Into Mongo")
    product_results = insert_to_mongo('products', products)
    customer_results = insert_to_mongo('customers', customers)
    rental_results = insert_to_mongo('rentals', rentals)

    # return array of tuples
    # [(products_added, customers_added, rentals_added),
    #  (product_errors, customer_errors, rentals_errors)]
    return [(product_results[0], customer_results[0],
             rental_results[0]),
            (product_results[1], customer_results[1],
             rental_results[1])]


@timing
def print_mdb_collection(collection_name):
    """ Generic collection printer """
    for doc in collection_name.find():
        print(doc)


@timing
def print_raw_products():
    """ Print Raw List of Products """
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.hpnorton
        products = database['products']
        print_mdb_collection(products)
        return products.count

    return 0


@timing
def show_available_products():
    """
    Output the available products from the database

    product_id.
    description.
    product_type.
    quantity_available.

    For example:

    {‘prd001’:{‘description’:‘60-inch TV stand’,’product_type’:’livingroom’,
    ’quantity_available’:‘3’},
    ’prd002’:{‘description’:’L-shaped sofa’,’product_type’:’livingroom’,
    ’quantity_available’:‘1’}}
    """
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.hpnorton
        products = database['products']
        dictionary = {}

        for product in products.find():
            value = {'description': product['DESCRIPTION'],
                     'product_type': product['PRODUCT_TYPE'],
                     'quantity_available': product['QUANTITY_AVAILABLE']}
            dictionary[product['ID']] = value

        for item in dictionary.items():
            print(item)

    return len(dictionary)


@timing
def show_rentals(product_id=None):
    """
    Output the rental history for a/all products.

    user_id.
    name.
    address.
    phone_number.
    email.

    For example:

    {‘user001’:{‘name’:’Elisa Miles’,’address’:‘4490 Union Street’,
                ’phone_number’:‘206-922-0882’,’email’:’elisa.miles@yahoo.com’},
    ’user002’:{‘name’:’Maya Data’,’address’:‘4936 Elliot Avenue’,
               ’phone_number’:‘206-777-1927’,’email’:’mdata@uw.edu’}}

    """
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.hpnorton
        customers = database['customers']
        rentals = database['rentals']
        dictionary = {}
        if product_id:
            # special handling
            LOGGER.debug("Finding product_id: %s", product_id)
            _rentals = rentals.find({"PRODUCT_ID": product_id})

            if _rentals is not None:
                LOGGER.debug("Searching for rentals of : '%s'", product_id)
                for rental in _rentals:
                    _customers = customers.find({"ID": rental['CUSTOMER_ID']})
                    for customer in _customers:
                        value = {'name': customer['NAME'],
                                 'address': customer['ADDRESS'],
                                 'phone_number': customer['PHONE_NUMBER'],
                                 'email': customer['EMAIL']}
                        dictionary[customer['ID']] = value

                for item in dictionary.items():
                    print(item)
            else:
                LOGGER.debug("%s not found", product_id)
        else:
            print_mdb_collection(rentals)

    return len(dictionary)


@timing
def show_customers():
    """
    Output all customers
    """
    mongo = MongoDBConnection()

    with mongo:
        database = mongo.connection.hpnorton

        customers = database['customers']
        print_mdb_collection(customers)

    return customers.count


@timing
def main():
    """ The main function for the program """
    import_stats = import_data("./data",
                               'products.csv',
                               'customers.csv',
                               'rentals.csv')
    print("Insertions:\n\tProducts:\t{}\n\tCustomers:\t{}\n\tRentals:\t{}\n"
          .format(import_stats[0][0],
                  import_stats[0][1],
                  import_stats[0][2]))
    print("Errors:\n\tProducts:\t{}\n\tCustomers:\t{}\n\tRentals:\t{}\n"
          .format(import_stats[1][0],
                  import_stats[1][1],
                  import_stats[1][2]))
    print("\nProduct List")
    show_available_products()
    print("\nRaw Product List")
    print_raw_products()
    print("\nCustomer List")
    show_customers()
    print("\nShow Rentals")
    show_rentals(product_id='prd001')
    print("\nShow All Rentals")
    show_rentals()
    print("Done")


if __name__ == "__main__":
    main()
    drop_database('hpnorton')
