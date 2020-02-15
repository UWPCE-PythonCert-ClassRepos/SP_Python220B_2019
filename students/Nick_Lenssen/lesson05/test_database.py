"""Testing module database"""

import sys
import unittest
import logging
import os
import database
sys.path.append('/Users/nicholaslenssen/Desktop/Python/Py220/SP_Python220B_2019/'
                'students/Nick_Lenssen/lesson04')

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class TestDatabase(unittest.TestCase):
    """Test Class"""
    def test_import_data(self):
        """testing import for three cases, empty, correct, repetitive"""
        database.clear()
        #test that the file not found error works for all three fake files
        test_count, test_errors = database.import_data(os.getcwd(), 'prod_none.csv',
                                                       'cust_none.csv', 'rental_none.csv')
        self.assertEqual(test_count, (0, 0, 0))
        self.assertEqual(test_errors, (1, 1, 1))
        #test the actual files are imported properly without errors
        test_count, test_errors = database.import_data(os.getcwd(), 'products.csv',
                                                       'customers.csv', 'rentals.csv')

        self.assertEqual(test_count, (5, 10, 10))
        self.assertEqual(test_errors, (0, 0, 0))

        #database not cleared and same files are imported, should raise duplicate errors
        #as long as the original file
        test_count, test_errors = database.import_data(os.getcwd(), 'products.csv',
                                                       'customers.csv', 'rentals.csv')

        self.assertEqual(test_errors, (5, 10, 10))
        database.clear()

    def test_show_available_products(self):
        """Test show_available_products"""
        # Clear the database
        database.clear()
        expected_data = {'prd001': {'description': 'table', 'product_type': 'diningroom',
                                    'quantity_available': '2'},
                         'prd002': {'description': 'lamp',
                                    'product_type': 'office', 'quantity_available': '3'},
                         'prd003': {'description': 'desk', 'product_type': 'office',
                                    'quantity_available': '1'},
                         'prd005': {'description': 'shovel',
                                    'product_type': 'yard', 'quantity_available': '5'}}

        database.import_data(os.getcwd(), 'products.csv', 'customers.csv', 'rentals.csv')
        return_dict = database.show_available_products()
        self.assertEqual(expected_data, return_dict)
        database.clear()

    def test_show_rentals(self):
        """Test show_rentals function"""
        # Clear the database
        database.clear()
        expected_data = {'cust003': {'name': 'Kim', 'address': '2132 Back St',
                                     'phone_number': '3432019212', 'email': 'Kim@aol.com'},
                         'cust008': {'name': 'Lisa', 'address': '929 Court Rd',
                                     'phone_number': '7474738902', 'email': 'Lisa@aol.com'}}
        database.import_data(os.getcwd(), 'products.csv', 'customers.csv', 'rentals.csv')
        return_dict = database.show_rentals('prd001')
        self.assertEqual(expected_data, return_dict)
        database.clear()
