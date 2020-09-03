"""
    Test module for Mongo database using unittest package
"""
import logging
from unittest import TestCase
import time
from linear import import_data, drop_database
from parallel import import_data_parallel
from parallel_contention_example import import_data_parallel_contention

DATABASE = "norton_furniture"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a logging "formatter"
LOG_FORMAT = "%(filename)-8s:%(lineno)-3d %(message)s"
formatter = logging.Formatter(LOG_FORMAT)

# Create a log message handler that sends output to log_file
file_handler = logging.FileHandler('test.log', mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ImportTests(TestCase):
    """ unittest class to define all tests for linear import function """
    def setUp(self):
        """ setup tests """
        self.data_folder = 'data'
        self.product_file = 'products.csv'
        self.customer_file = 'customers.csv'
        self.rental_file = 'rentals.csv'

    def tearDown(self):
        """ empty database after each test """
        drop_database(DATABASE)

    def test_import_data(self):
        """ test import_data """
        logger.info('Test Linear import...')
        start = time.perf_counter()
        result = import_data(self.data_folder, self.product_file, self.customer_file,
                             self.rental_file)
        end = time.perf_counter()
        logger.info(f'Linear import takes {end-start} seconds in total.')
        logger.info(f"Customer tuple: {result[0]} ")
        logger.info(f"Product tuple: {result[1]} ")

        self.assertEqual(result[0][0], 1000)
        self.assertEqual(result[0][1], 0)
        self.assertEqual(result[0][2], 1000)
        self.assertEqual(result[1][0], 1000)
        self.assertEqual(result[1][1], 0)
        self.assertEqual(result[1][2], 1000)

    def test_import_data_parallel(self):
        """ test import_data_parallel"""
        logger.info('')
        logger.info('Test concurrent import...')
        start = time.perf_counter()
        result = import_data_parallel(self.data_folder, self.product_file,
                                      self.customer_file, self.rental_file)
        end = time.perf_counter()
        logger.info(f'Concurrent import takes {end-start} seconds in total.')
        logger.info(f"Customer tuple: {result[0]} ")
        logger.info(f"Product tuple: {result[1]} ")

    def test_import_data_parallel_contention(self):
        """ test import_data_parallel_contention """
        logger.info('')
        logger.info('Test concurrent import with contention ...')
        logger.info('Two threads import the same product CSV file and save to the same collection')
        result = import_data_parallel_contention(self.data_folder, self.product_file)
        logger.info(f"Product tuple from thread 1: {result[0]} ")
        logger.info(f"Product tuple from thread 2: {result[1]} ")

    def test_import_data_exception(self):
        """ test import_data function when exceptions occur"""
        import_data('data', 'product.csv', 'customer.csv', 'rental.csv')
