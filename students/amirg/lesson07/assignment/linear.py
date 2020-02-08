"""
Class for the linear performance of the import data module
"""
#pylint: disable=invalid-name
#pylint: disable=too-many-locals
import csv
import logging
import time
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

def import_data(directory_name, product_file, customer_file):
    """
    Takes a directory name two csv files on input (product data, customer data) 
    and populates new mongo DB and returns two tuples of record data and time 
    processing data for both files
    """
    logging.debug('Attempting to import file data')
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.HPNorton

        file_list = (product_file, customer_file)
        logging.debug('Successfully obtained file list')
        #record_count = []
        #error_count = []
        products = db['products']
        customers = db['customers']
        #rentals = db['rentals']
        database_list = (products, customers)
        logging.debug('Got database list, going through files now')
        final_list = []
        for filename, database in zip(file_list, database_list):
            #errors = 0
            logging.debug('Attempting to open %s/%s', directory_name, filename)
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
                    final_list.append((record_count, records_before, records_after, run_time))
            except FileNotFoundError:
                logging.error('Could not open file %s', filename)
                #errors += 1
                #record_count.append(None)

            #error_count.append(errors)
        print(final_list)
        return final_list

def drop_data():
    '''Drops the data in mongo'''
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.HPNorton
        db.customers.drop()
        db.products.drop()
