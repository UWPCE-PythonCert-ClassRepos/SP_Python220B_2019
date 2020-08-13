# Stella Kim
# Assignment 7: Concurrency & Async

"""Integration tests for business data import (linear)"""

from unittest import TestCase
import linear as main


class ModuleTests(TestCase):
    """Class for testing HP Norton database"""

    def test_import_data(self):
        """Test CSV import and correct database insertion functionality"""
        main.clear_collections()  # clear all collections from database
        result = main.import_data('./data/', 'products',
                                  'customers', 'rentals')

        # Check collection tuple values
        self.assertEqual(result[0][1], 1000)
        self.assertEqual(result[0][2], 0)

        self.assertEqual(result[1][0], 'products')
        self.assertEqual(result[1][3], 1000)

        self.assertEqual(result[2][2], 0)
        self.assertGreater(result[2][4], 0)

    def test_failed_import_data(self):
        """Test CSV import failure"""
        main.clear_collections()  # clear all collections from database
        self.assertRaises(FileNotFoundError, main.import_data, './data/',
                          'products', 'customers', 'fail')

    def test_show_available_products(self):
        """Test DB to show all available products as a Python dictionary"""
        function = main.show_available_products()
        product_1 = function['prd0026']['description']
        product_2 = function['prd0280']['product_type']
        product_3 = function['prd0501']['quantity_available']
        product_4 = function['prd0687']['product_type']
        product_5 = function['prd0998']['description']

        self.assertEqual(product_1, 'Teal Vacuum Cleaner')
        self.assertEqual(product_2, 'Furniture')
        self.assertEqual(product_3, 22)
        self.assertEqual(product_4, 'Appliance')
        self.assertEqual(product_5, 'Lime Bookshelf')

    def test_show_rentals(self):
        """Test DB to return user info for rentals matching product_id"""
        result = main.show_rentals('prd0104')
        expected = {'user0113': {'name': 'Joe Horton',
                                 'address': '6090 James Spurs',
                                 'phone_number': '2065559086',
                                 'email': 'horton.joe@example.com'},
                    'user0100': {'name': 'Brittany Wright',
                                 'address': '327 Donna Mountains',
                                 'phone_number': '2065559749',
                                 'email': 'wright.brittany@example.com'}}
        self.assertEqual(result, expected)
