"""
Module for testing database.py function.
"""

from unittest import TestCase
import database


class DataBaseTest(TestCase):
    """Testing database module."""

    def setUp(self):
        self.test_product_input = [{'product_id': 'prd001',
                                    'description': '60-inch TV stand',
                                    'product_type': 'livingroom',
                                    'quantity_available': 3},
                                   {'product_id': 'prd002',
                                    'description': 'L-shaped sofa',
                                    'product_type': 'livingroom',
                                    'quantity_available': 1},
                                   {'product_id': 'prd003',
                                    'description': 'Queen size bed frame',
                                    'product_type': 'bedroom',
                                    'quantity_available': 2},
                                   {'product_id': 'prd004',
                                    'description': 'Table with leaves',
                                    'product_type': 'diningroom',
                                    'quantity_available': 1},
                                   {'product_id': 'prd005',
                                    'description': 'Desk',
                                    'product_type': 'den',
                                    'quantity_available': 3},
                                   {'product_id': 'prd006',
                                    'description': 'Desk Light',
                                    'product_type': 'den',
                                    'quantity_available': 4},
                                   {'product_id': 'prd007',
                                    'description': 'Coffee Table',
                                    'product_type': 'livingroom',
                                    'quantity_available': 0},
                                   {'product_id': 'prd008',
                                    'description': 'Throw Pillow',
                                    'product_type': 'livingroom',
                                    'quantity_available': 10}]


    def test_import_csv(self):
        """Test import function."""
        input, count = database.import_csv('data/', 'products.csv')
        self.assertEqual(self.test_product_input, input)
        self.assertEqual(count, 8)

    def test_import_data(self):
        """Test import data function."""
        pass


