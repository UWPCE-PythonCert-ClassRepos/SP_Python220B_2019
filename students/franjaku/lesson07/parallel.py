"""
    Linear import of lesson05

"""

import logging
import time
import sys
import csv
import asyncio
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


async def call_insert_many(collection, data):
    return collection.insert_many(data)


async def import_data(directory_name, file, file_type):
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
    files_types = {'product': 'product_data',
                   'customer': 'customer_data',
                   'rental': 'rental_data'}

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
        logging.info('Connecting to collection...')
        collection_data = hp_db[files_types[file_type]]
        logging.info('*connected to collection: product_data')

        # load data
        logging.info('Attempting to open: %s', file)
        with open(directory_name + '/' + file) as curr_f:
            logging.info('File opened.')
            reader = csv.DictReader(curr_f)
            logging.debug('Created reader to process file.')
            data = []
            for row in reader:
                logging.debug('Adding to data list %s', row)
                data.append(row)
                logging.debug('Data added to list.')

        try:
            print('awaiting insertion into collection: %s', files_types[file_type])
            result = await collection_data.insert_many(data)
            # await call_insert_many(collection_data, data)
            count_list.append(data.__len__())
            print('File data loaded for collection: %s', files_types[file_type])
            logging.info('File data loaded.')
        except TypeError as er:  # may need to figure out how to accommodate more errors...
            logging.error('Error %s: ', er)
            error_list.append(er)

    logging.info('--------All data import complete.')
    # Outputs
    tuple1 = tuple(count_list)
    tuple2 = tuple(error_list)

    return tuple1, tuple2, result

if __name__ == '__main__':
    directory_path = 'C:/Users/USer/Documents/UW_Python_Certificate/Course_2/' \
                     'SP_Python220B_2019/students/franjaku/lesson07'
    start = time.time()
    files = ['customer_data.csv', 'product_data.csv', 'rental_data.csv']
    file_types = ['customer', 'product', 'rental']
    loop = asyncio.get_event_loop()
    jobs = asyncio.gather(*(import_data(directory_path, file, file_type) for file, file_type in
                            zip(files, file_types)))
    loop.run_until_complete(jobs)

    tottime = time.time() - start
    print('Time: %s', tottime)
