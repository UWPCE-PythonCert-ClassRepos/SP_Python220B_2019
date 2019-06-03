#!/usr/bin/env python3
"""
Tests for database.py
"""
from unittest import TestCase
from unittest.mock import patch
import database  # pylint: disable=E0401


TEST_DB_NAMES = ['test_products', 'test_customers', 'test_rentals']


def clear_test_collections():
    with database.MONGO:
        db = database.MONGO.connection.media
        db[TEST_DB_NAMES[0]].drop()
        db[TEST_DB_NAMES[1]].drop()
        db[TEST_DB_NAMES[2]].drop()


class DatabaseUnitTest(TestCase):
    """
    Class for unit tests for basic_operations.py
    """
    def test_import_data(self):
        """
        Test that import_data imports csv into database
        """
        clear_test_collections()
        with patch('database.__set_collection_names', return_value=TEST_DB_NAMES):
            incorrect_names = database.import_data('', 'Products .csv', 'Customers .csv', 'Rentals .csv')
        self.assertEqual([(0, 0, 0), (1, 1, 1)], incorrect_names)
        with patch('database.__set_collection_names', return_value=TEST_DB_NAMES):
            import_data = database.import_data('', 'Products.csv', 'Customers.csv', 'Rentals.csv')
        self.assertEqual([(4, 3, 4), (0, 0, 0)], import_data)
        with patch('database.__set_collection_names', return_value=TEST_DB_NAMES):
            duplicate_data = database.import_data('', 'Products.csv', 'Customers.csv', 'Rentals.csv')
        self.assertEqual([(4, 3, 4), (0, 0, 0)], duplicate_data)
        with database.MONGO:
            db = database.MONGO.connection.media
            self.assertEqual(8, db[TEST_DB_NAMES[0]].count_documents({}))
            self.assertEqual(6, db[TEST_DB_NAMES[1]].count_documents({}))
            self.assertEqual(8, db[TEST_DB_NAMES[2]].count_documents({}))
        clear_test_collections()

    def test_show_available_products(self):
        """
        Tests show_available_products
        """
        clear_test_collections()
        test_products = [
            {'product_id': 'prd0001', 'description': 'Computer keyboard', 'product_type': 'office',
             'quantity_available': '100'},
            {'product_id': 'prd0002', 'description': 'Deluxe office chair', 'product_type': 'office',
             'quantity_available': '50'},
            {'product_id': 'prd0003', 'description': 'Mr. Coffee espresso machine', 'product_type': 'kitchen',
             'quantity_available': '0'}
        ]
        with database.MONGO:
            db = database.MONGO.connection.media
            db[TEST_DB_NAMES[0]].insert_many(test_products)
        with patch('database.__set_collection_names', return_value=TEST_DB_NAMES):
            available_products = database.show_available_products()
        item_1 = {'description': 'Computer keyboard', 'product_type': 'office',
                  'quantity_available': '100'}
        item_2 = {'description': 'Deluxe office chair', 'product_type': 'office',
                  'quantity_available': '50'}
        self.assertEqual(item_1, available_products['prd0001'])
        self.assertEqual(item_2, available_products['prd0002'])
        self.assertEqual(2, len(available_products))

    def test_show_rentals(self):
        """
        Tests show_rentals
        """
        pass
