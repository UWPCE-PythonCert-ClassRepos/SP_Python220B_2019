"""
This file will test the methods in database.py for reading and writing to a mongoDB database
"""

import logging
import unittest
from src import parallel

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'test_parallel.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class TestDatabase(unittest.TestCase):
    """This class will contain all the tests for parallel.py"""

    def test_import(self):
        """This method will test import of .csv files to the database"""

        parallel.delete_database()

        #Fully successful import
        actual_tuples1 = parallel.import_data('csvs', 'product_data.csv', 'customer_data.csv',
                                              'rentals_data.csv')
        expected_tuples1 = ((1000, 0, 1000, actual_tuples1[0][3]),
                            (1000, 0, 1000, actual_tuples1[1][3]))
        self.assertEqual(actual_tuples1, expected_tuples1)
        parallel.delete_database()

        #Partially successful import with failed product_data
        actual_tuples2 = parallel.import_data('csvs', 'produc_data.csv', 'customer_data.csv',
                                              'rentals_data.csv')
        expected_tuples2 = ((0, 0, 0, 0), (1000, 0, 1000, actual_tuples2[1][3]))
        self.assertEqual(actual_tuples2, expected_tuples2)
        parallel.delete_database()

        #Partially successful import with failed customer_data
        actual_tuples3 = parallel.import_data('csvs', 'product_data.csv', 'custome_data.csv',
                                              'rentals_data.csv')
        expected_tuples3 = ((1000, 0, 1000, actual_tuples3[0][3]), (0, 0, 0, 0))
        self.assertEqual(actual_tuples3, expected_tuples3)
        parallel.delete_database()

        main_return = parallel.main()
        actual_main_return = type(main_return[0]), type(main_return[1])
        expected_main_return = float, float
        self.assertEqual(actual_main_return, expected_main_return)

if __name__ == '__main__':
    unittest.main()
