#!/usr/bin/env python
"""
Lesson 10 with UI.

This includes multiprocessing, context managers, metaclasses, and class generation.

Menu option '6' executes the timing run with csv files generated on the fly.
"""
import sys
import os
import csv
import logging
import multiprocessing
import time
import types
from pymongo import MongoClient
from csv_expander import main as expand_main

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger initialized')


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='localhost', port=27017, products_init=False, customers_init=False,
                 rentals_init=False):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.products_init = products_init
        self.customers_init = customers_init
        self.rentals_init = rentals_init
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        self.db = self.connection['products_database']
        if self.products_init is True:
            self.products_collection = self.db['products']
        if self.customers_init is True:
            self.customers_collection = self.db['customers']
        if self.rentals_init is True:
            self.rentals_collection = self.db['rentals']
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class TimingEmbed(type):
    """
    Metaclass for embedding timing within each method of a class.
    """

    def __new__(cls, clsname, bases, attrs):
        """
        Modify a class to have its methods include timing.
        """
        for attr, val in attrs.items():
            if isinstance(val, (types.FunctionType, types.MethodType)):
                attrs[attr] = cls.timing_mod(val)
        return super(TimingEmbed, cls).__new__(cls, clsname, bases, attrs)

    @classmethod
    def timing_mod(cls, method):
        """
        Ingest a method for a timing wrapper.
        """
        def establish_timing(*args, **kwargs):
            """
            Wrap a method with timing commands.
            """
            start_time = time.time()
            result = method(*args, **kwargs)
            finish_time = time.time() - start_time

            LOGGER.info(f'{method.__name__} executed in {finish_time}')
            return result
        return establish_timing


def timing_run(attrs_dict):
    """
    Generate a class for each timing scenario, with corresponding csv's.

    Complete timing runs for each class, and delete each csv.
    """
    number_scenarios = int(input('Please enter the number of desired comprehensive timing '
                                 'scenarios: '
                                 '\n**(Caution, this requires unique csv files for each scenario,'
                                 '\nwith manual entry for number of rows each time)**'
                                 '\n: '))

    db_instantiations = []
    for i in range(number_scenarios):  # Build a list of generated classes with corresponding csv's
        entry_response = expand_main()
        attrs_dict['directory_response'] = os.getcwd() + '/src_data/'
        attrs_dict['product_file'] = 'product_file_{}.csv'.format(entry_response)
        attrs_dict['customer_file'] = 'customer_file_{}.csv'.format(entry_response)
        attrs_dict['rentals_file'] = 'rental_file_{}.csv'.format(entry_response)
        DBFunctions = type('DBFunctions', (TimingEmbed,), attrs_dict)
        db_instantiations.append(DBFunctions('DBFunctions', (TimingEmbed,), attrs_dict))

    for i, db_instantiation in enumerate(db_instantiations):  # Complete timing runs for each class
        LOGGER.info(f'In scenario {i}')
        db_instantiation.clear_data(self=None)
        db_instantiation.import_data(self=None,
                                     directory_name=db_instantiation.directory_response,
                                     product_file=db_instantiation.product_file,
                                     customer_file=db_instantiation.customer_file,
                                     rentals_file=db_instantiation.rentals_file)
        db_instantiation.show_available_products(self=None, suppress_output=True)
        db_instantiation.show_rentals(self=None, product_id='PID0001', suppress_output=True)
        os.remove(db_instantiation.directory_response + db_instantiation.product_file)
        os.remove(db_instantiation.directory_response + db_instantiation.customer_file)
        os.remove(db_instantiation.directory_response + db_instantiation.rentals_file)
        # Delete each resulting csv


