"""
    Linear import of lesson05

"""

import logging
import time
import sys
import csv
import threading
from queue import Queue
sys.path.append('../')
from lesson05.database import MongoDBConnection

# File logging setup
LOG_FILE = 'HP.log'
FILE_LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
FILE_FORMATTER = logging.Formatter(FILE_LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE, mode="w")
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FILE_FORMATTER)

# Console logging setup
CONSOLE_LOG_FORMAT = "%(filename)s:%(lineno)-4d %(message)s"
CONSOLE_FORMATTER = logging.Formatter(CONSOLE_LOG_FORMAT)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.ERROR)
CONSOLE_HANDLER.setFormatter(CONSOLE_FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.ERROR)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


def get_file_data(directory_name, file):
    """Extract data from different files"""

    with open(directory_name + '/' + file) as curr_f:
        logging.info('File opened.')
        reader = csv.DictReader(curr_f)
        logging.debug('Created reader to process file.')
        data = []
        for row in reader:
            logging.debug('Adding to data list %s', row)
            data.append(row)
            logging.debug('Data added to list.')
    return data


def insert_data(collection, data):
    """Insert data into mongodb database"""
    error_count = []
    t1 = time.time()
    try:
        print('awaiting insertion into collection: ', collection.name)
        records_before = collection.count_documents({})
        collection.insert_many(data)
        records_after = collection.count_documents({})
        record_int = data.__len__()
        print('File data loaded for collection')
        logging.info('File data loaded.')
    except TypeError as error:  # may need to figure out how to accommodate more errors...
        logging.error('Error %s: ', error)
        error_count.append(error)
        records_before = -1000
        records_after = -1000
        record_int = -1000
    return record_int, records_before, records_after, time.time() - t1, collection.name, error_count


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
     This function takes a directory name three csv files as input, one with product data, one with
    customer data and the third one with rentals data and creates and populates a new MongoDB
    database with these data. It returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a count of any errors
    that occurred, in the same order.

    :return: tuple1, record count of the # of products, customers, rentals added
             tuple2, count of any errors that occurred, in the same order
    """
    logging.info('--------Importing datafiles in %s', directory_name)
    temp_out = []
    output = []
    # Open connection
    logging.info('Opening connection to mongodb.')
    mongo = MongoDBConnection()
    logging.info('Connection open.')

    with mongo:
        # Create connection to database
        logging.info('Attempting to connect to mongodb: HPNortonDatabase in local')
        hp_db = mongo.connection.HPNortonDatabase
        logging.info('Connected HPNortonDatabase.')

        # create/connect to collections
        logging.info('Connecting to collections...')
        product_collection = hp_db['product_data']
        logging.info('*connected to collection: product_data')
        customer_collection = hp_db['customer_data']
        logging.info('*connected to collection: customer_data')
        rental_collection = hp_db['rental_data']
        logging.info('*connected to collection: rental_data')

        # Refactor to use threads
        threads = []
        files = (product_file, customer_file, rentals_file)
        collections = (product_collection, customer_collection, rental_collection)
        for file, collection in zip(files, collections):
            data = get_file_data(directory_name, file)
            records_before = collection.count_documents({})
            records = data.__len__()
            records_after = records_before + records
            threads.append(threading.Thread(target=insert_data, args=(collection, data)))
            temp_out.append([records, records_before, records_after])

        start_time = time.time()
        for thread in threads:
            thread.start()
            thread.join()

    tot_time = time.time() - start_time
    temp_out[0].append(tot_time)
    temp_out[1].append(tot_time)
    logging.info('--------All data import complete.')
    # Outputs

    return (temp_out[0]), (temp_out[1])


if __name__ == '__main__':
    directory_path = 'C:/Users/USer/Documents/UW_Python_Certificate/Course_2/' \
                     'SP_Python220B_2019/students/franjaku/lesson07'
    start = time.time()
    data_files = ['customer_data.csv', 'product_data.csv', 'rental_data.csv']
    output = import_data(directory_path, data_files[0], data_files[1],
                                            data_files[2])
    tottime = time.time() - start
    print('Time to load all data: %s', tottime)
    print(output)
