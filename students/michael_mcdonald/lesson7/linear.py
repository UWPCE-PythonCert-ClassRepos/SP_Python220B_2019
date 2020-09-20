"""
Each module will return a list of tuples,
    one tuple for customer and
    one for products.
Each tuple will contain 4 values:
    the number of records processed (int),
    the record count in the database prior to running (int),
    the record count after running (int), and
    the time taken to run the module (float).
"""

# pylint: disable=E1111
# pylint: disable=import-error
# pylint: disable=W0614
# pylint: disable-msg=R0913
# pylint: disable-msg=too-many-locals
# pylint: disable-msg=too-many-statements
import sys
import os
import csv
import logging
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure

# set up logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
file_handler = logging.FileHandler('main_lesson_7.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class MongoDBConnection:
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """define host and port for the connection"""

        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        try:
            self.connection = MongoClient(self.host, self.port)
            logger.info('connection successful')
            return self
        except ConnectionFailure as e:
            logger.error('mongo connection error %s', e, exc_info=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def timeit_data_import(norton_db_inserts):
    """ time import of customer data in linear returns tuple"""

    mongo = MongoDBConnection()
    counter = 0
    customer_tuple = ()
    products_tuple = ()
    for table, file in norton_db_inserts.items():
        try:
            current_dir = os.getcwd()
            directory_name = current_dir + '\\' + 'data' + '\\'
            tmp_file = directory_name + file
            with mongo:
                if mongo is None:
                    return 'connection not found'
                try:
                    tmp_csv_file = open(tmp_file, 'r')
                    tmp_reader = csv.DictReader(tmp_csv_file)
                except FileNotFoundError:
                    error_result = 'file import error: {} not found'.format(tmp_file)
                    counter += 1
                    return error_result
                norton_db = mongo.connection.NortonDB
                try:
                    header = []
                    prior_record_cnt = norton_db[table].count_documents({})
                    if table == 'customers':
                        processing_time = 0
                        header = ['user_id', 'name', 'address', 'phone_number',
                                  'email']
                        t1_start = time.perf_counter()
                        for each in tmp_reader:
                            row = {}
                            for field in header:
                                row[field] = each[field]
                            norton_db[table].insert_one(row)
                        t1_stop = time.perf_counter()
                        elapsed_time = t1_stop - t1_start
                        processing_time += elapsed_time
                        post_record_cnt = norton_db[table].count_documents({})
                        processed_record_cnt = post_record_cnt - prior_record_cnt
                        customer_tuple = (processed_record_cnt, prior_record_cnt,
                                          post_record_cnt, processing_time)
                    elif table == 'products':
                        header = ['product_id', 'description', 'product_type',
                                  'quantity_available']
                        processing_time = 0
                        t1_start = time.perf_counter()
                        for each in tmp_reader:
                            row = {}
                            for field in header:
                                row[field] = each[field]
                            norton_db[table].insert_one(row)
                        t1_stop = time.perf_counter()
                        elapsed_time = t1_stop - t1_start
                        processing_time += elapsed_time
                        post_record_cnt = norton_db[table].count_documents({})
                        processed_record_cnt = post_record_cnt - prior_record_cnt
                        products_tuple = (processed_record_cnt, prior_record_cnt,
                                          post_record_cnt, processing_time)
                except OperationFailure as e:
                    logger.error('mongo import error %s', e, exc_info=True)
                    counter += 1
        except FileNotFoundError as e:
            logger.error('exception %s', e, exc_info=True)
            print('exception {}'.format(e))
        results = [customer_tuple, products_tuple]
    return results


def timeit_data_import_handler():
    """analyze function with timeit"""
    file_name_dict = {'products': 'products.csv',
                      'customers': 'customers.csv'}
    results = timeit_data_import(file_name_dict)
    counter = 0
    t1_start = time.perf_counter()
    for list_item in results:
        if counter == 0:
            print(f'Prods: processed_record_cnt:{list_item[0]}\t'
                  f'prior_record_cnt:{list_item[1]}\t'
                  f'post_record_cnt:{list_item[2]}\t'
                  f'processing_time:{round(list_item[3], 5)}\t')
        else:
            print(f'Custs: processed_record_cnt:{list_item[0]}\t'
                  f'prior_record_cnt:{list_item[1]}\t'
                  f'post_record_cnt:{list_item[2]}\t'
                  f'processing_time:{round(list_item[3], 5)}\t')
        counter = 1
    t1_stop = time.perf_counter()
    elapsed_time = t1_stop - t1_start
    print(f'total runtime: {elapsed_time}')


def drop_data():
    """drop data"""

    mongo = MongoDBConnection()
    tables = ['customers', 'products']
    if mongo is None:
        return 'connection not found'
    with mongo:
        norton_db = mongo.connection.NortonDB
        try:
            for table in tables:
                drop_table = norton_db[table]
                drop_table.drop()
            result = 'all data dropped- not a good day for you'
        except OperationFailure as e:
            logger.error('mongo drop table error %s', e, exc_info=True)
            result = 'mongo drop table error {}'.format(e)
    return result


def drop_data_handler():
    """call drop_data"""

    results = drop_data()
    print(results)


def exit_program():
    """exit program"""

    sys.exit(1)


def main_menu(user_prompt=None):
    """main menu"""

    valid_prompts = {'1': timeit_data_import_handler,
                     '2': drop_data_handler,
                     'q': exit_program}
    while user_prompt not in valid_prompts:
        print('Please choose from the following options ({options_str}):')
        print('1. Time linear data import')
        print('2. Drop data')
        print('q. Quit')
        user_prompt = input('>')
    return valid_prompts.get(user_prompt)


if __name__ == '__main__':
    while True:
        main_menu()()
        input("Press Enter to continue...........")