def main_menu(attrs_dict):
    """
    Provide the user with an input interface.

    Call functions based on the user's input.
    """
    valid_prompts = ['1', '2', '3', '4', '5', '6', 'q']
    user_prompt = None
    DBFunctions = type('DBFunctions', (object,), attrs_dict)
    db_instantiation = DBFunctions()

    while user_prompt not in valid_prompts:
        print("""Please choose from the following:
              '1' - Print database
              '2' - Load data
              '3' - Clear data
              '4' - Show available products
              '5' - Show rentals
              '6' - Timing run
              'q' - Quit""")
        user_prompt = input(": ")

    if user_prompt == '1':
        db_instantiation.print_database()

    if user_prompt == '2':
        directory_response = input("Please provide the full path to the source files. Include "
                                   "closing '/',\nor press 'enter' to pass the current path with "
                                   "'/src_data/' added.\n: ")
        product_response = input("Please provide the filename of the product file. Include '.csv',"
                                 "\nor press 'enter' to pass 'product_file.csv'\n: ")
        customer_response = input("Please provide the filename of the customer file. Include "
                                  "'.csv',\nor press 'enter' to pass customer_file.csv'\n: ")
        rentals_response = input("Please provide the filename of the rental file. Include '.csv',"
                                 "\nor press 'enter' to pass 'rentals_file.csv'\n: ")

        if directory_response == "":
            directory_name = os.getcwd() + '/src_data/'
        else:
            directory_name = directory_response
        if product_response == "":
            product_file = 'product_file.csv'
        else:
            product_file = product_response
        if customer_response == "":
            customer_file = 'customer_file.csv'
        else:
            customer_file = customer_response
        if rentals_response == "":
            rentals_file = 'rental_file.csv'
        else:
            rentals_file = rentals_response

        db_instantiation.import_data(directory_name, product_file, customer_file, rentals_file)

    if user_prompt == '3':
        db_instantiation.clear_data()

    if user_prompt == '4':
        db_instantiation.show_available_products()

    if user_prompt == '5':
        product_id = input("Please provide the product ID: ")
        db_instantiation.show_rentals(product_id)

    if user_prompt == '6':
        timing_run(attrs_dict)

    if user_prompt == 'q':
        exit_program()


def print_database(self):
    """
    Present the full database.
    """
    with MongoDBConnection(products_init=True, customers_init=True, rentals_init=True) as mongo:
        collections = [mongo.products_collection, mongo.customers_collection,
                       mongo.rentals_collection]

    for collection in collections:
        print(collection)
        for document in collection.find():
            document.pop('_id', None)
            print(document)


def import_data(self, directory_name, product_file, customer_file, rentals_file,
                call_inner=False):
    """
    Populate the new MongoDB database with source data, and return two tuples:

    1: A record count of the number of products, customers, and rentals added (in this order)
    2: A count of any errors that occured, in the same order.
    """
    def write_data(file_path, shared_error_counts, shared_document_counts, bad_file_path, i):
        """
        Helper function to provide a target for multiprocessed writing.
        """
        error_counts = 0

        if i == 0:
            with MongoDBConnection(products_init=True) as mongo:
                collection = mongo.products_collection
        if i == 1:
            with MongoDBConnection(customers_init=True) as mongo:
                collection = mongo.customers_collection
        if i == 2:
            with MongoDBConnection(rentals_init=True) as mongo:
                collection = mongo.rentals_collection

        try:
            with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.reader(csv_file)
                fields = next(csv_reader)
                extracted_data = []
                for row in csv_reader:
                    row_dict = {}
                    for j, field in enumerate(fields):
                        error = False
                        if row[j].strip() == '' and field != 'end_date':
                            error = True
                            break
                        row_dict[field] = row[j]
                    if error is False:
                        extracted_data.append(row_dict)
                    else:
                        error_counts += 1
        except FileNotFoundError as err:
            bad_file_path.append(True)
            print(err)
            LOGGER.info(f'{collection} not added due to FileNotFoundError.')
        else:
            bad_file_path.append(False)
            collection.insert_many(extracted_data)
            LOGGER.info(f'{collection} successfully added.')
            shared_document_counts.append(collection.count_documents({}))
            shared_error_counts.append(error_counts)

    if call_inner:
        return write_data(directory_name + product_file, [], [], [], 0)
    else:
        file_paths = [directory_name + product_file,
                      directory_name + customer_file,
                      directory_name + rentals_file]
        manager = multiprocessing.Manager()
        shared_error_counts = manager.list()
        shared_document_counts = manager.list()
        bad_file_path = manager.list()

        # init = time.process_time()

        for i in range(len(file_paths)):
            proc = multiprocessing.Process(target=write_data, args=(file_paths[i],
                                                                    shared_error_counts,
                                                                    shared_document_counts,
                                                                    bad_file_path, i))
            proc.start()
            proc.join()

        if True in bad_file_path:
            LOGGER.info("\n\nRecommend clearing and reloading database due to unsuccessful "
                        "insertion of collection\n\n")

        print('total rows/documents =', (shared_document_counts[0], shared_document_counts[1],
                                         shared_document_counts[2]), ' ',
              'invalid rows/documents(blank entries aside from end_date) =',
              (shared_error_counts[0], shared_error_counts[1], shared_error_counts[2]))
        return (shared_document_counts[0], shared_document_counts[1],
                shared_document_counts[2]), (shared_error_counts[0], shared_error_counts[1],\
                shared_error_counts[2])


