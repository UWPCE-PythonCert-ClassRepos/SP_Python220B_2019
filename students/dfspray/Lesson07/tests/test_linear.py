"""
This file will test the methods in database.py for reading and writing to a mongoDB database
"""

import logging
import unittest
from src import linear

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'test_linear.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class TestDatabase(unittest.TestCase):
    """This class will contain all the tests for linear.py"""

    def test_import(self):
        """This method will test import of .csv files to the database"""

        linear.delete_database()

        #Fully successful import
        actual_tuples1 = linear.import_data('csvs', 'product_data.csv', 'customer_data.csv',
                                            'rentals_data.csv')
        expected_tuples1 = ((1, 1, 1), (0, 0, 0))
        self.assertEqual(actual_tuples1, expected_tuples1)
        linear.delete_database()

        #Partially successful import with failed product_data
        actual_tuples2 = linear.import_data('csvs', 'produc_data.csv', 'customer_data.csv',
                                            'rentals_data.csv')
        expected_tuples2 = ((0, 1, 1), (1, 0, 0))
        self.assertEqual(actual_tuples2, expected_tuples2)
        linear.delete_database()

        #Partially successful import with failed customer_data
        actual_tuples3 = linear.import_data('csvs', 'product_data.csv', 'custome_data.csv',
                                            'rentals_data.csv')
        expected_tuples3 = ((1, 0, 1), (0, 1, 0))
        self.assertEqual(actual_tuples3, expected_tuples3)
        linear.delete_database()

        #Partially successful import with failed rentals_data
        actual_tuples4 = linear.import_data('csvs', 'product_data.csv', 'customer_data.csv',
                                            'rental_data.csv')
        expected_tuples4 = ((1, 1, 0), (0, 0, 1))
        self.assertEqual(actual_tuples4, expected_tuples4)
        linear.delete_database()

if __name__ == '__main__':
    unittest.main()
