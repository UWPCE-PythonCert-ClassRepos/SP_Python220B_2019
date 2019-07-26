"""
Tests for database.py
"""

from unittest import TestCase
import linear


class DatabaseTests(TestCase):
    """
    Contains test functions to evaluate basic_operations
    """
    def test_csv_to_dict(self):
        """
        Test csv_to_dict function
        """
        actual_dict = linear.csv_to_dict('data/products.csv')
        expected_dict_1 = {'product_id': 'prd001',
                           'description': '700-W microwave',
                           'product_type': 'kitchen',
                           'quantity_available': '5'}

        self.assertEqual(actual_dict[0], expected_dict_1)


    def test_import_data(self):
        """
        Test import_data function
        """
        linear.drop_db()

        actual_1_raw = linear.import_data('', 'data/products.csv',
                                          'data/customers.csv',
                                          'data/rentals.csv')
        actual_1 = [actual_1_raw[0][:3], actual_1_raw[1][:3]]

        expected_1 = [(1000, 0, 1000), (1000, 0, 1000)]
        self.assertEqual(actual_1, expected_1)