def clear_data(self):
    """
    Clear the database.
    """
    mongo_client = MongoClient('mongodb://localhost:27017')
    mongo_client.drop_database('products_database')
    remaining_databases = mongo_client.list_database_names()
    print('products_database dropped')
    return remaining_databases


def show_available_products(self, suppress_output=False):
    """
    Returns a Python dictionary of products listed as available in the following format:

    {‘prd001’:{‘description’:‘60-inch TV stand’,’product_type’:’livingroom’,
    ’quantity_available’:‘3’},’prd002’:{‘description’:’L-shaped sofa’,’product_type’:’livingroom’,
    ’quantity_available’:‘1’}}
    """
    with MongoDBConnection(products_init=True) as mongo:
        available_products = {}
        for document in mongo.products_collection.find():
            keys, values = [], []
            for key, value in document.items():
                available = True
                if key == 'quantity_available' and value == '0':
                    available = False
                    break
                else:
                    keys.append(key)
                    values.append(value)
            if available:
                available_products[values[1]] = {keys[2]: values[2], keys[3]: values[3],
                                                 keys[4]: values[4], keys[5]: values[5]}

    entries = (" {:^7}|{:^30}|{:^18}|{:^5}|{:^4}".
               format(key, value['description'], value['product_type'],
                      value['quantity_available'], value['daily_rate']) for key, value in
               available_products.items())

    if suppress_output is False:
        print(" {:^7}|{:^30}|{:^18}|{:^5}|{:^4}".format('P_ID', 'DESCRIPTION', 'PRODUCT TYPE',
                                                        'QTY', 'RATE'))
        print('-' * 69)
        for entry in entries:
            print(entry)
    else:
        pass

    return available_products


def show_rentals(self, product_id, suppress_output=False):
    """
    Return a Python dictionary from users that have rented products matching product_id in the
    following format:

    {‘user001’:{‘name’:’Elisa Miles’,’address’:‘4490 Union Street’,’phone_number’:‘206-922-0882’,
    ’email’:’elisa.miles@yahoo.com’},’user002’:{‘name’:’Maya Data’,’address’:‘4936 Elliot Avenue’,
    ’phone_number’:‘206-777-1927’,’email’:’mdata@uw.edu’}}
    """
    with MongoDBConnection(customers_init=True, rentals_init=True) as mongo:
        users_of_product = {}
        for rental in mongo.rentals_collection.find({'product_id': product_id}):
            query = {'user_id': rental['user_id']}
            for document in mongo.customers_collection.find(query):
                keys, values = [], []
                for key, value in document.items():
                    keys.append(key)
                    values.append(value)
                users_of_product[values[1]] = {keys[2]: values[2], keys[3]: values[3],
                                               keys[4]: values[4], keys[5]: values[5]}

    entries = (" {:^7}|{:^30}|{:^50}|{:^12}|{:^25}".
               format(key, value['name'], value['address'],
                      value['phone_number'], value['email']) for key, value in
               users_of_product.items())

    if suppress_output is False:
        print(" {:^7}|{:^30}|{:^50}|{:^12}|{:^25}".format('usrID', 'NAME', 'ADDRESS', 'PHONE',
                                                          'EMAIL'))
        print('-' * 129)
        for entry in entries:
            print(entry)
    else:
        pass

    return users_of_product


def exit_program():
    """
    Close the database and exit the program.
    """
    sys.exit()


if __name__ == "__main__":
    ATTRS_DICT = {'print_database': print_database, 'import_data': import_data,
                  'clear_data': clear_data, 'show_available_products': show_available_products,
                  'show_rentals': show_rentals}
    while True:
        main_menu(ATTRS_DICT)
        print(" \n")
