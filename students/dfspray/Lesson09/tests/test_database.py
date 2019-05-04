"""
This file will test the methods in database.py for reading and writing to a mongoDB database
"""

import logging
import unittest
from src import database

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'test_database.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

class TestDatabase(unittest.TestCase):
    """This class will contain all the tests for database.py"""

    def test_import(self):
        """This method will test import of .csv files to the database"""

        database.delete_database()

        #Fully successful import
        actual_tuples1 = database.import_data('csvs', 'product_data.csv', 'customer_data.csv',
                                              'rentals_data.csv')
        expected_tuples1 = ((1, 1, 1), (0, 0, 0))
        self.assertEqual(actual_tuples1, expected_tuples1)
        database.delete_database()

        #Partially successful import with failed product_data
        actual_tuples2 = database.import_data('csvs', 'produc_data.csv', 'customer_data.csv',
                                              'rentals_data.csv')
        expected_tuples2 = ((0, 1, 1), (1, 0, 0))
        self.assertEqual(actual_tuples2, expected_tuples2)
        database.delete_database()

        #Partially successful import with failed customer_data
        actual_tuples3 = database.import_data('csvs', 'product_data.csv', 'custome_data.csv',
                                              'rentals_data.csv')
        expected_tuples3 = ((1, 0, 1), (0, 1, 0))
        self.assertEqual(actual_tuples3, expected_tuples3)
        database.delete_database()

        #Partially successful import with failed rentals_data
        actual_tuples4 = database.import_data('csvs', 'product_data.csv', 'customer_data.csv',
                                              'rental_data.csv')
        expected_tuples4 = ((1, 1, 0), (0, 0, 1))
        self.assertEqual(actual_tuples4, expected_tuples4)
        database.delete_database()

    def test_show_available(self):
        """This method tests that all and only available products are displayed"""
        database.import_data('csvs', 'product_data.csv', 'customer_data.csv', 'rentals_data.csv')
        actual_available = database.show_available_products()
        expected_available = {'prd001': {'description': 'TV', 'product_type': 'livingroom',
                                         'quantity_available': '3'},
                              'prd002': {'description': 'Couch', 'product_type': 'livingroom',
                                         'quantity_available': '1'}}
        self.assertEqual(actual_available, expected_available)
        database.delete_database()

        database.import_data('csvs', 'produc_data.csv', 'customer_data.csv', 'rentals_data.csv')
        database.delete_database()

    def test_show_rentals(self):
        """This method tests that the correct customers are displayed for the product_id"""
        database.import_data('csvs', 'product_data.csv', 'customer_data.csv', 'rentals_data.csv')
        actual_customers1 = database.show_rentals('prd002')
        expected_customers1 = {'cst001': {'name': 'Charlie', 'address': '123 Fleet Street',
                                          'phone_number': '1231234123'},
                               'cst002': {'name': 'Andrey', 'address': '123 Jordan Street',
                                          'phone_number': '4564564567'}}
        actual_customers2 = database.show_rentals('prd009')
        expected_customers2 = {}
        self.assertEqual(actual_customers1, expected_customers1)
        self.assertEqual(actual_customers2, expected_customers2)

if __name__ == '__main__':
    unittest.main()
