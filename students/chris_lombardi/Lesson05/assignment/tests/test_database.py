import sys
sys.path.append('C:\\Users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\students\\'
                'chris_lombardi\\Lesson05\\assignment')

import unittest
import database
import logging
from pymongo import errors as pyerror


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
PATH = ('C:\\users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\students\\'
        'chris_lombardi\\Lesson05\\assignment\\')

class test_database(unittest.TestCase):

    def test_import_data(self):
        """Test importing data into the database"""
        # Clear the database
        database.drop_all()

        # Test that file not found error works for all three conditions.
        test_one, test_two = database.import_data(PATH, 'empty_prod.csv',
                                                  'empty_cust.csv', 'empty_rental.csv')
        self.assertEqual(test_one, (0, 0, 0))
        self.assertEqual(test_two, (1, 1, 1))

        # Test that records are successfully added to the database with no errors.
        test_one, test_two = database.import_data(PATH, 'products.csv',
                                                  'customers.csv', 'rentals.csv')
        self.assertEqual(test_one, (5, 10, 10))
        self.assertEqual(test_two, (0, 0, 0))

        # Test DuplicateKeyError raised when importing documents again.
        tup1, tup2 = database.import_data(PATH, 'products.csv', 'customers.csv',
                                          'rentals.csv')
        self.assertEqual(tup2, (5, 10, 10))
        database.drop_all()

    def test_show_available_products(self):
        """Test show_available_products function"""
        # Clear the database
        database.drop_all()
        expected_data = {'prd001': {'description': 'table', 'product_type': 'diningroom',
                         'quantity_available': '2'}, 'prd002': {'description': 'lamp',
                         'product_type': 'office', 'quantity_available': '3'},
                         'prd003': {'description': 'desk', 'product_type': 'office',
                         'quantity_available': '1'}, 'prd005': {'description': 'shovel',
                         'product_type': 'yard', 'quantity_available': '5'}}
        database.import_data(PATH, 'products.csv', 'customers.csv', 'rentals.csv')
        return_dict = database.show_available_products()
        self.assertEqual(expected_data, return_dict)
        database.drop_all()

    def test_show_rentals(self):
        """Test show_rentals function"""
        # Clear the database
        database.drop_all()
        expected_data = {'cust003': {'name': 'Kim', 'address': '2132 Back St',
                         'phone_number': '3432019212', 'email': 'Kim@aol.com'},
                         'cust008': {'name': 'Lisa', 'address': '929 Court Rd',
                         'phone_number': '7474738902', 'email': 'Lisa@aol.com'}}
        database.import_data(PATH, 'products.csv', 'customers.csv', 'rentals.csv')
        return_dict = database.show_rentals('prd001')
        self.assertEqual(expected_data, return_dict)
        database.drop_all()
