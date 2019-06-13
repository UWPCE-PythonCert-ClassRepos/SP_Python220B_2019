"""
Tests for database.py
"""

from unittest import TestCase
import database


class DatabaseTests(TestCase):
    """
    Contains test functions to evaluate basic_operations
    """
    def test_csv_to_dict(self):
        """
        Test csv_to_dict function
        """
        actual_dict = database.csv_to_dict('data/tests.csv')
        expected_dict = [{'product_id': 'prd001',
                          'description': 'microwave',
                          'product_type': 'kitchen'},
                         {'product_id': 'prd002',
                          'description': 'table',
                          'product_type': 'living room'},
                         {'product_id': 'prd003',
                          'description': 'desk',
                          'product_type': 'office'}]

        self.assertEqual(actual_dict, expected_dict)


    def test_import_data(self):
        """
        Test import_data function
        """
        database.drop_db()

        actual_1 = database.import_data('', 'data/products.csv',
                                        'data/customers.csv',
                                        'data/rentals.csv')
        expected_1 = ((8, 5, 9), (0, 0, 0))

        actual_2 = database.import_data('', 'data/products12345.csv',
                                        'data/customers.csv',
                                        'data/rentals.csv')
        expected_2 = ((0, 5, 9), (1, 0, 0))

        actual_3 = database.import_data('', 'data/products.csv',
                                        'data/customers007.csv',
                                        'data/rentals.csv')
        expected_3 = ((8, 0, 9), (0, 1, 0))

        actual_4 = database.import_data('', 'data/products.csv',
                                        'data/customers.csv',
                                        'data/rentals5.csv')
        expected_4 = ((8, 5, 0), (0, 0, 1))

        self.assertEqual(actual_1, expected_1)
        self.assertEqual(actual_2, expected_2)
        self.assertEqual(actual_3, expected_3)
        self.assertEqual(actual_4, expected_4)


    def test_show_available_products(self):
        """
        Test show_available_products function
        """
        database.drop_db()
        database.import_data('', 'data/products.csv',
                             'data/customers.csv',
                             'data/rentals.csv')
        actual = database.show_available_products()
        expected = {'prd001': {'description': '700-W microwave',
                               'product_type': 'kitchen',
                               'quantity_available': '5'},
                    'prd002': {'description': 'coffee table',
                               'product_type': 'living room',
                               'quantity_available': '2'},
                    'prd003': {'description': 'standing desk',
                               'product_type': 'office',
                               'quantity_available': '14'},
                    'prd004': {'description': 'futon',
                               'product_type': 'living room',
                               'quantity_available': '1'},
                    'prd005': {'description': 'office chair',
                               'product_type': 'office',
                               'quantity_available': '2'},
                    'prd006': {'description': 'bar stool',
                               'product_type': 'kitchen',
                               'quantity_available': '13'},
                    'prd007': {'description': 'tv stand',
                               'product_type': 'living room',
                               'quantity_available': '3'}}

        self.assertEqual(actual, expected)


    def test_show_rentals(self):
        """
        Test show_rentals function
        """
        database.drop_db()
        database.import_data('', 'data/products.csv',
                             'data/customers.csv',
                             'data/rentals.csv')
        actual = database.show_rentals('prd001')
        expected = {'user003': {'name': 'Jeff Bezos',
                                'address': '3 Rich Place',
                                'phone_number': '555-557-7131',
                                'email': 'jeff.bezos@amazon.com'}}

        self.assertEqual(actual, expected)


    def test_drop_db(self):
        """
        Test drop_db function
        """
        database.drop_db()
        actual = database.show_available_products()
        expected = {}
        self.assertEqual(actual, expected)
