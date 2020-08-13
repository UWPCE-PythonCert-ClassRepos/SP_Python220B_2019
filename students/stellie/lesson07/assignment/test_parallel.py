# Stella Kim
# Assignment 7: Concurrency & Async

"""Integration tests for business data import (parallel)"""

from unittest import TestCase
import parallel as main


class ModuleTests(TestCase):
    """Class for testing HP Norton database"""

    def test_import_data(self):
        """Test CSV import and correct database insertion functionality"""
        main.clear_collections()  # clear all collections from database
        result = main.import_data('./data/', 'products',
                                  'customers', 'rentals')

        # Check collection tuple values
        self.assertEqual(result[1], 1000)
        self.assertEqual(result[2], 0)
        self.assertEqual(result[3], 1000)
        self.assertGreater(result[4], 0)

    # def test_failed_import_data(self):
    #     """Test CSV import failure"""
    #     main.clear_collections()  # clear all collections from database
    #     with self.assertRaises(FileNotFoundError):
    #         main.import_data('./data/', 'products', 'customers', 'fail')

    def test_show_available_products(self):
        """Test DB to show all available products as a Python dictionary"""
        function = main.show_available_products()
        product_1 = function['prd0018']['description']
        product_2 = function['prd0244']['product_type']
        product_3 = function['prd0543']['quantity_available']
        product_4 = function['prd0789']['product_type']
        product_5 = function['prd0979']['description']

        self.assertEqual(product_1, 'Olive Office Chair')
        self.assertEqual(product_2, 'Furniture')
        self.assertEqual(product_3, 19)
        self.assertEqual(product_4, 'Appliance')
        self.assertEqual(product_5, 'Fuchsia Rice Cooker')

    def test_show_rentals(self):
        """Test DB to return user info for rentals matching product_id"""
        result = main.show_rentals('prd0488')
        expected = {'user0789': {'name': 'Sandra Huber',
                                 'address': '0233 Anderson Inlet Suite 288',
                                 'phone_number': '3605559616',
                                 'email': 'huber.sandra@example.com'},
                    'user0975': {'name': 'Shane Medina',
                                 'address': '1122 Mullins Pine Suite 297',
                                 'phone_number': '4255555666',
                                 'email': 'medina.shane@example.com'}}
        self.assertEqual(result, expected)
