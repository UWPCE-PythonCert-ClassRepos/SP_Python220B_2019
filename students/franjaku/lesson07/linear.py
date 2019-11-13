"""
    Linear import of lesson05

"""

import logging
import time
import sys
import csv
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
    count_list = []
    error_list = []
    files = (product_file, customer_file, rentals_file)

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
        product_data = hp_db['product_data']
        logging.info('*connected to collection: product_data')
        customer_data = hp_db['customer_data']
        logging.info('*connected to collection: customer_data')
        rental_data = hp_db['rental_data']
        logging.info('*connected to collection: rental_data')
        collections = (product_data, customer_data, rental_data)

        # load data
        for file, collection in zip(files, collections):
            logging.info('Attempting to open: %s', file)

            # Refactor this to its own function
            with open(directory_name + '/' + file) as curr_f:
                logging.info('File opened.')
                reader = csv.DictReader(curr_f)
                logging.debug('Created reader to process file.')
                data = []
                for row in reader:
                    logging.debug('Adding to data list %s', row)
                    data.append(row)
                    logging.debug('Data added to list.')

            # Refactor this to its own function
            try:
                print('awaiting insertion into collection: %s', file)
                t1 = time.time()
                collection.insert_many(data)
                print(time.time()-t1)
                count_list.append(data.__len__())
                print('File data loaded for collection: %s', file)
                logging.info('File data loaded.')
            except TypeError as error: # may need to figure out how to accommodate more errors...
                logging.error('Error %s: ', error)
                error_list.append(error)

    logging.info('--------All data import complete.')
    # Outputs
    tuple1 = tuple(count_list)
    tuple2 = tuple(error_list)

    return tuple1, tuple2


if __name__ == '__main__':
    directory_path = 'C:/Users/USer/Documents/UW_Python_Certificate/Course_2/' \
                     'SP_Python220B_2019/students/franjaku/lesson07'
    start = time.time()
    _, __ = import_data(directory_path, 'product_data.csv', 'customer_data.csv', 'rental_data.csv')
    tottime = time.time() - start
    print('Time: %s', tottime)
