#!/usr/bin/env python3
"""
Tests for database.py
"""
from unittest import TestCase
from unittest.mock import patch
import database  # pylint: disable=E0401


TEST_DB_NAMES = ['test_products', 'test_customers', 'test_rentals']


class DatabaseUnitTest(TestCase):
    """
    Class for unit tests for basic_operations.py
    """
    def test_import_data(self):
        """
        Test that import_data imports csv into database
        """
        with patch('database.__set_db_names', return_value=TEST_DB_NAMES):
            database.import_data('', 'Products.csv', 'Customers.csv', 'Rentals.csv')
        # Test with an incorrect file name
        with database.MONGO:
            db = database.MONGO.connection.media
            db["test_products"].drop()
            db["test_customers"].drop()
            db["test_rentals"].drop()

    def test_show_available_products(self):
        """
        Tests show_available_products
        """
        pass

    def test_show_rentals(self):
        """
        Tests show_rentals
        """
        pass
