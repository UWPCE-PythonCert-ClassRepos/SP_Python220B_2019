"""
Class for the parallel performance of the import data module
"""
#pylint: disable=invalid-name
#pylint: disable=too-many-locals
import csv
import logging
import time
import multiprocessing
import multiprocessing.pool
from pymongo import MongoClient

#format for the log
LOG_FORMAT = "%(asctime)s %(filename)s: %(lineno)-3d %(levelname)s %(message)s"

#setup for formatter and log file
FORMATTER = logging.Formatter(LOG_FORMAT)
LOG_FILE = 'db.log'

#setup for file hanlder at error level
FILE_HANDLER = logging.FileHandler(LOG_FILE, mode='w')
FILE_HANDLER.setLevel(30)
FILE_HANDLER.setFormatter(FORMATTER)

#setup for console handler at debug level
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(10)
CONSOLE_HANDLER.setFormatter(FORMATTER)

#setup for logging set at debug level
LOGGER = logging.getLogger()
LOGGER.setLevel(10)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

#dict to convert debug input to log level
LOG_LEVEL = {'0': 51, '1': 40, '2': 30, '3': 10}

class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def insert_data(directory_name, filename, database):
    """Inserts data into database"""
    try:
        with open(directory_name + "/" + filename) as file:
            start = time.time()
            records_before = database.count()
            csv_dict = csv.DictReader(file, delimiter=',')
            logging.debug('Opened csv file %s', file)
            list_data = []
            logging.debug('Lopping through data in csv file')
            for row in csv_dict:
                list_data.append(row)

            logging.debug('Attempting to insert data in database')
            database.insert_many(list_data)
            record_count = len(list_data)
            logging.debug('Successfully added data into database')

            records_after = database.count()
            run_time = time.time() - start
            return (record_count, records_before, records_after, run_time)
    except FileNotFoundError:
        logging.error('Could not open file %s', filename)

def import_data_thread(directory_name, product_file, customer_file):
        """
    Takes a directory name two csv files on input (product data, customer data) 
    and populates new mongo DB and returns two tuples of record data and time 
    processing data for both files (thread processing)
    """
    logging.debug('Attempting to import file data')
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.HPNorton

        file_list = (product_file, customer_file)
        logging.debug('Successfully obtained file list')
        products = db['products']
        customers = db['customers']
        database_list = (products, customers)
        logging.debug('Got database list, going through files now')
        final_list = []
        MP_list = []
        pool = multiprocessing.pool.ThreadPool(processes=2)
        for filename, database in zip(file_list, database_list):
            logging.debug('Attempting to open %s/%s', directory_name, filename)
            MP = pool.apply_async(insert_data,
                                  (directory_name, filename, database))
            MP_list.append(MP)

        list1 = MP_list[0]
        list2 = MP_list[1]
        final_list = [list1.get(), list2.get()]
        print(final_list)
        return final_list



def import_data(directory_name, product_file, customer_file):
    """
    Takes a directory name three csv files on input (product data, customer data, rentals
    data) and populates new mongo DB and returns two tuples (record count of number or products
    customers, rentals added) (second with count of number of errors occured)
    """
    logging.debug('Attempting to import file data')
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.HPNorton

        file_list = (product_file, customer_file)
        logging.debug('Successfully obtained file list')
        products = db['products']
        customers = db['customers']
        database_list = (products, customers)
        logging.debug('Got database list, going through files now')
        final_list = []
        for filename, database in zip(file_list, database_list):
            logging.debug('Attempting to open %s/%s', directory_name, filename)
            final_list.append(insert_data(directory_name, filename, database))
        print(final_list)
        return final_list

def drop_data():
    '''Drops the data in mongo'''
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.HPNorton
        db.customers.drop()
        db.products.drop()
