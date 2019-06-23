#!/usr/bin/env python3
"""
Tests for linear.py
"""
from unittest import TestCase
from unittest.mock import patch
import linear  # pylint: disable=E0401


TEST_DB_NAMES = ['test_products', 'test_customers', 'test_rentals']


def clear_test_collections():
    """Clears the collections used for testing"""
    with linear.MONGO:
        db = linear.MONGO.connection.media  # pylint: disable=C0103
        db[TEST_DB_NAMES[0]].drop()
        db[TEST_DB_NAMES[1]].drop()
        db[TEST_DB_NAMES[2]].drop()


class DatabaseUnitTest(TestCase):
    """
    Class for unit tests for linear.py
    """
    def test_import_data(self):
        """
        Test that import_data imports csv into database
        """
        clear_test_collections()
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            incorrect_names = linear.import_data('', 'Products .csv', 'Customers .csv',
                                                 'Rentals .csv')
        self.assertEqual([(0, 0, 0), (1, 1, 1)], incorrect_names)
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            import_data = linear.import_data('', 'Products.csv', 'Customers.csv', 'Rentals.csv')
        self.assertEqual([(4, 3, 4), (0, 0, 0)], import_data)
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            duplicate_data = linear.import_data('', 'Products.csv', 'Customers.csv',
                                                'Rentals.csv')
        self.assertEqual([(4, 3, 4), (0, 0, 0)], duplicate_data)
        with linear.MONGO:
            db = linear.MONGO.connection.media  # pylint: disable=C0103
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
            {'product_id': 'prd0002', 'description': 'Deluxe office chair',
             'product_type': 'office', 'quantity_available': '50'},
            {'product_id': 'prd0003', 'description': 'Mr. Coffee espresso machine',
             'product_type': 'kitchen', 'quantity_available': '0'}
        ]
        with linear.MONGO:
            db = linear.MONGO.connection.media  # pylint: disable=C0103
            db[TEST_DB_NAMES[0]].insert_many(test_products)
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            available_products = linear.show_available_products()
        item_1 = {'description': 'Computer keyboard', 'product_type': 'office',
                  'quantity_available': '100'}
        item_2 = {'description': 'Deluxe office chair', 'product_type': 'office',
                  'quantity_available': '50'}
        self.assertEqual(item_1, available_products['prd0001'])
        self.assertEqual(item_2, available_products['prd0002'])
        self.assertEqual(2, len(available_products))
        clear_test_collections()

    def test_show_rentals(self):
        """
        Tests show_rentals
        """
        clear_test_collections()
        test_rentals = [
            {'user_id': 'user0001', 'product_id': 'prd00001'},
            {'user_id': 'user0002', 'product_id': 'prd00001'},
            {'user_id': 'user0001', 'product_id': 'prd00002'},
            {'user_id': 'user0003', 'product_id': 'prd00003'}
        ]
        test_customers = [
            {'user_id': 'user0001', 'name': 'Matt Walker', 'address': '5478 17th St',
             'phone_number': '555-154-4848', 'email': 'MattyWalker@aol.com'},
            {'user_id': 'user0002', 'name': 'New Guy', 'address': '811 Ferns Ave',
             'phone_number': '555-478-8757', 'email': 'ThisTheNewGuy@Hotmail.com'},
            {'user_id': 'user0003', 'name': 'One More', 'address': '64 That St NW',
             'phone_number': '555-777-5558', 'email': 'OneMoreEmail@Netscape.com'}
        ]
        with linear.MONGO:
            db = linear.MONGO.connection.media  # pylint: disable=C0103
            db[TEST_DB_NAMES[1]].insert_many(test_customers)
            db[TEST_DB_NAMES[2]].insert_many(test_rentals)
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            rental_customers_1 = linear.show_rentals('prd00001')
            rental_customers_2 = linear.show_rentals('prd00002')
            rental_customers_3 = linear.show_rentals('prd00003')
        customer_1 = {'name': 'Matt Walker', 'address': '5478 17th St',
                      'phone_number': '555-154-4848', 'email': 'MattyWalker@aol.com'}
        customer_2 = {'name': 'New Guy', 'address': '811 Ferns Ave', 'phone_number': '555-478-8757',
                      'email': 'ThisTheNewGuy@Hotmail.com'}
        customer_3 = {'name': 'One More', 'address': '64 That St NW',
                      'phone_number': '555-777-5558', 'email': 'OneMoreEmail@Netscape.com'}
        self.assertEqual(customer_1, rental_customers_1['user0001'])
        self.assertEqual(customer_2, rental_customers_1['user0002'])
        self.assertEqual(customer_1, rental_customers_2['user0001'])
        self.assertEqual(customer_3, rental_customers_3['user0003'])
        self.assertEqual({}, linear.show_rentals('prod00004'))
        self.assertEqual(2, len(rental_customers_1))
        self.assertEqual(1, len(rental_customers_2))
        clear_test_collections()


class DatabaseIntegrationTest(TestCase):
    """
    Class for integration tests for linear.py
    """
    def test_integration_database(self):
        """Integration test to ensure items can be added and queried correctly"""
        clear_test_collections()
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            import_data = linear.import_data('', 'Products.csv', 'Customers.csv', 'Rentals.csv')
        self.assertEqual([(4, 3, 4), (0, 0, 0)], import_data)
        item_1 = {'description': 'Computer keyboard', 'product_type': 'office',
                  'quantity_available': '100'}
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            available_products = linear.show_available_products()
        self.assertEqual(item_1, available_products['prd0001'])
        with patch('linear.__set_collection_names', return_value=TEST_DB_NAMES):
            rental_customers_1 = linear.show_rentals('prd00001')
        customer_1 = {'name': 'Matt Walker', 'address': '5478 17th St',
                      'phone_number': '555-154-4848', 'email': 'MattyWalker@aol.com'}
        self.assertEqual(customer_1, rental_customers_1['user0001'])
        self.assertEqual(2, len(rental_customers_1))
