"""
Module for testing of database.py, HP Norton mongoDB implementation.
"""
# pylint: disable=unused-argument

from unittest import TestCase
from unittest.mock import patch
from copy import deepcopy
from csv import reader
import os

import linear
from linear import import_all_data, read_csv, write_many_to_database, MongoDBConnection
from tests.test_lists import mock_customer_list, mock_rental_list, mock_product_list


TEST_DIRECTORY = 'sample_csv_files'
TEST_DATABASE = 'linear_test'
TEST_CUSTOMERS_FILE = 'customers.csv'
TEST_PRODUCTS_FILE = 'products.csv'
TEST_RENTALS_FILE = 'rentals.csv'

class DatabaseUnitTests(TestCase):
    """Database unittest class."""

    def setUp(self):
        """Setup for all unit tests"""
        self.product_fields = ('product_id', 'description', 'product_type', 'quantity_available')
        self.customer_fields = ('customer_id', 'name', 'address', 'phone_number', 'email')
        self.rental_fields = ('rental_id', 'product_id', 'customer_id', 'rental_start',
                              'rental_end')

    def test_read_csv(self):
        """Unit test of the read_csv function."""
        customer_list = []
        with open(os.path.join(TEST_DIRECTORY, TEST_CUSTOMERS_FILE), newline='') as customer_file:
            for row in reader(customer_file):
                customer_list.append(dict(zip(self.customer_fields, row)))

        result_list, error_count = read_csv(TEST_DIRECTORY, TEST_CUSTOMERS_FILE,
                                            self.customer_fields)
        self.assertListEqual(result_list, customer_list)
        self.assertEqual(error_count, 0)

    def test_write_many_to_database(self):
        """Unit test of the write_many_to_database function."""
        rental_list = []
        with open(os.path.join(TEST_DIRECTORY, TEST_RENTALS_FILE), newline='') as rental_file:
            for row in reader(rental_file):
                rental_list.append(dict(zip(self.rental_fields, row)))
        mongo = MongoDBConnection()
        with mongo:
            mongo.connection[TEST_DATABASE]['write_test'].drop()
        entry_count, init_count = write_many_to_database(TEST_DATABASE, 'write_test',
                                                         deepcopy(rental_list))
        self.assertEqual(entry_count, len(rental_list))
        self.assertEqual(init_count, 0)
        result_list = []
        mongo = MongoDBConnection()
        with mongo:
            query = mongo.connection[TEST_DATABASE]['write_test'].find()
            for item in query:
                del item['_id']
                result_list.append(item)
            mongo.connection[TEST_DATABASE]['write_test'].drop()
        self.assertListEqual(result_list, rental_list)

    @patch('linear.DATABASE')
    def test_import_all_data(self, mock_database):
        """Unit test of the import_all_data function."""
        linear.DATABASE = TEST_DATABASE
        with patch('linear.read_csv', side_effect=[(mock_product_list, 2),
                                                   (mock_customer_list, 1),
                                                   (mock_rental_list, 0)]) as mock_read_csv:
            with patch('linear.write_many_to_database', side_effect=[(7, 2), (5, 1), (8, 15)]) \
                    as mock_write_many:
                result = import_all_data(TEST_DIRECTORY, 'test_products.csv',
                                         'test_customers.csv', 'test_rentals.csv')
                mock_write_many.assert_called_with(linear.DATABASE, 'rentals', mock_rental_list)
                mock_read_csv.assert_called_with(TEST_DIRECTORY, 'test_rentals.csv',
                                                 self.rental_fields)
        self.assertEqual(result[0][:3], (5, 1, 6))
        self.assertEqual(result[1][:3], (7, 2, 9))


class DatabaseSystemTests(TestCase):
    """Full integrated testing of the database.py functions."""

    @patch('linear.DATABASE')
    def test_integrated(self, mock_database):
        """Integrated function testing."""
        mongo = MongoDBConnection()
        with mongo:
            test_database = mongo.connection[TEST_DATABASE]
            test_database['customers'].drop()
            test_database['products'].drop()
            test_database['rentals'].drop()


        linear.DATABASE = TEST_DATABASE
        result = import_all_data(TEST_DIRECTORY, TEST_PRODUCTS_FILE, TEST_CUSTOMERS_FILE,
                                 TEST_RENTALS_FILE)
        expected_result = [(10000, 0, 10000, None), (10000, 0, 10000, None)]
        self.assertEqual(result[0][:3], expected_result[0][:3])
        self.assertEqual(result[1][:3], expected_result[1][:3])
