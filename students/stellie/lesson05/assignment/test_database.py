# Stella Kim
# Assignment 5: Consuming APIs with NoSQL

"""Integration tests for business data import"""

from unittest import TestCase
import database as main


class ModuleTests(TestCase):
    """Class for testing HP Norton database"""
    def test_import_data(self):
        """Test CSV import and correct database insertion functionality"""
        main.clear_collections()  # clear all collections from database
        result = main.import_data('./data/', 'products',
                                  'customers', 'rentals')
        self.assertEqual(result, ((9, 4, 9), (0, 0, 0)))

    def test_failed_import_data(self):
        """Test CSV import failure"""
        main.clear_collections()  # clear all collections from database
        result = main.import_data('./data/', 'products', 'customers', 'fail')
        self.assertEqual(result, ((9, 4, 0), (0, 0, 1)))

    def test_show_available_products(self):
        """Test DB to show all available products as a Python dictionary"""
        result = main.show_available_products()
        expected = {'prd001': {'description': 'Hamilton Beach 2-Slice Toaster',
                               'product_type': 'Appliance',
                               'quantity_available': 5},
                    'prd002': {'description': '89" Brown Leather Couch',
                               'product_type': 'Furniture',
                               'quantity_available': 2},
                    'prd003': {'description': 'Ladder Wooden Bookshelf',
                               'product_type': 'Furniture',
                               'quantity_available': 1},
                    'prd004': {'description': 'Cuisinart Countertop Blender',
                               'product_type': 'Appliance',
                               'quantity_available': 5},
                    'prd005': {'description': 'Wooden Swivel Office Chair',
                               'product_type': 'Furniture',
                               'quantity_available': 3},
                    'prd006': {'description': 'Tiger 5.5 Cup Rice Cooker',
                               'product_type': 'Appliance',
                               'quantity_available': 2},
                    'prd008': {'description': '100% Cotton Towel Set',
                               'product_type': 'Supplies',
                               'quantity_available': 10},
                    'prd009': {'description': 'Silicone Utensil Set',
                               'product_type': 'Supplies',
                               'quantity_available': 10}}
        self.assertEqual(result, expected)

    def test_show_rentals(self):
        """Test DB to return user info for rentals matching product_id"""
        result = main.show_rentals('prd001')
        expected = {'user001': {'name': 'John Smith',
                                'address': '123 Main Street',
                                'phone_number': '2065551234',
                                'email': 'smith.john@example.com'},
                    'user003': {'name': 'Alice Wonderland',
                                'address': '200 Cherry Street',
                                'phone_number': '2065551357',
                                'email': 'wonderland.alice@example.com'}}
        self.assertEqual(result, expected)
