"""
Module for testing of database.py, HP Norton mongoDB implementation.
"""

from unittest import TestCase
from unittest.mock import patch

from database import (import_data, read_csv, write_many_to_database, show_available_products,
                      show_rentals)
import database
from test_files.expected_lists import customer_list, product_list, rental_list


TEST_DIRECTORY = 'tests/test_files'
TEST_DATABASE = 'test'



class DatabaseTests(TestCase):
    """Database unittest class."""

    def setUp(self):
        """Setup for unit tests."""
        self.product_fields = ('product_id', 'description', 'product_type', 'quantity_available')
        self.customer_fields = ('customer_id', 'name', 'address', 'phone_number', 'email')
        self.rental_fields = ('rental_id', 'product_id', 'customer_id', 'rental_start',
                              'rental_end')

    def tearDown(self):
        """Teardown for unit tests."""

    def test_read_csv(self):
        """Unit test of the read_csv function."""
        result = read_csv('tests/test_files', 'test_products.csv', self.product_fields)
        self.assertListEqual(result, customer_list)


    def test_write_many_to_database(self):
        """Unit test of the write_many_to_database function."""



    @patch('database.DATABASE')
    def test_import_data(self):
        """Unit test of the import_data function."""
        database.DATABASE = TEST_DATABASE
        with patch('read_csv', side_effect=[(product_list, 2),
                                            (customer_list, 1),
                                            (rental_list, 0)]) as mock_read_csv:
            with patch('write_many_do_database', side_effect=[7, 5, 8]) as mock_write_many:
                result_count, result_errors = import_data(TEST_DIRECTORY, 'test_products.csv',
                                                          'test_customers.csv', 'test_rentals.csv')
                mock_write_many.assert_called_with(database.DATABASE, 'rentals', rental_list)
                mock_read_csv.assert_called_with(TEST_DIRECTORY, 'test_rentals.csv',
                                                 self.rental_fields)
        self.assertEqual(result_count, (7, 5, 8))
        self.assertEqual(result_errors, (2, 1, 0))


    def test_shown_available_products(self):
        """Unit test of the show_available_products function"""

    def test_show_rentals(self):
        """Unit test of the show_rentals function"""

    def test_integrated(self):
        """Integrated function testing."""