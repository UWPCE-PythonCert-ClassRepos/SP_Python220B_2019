"""
Module for testing of database.py, HP Norton mongoDB implementation.
"""
# pylint: disable=unused-argument

from unittest import TestCase
from unittest.mock import patch
from copy import deepcopy

from database import (import_data, read_csv, write_many_to_database, show_available_products,
                      show_rentals, MongoDBConnection)
import database
from tests.test_files.expected_lists import (customer_list, product_list, rental_list,
                                             available_products_dict, rental_customers_dict)


TEST_DIRECTORY = 'tests/test_files'
TEST_DATABASE = 'test3'


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
        result_list, result_count = read_csv('tests/test_files', 'test_customers.csv',
                                             self.customer_fields)
        self.assertListEqual(result_list, customer_list)
        self.assertEqual(result_count, 2)

    def test_write_many_to_database(self):
        """Unit test of the write_many_to_database function."""
        entry_count = write_many_to_database(TEST_DATABASE, 'write_test', deepcopy(rental_list))
        self.assertEqual(entry_count, 8)
        result_list = []
        mongo = MongoDBConnection()
        with mongo:
            query = mongo.connection[TEST_DATABASE]['write_test'].find()
            for item in query:
                del item['_id']
                result_list.append(item)
            mongo.connection[TEST_DATABASE]['write_test'].drop()
        self.assertListEqual(result_list, rental_list)

    @patch('database.DATABASE')
    def test_import_data(self, mock_database):
        """Unit test of the import_data function."""
        database.DATABASE = TEST_DATABASE
        with patch('database.read_csv', side_effect=[(product_list, 2),
                                                     (customer_list, 1),
                                                     (rental_list, 0)]) as mock_read_csv:
            with patch('database.write_many_to_database', side_effect=[7, 5, 8]) as mock_write_many:
                result_count, result_errors = import_data(TEST_DIRECTORY, 'test_products.csv',
                                                          'test_customers.csv', 'test_rentals.csv')
                mock_write_many.assert_called_with(database.DATABASE, 'rentals', rental_list)
                mock_read_csv.assert_called_with(TEST_DIRECTORY, 'test_rentals.csv',
                                                 self.rental_fields)
        self.assertEqual(result_count, (7, 5, 8))
        self.assertEqual(result_errors, (2, 1, 0))


class DatabaseIntegratedTests(TestCase):
    """Database unittest class."""

    def setUp(self):
        """Setup for all unit tests"""
        self.product_fields = ('product_id', 'description', 'product_type', 'quantity_available')
        self.customer_fields = ('customer_id', 'name', 'address', 'phone_number', 'email')
        self.rental_fields = ('rental_id', 'product_id', 'customer_id', 'rental_start',
                              'rental_end')
        for item in product_list:
            item['quantity_available'] = int(item['quantity_available'])
        mongo = MongoDBConnection()
        with mongo:
            test_database = mongo.connection[TEST_DATABASE]
            test_database['rentals'].insert_many(deepcopy(rental_list))
            test_database['customers'].insert_many(deepcopy(customer_list))
            test_database['products'].insert_many(deepcopy(product_list))

    def tearDown(self):
        """Teardown of test database."""
        mongo = MongoDBConnection()
        with mongo:
            test_database = mongo.connection[TEST_DATABASE]
            test_database['rentals'].drop()
            test_database['customers'].drop()
            test_database['products'].drop()

    def test_show_available_products(self):
        """Unit test of the show_available_products function"""
        result = show_available_products(TEST_DATABASE)
        self.assertDictEqual(result, available_products_dict)

    def test_show_rentals(self):
        """Unit test of the show_rentals function"""
        result = show_rentals('F-25', TEST_DATABASE)
        self.assertDictEqual(result, rental_customers_dict)


class DatabaseSystemTests(TestCase):
    """Full integrated testing of the database.py functions."""

    @patch('database.DATABASE')
    def test_integrated(self, mock_database):
        """Integrated function testing."""
        database.DATABASE = TEST_DATABASE
        result_count, result_errors = import_data(TEST_DIRECTORY, 'test_products.csv',
                                                  'test_customers.csv', 'test_rentals.csv')
        self.assertEqual(result_count, (7, 5, 8))
        self.assertEqual(result_errors, (0, 2, 1))
        self.assertDictEqual(show_rentals('F-25', TEST_DATABASE), rental_customers_dict)
        self.assertDictEqual(show_available_products(TEST_DATABASE), available_products_dict)
