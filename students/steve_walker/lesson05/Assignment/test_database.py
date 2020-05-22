"""Tests for database.py"""

from unittest import TestCase
from collections import OrderedDict
import database as db


class DatabaseTests(TestCase):
    """Unit tests for database.py."""

    def test_csv_to_dict(self):
        test_dict = db.csv_to_dict('data/test.csv')
        expected_dict = [OrderedDict([('test_id', 'test_1'),
                                      ('description', 'test 1'),
                                      ('quantity_available', '0'),
                                      ('product_id', 'prod_1'),
                                      ('customer_id', 'cust_1')]),
                         OrderedDict([('test_id', 'test_2'),
                                      ('description', 'test 2'),
                                      ('quantity_available', '2'),
                                      ('product_id', 'prod_1'),
                                      ('customer_id', 'cust_2')]),
                         OrderedDict([('test_id', 'test_3'),
                                      ('description', 'test 3'),
                                      ('quantity_available', '4'),
                                      ('product_id', 'prod_1'),
                                      ('customer_id', 'cust_2')]),
                         OrderedDict([('test_id', 'test_4'),
                                      ('description', 'test 4'),
                                      ('quantity_available', '8'),
                                      ('product_id', 'prod_2'),
                                      ('customer_id', 'cust_3')])]

        self.assertEqual(test_dict, expected_dict)


    def test_import_data(self):
        # Make sure import_data works when error free
        db.drop_data()
        good_import = db.import_data('data', 'products.csv',
                                     'customers.csv', 'rentals.csv')
        expected_good_import = ((5, 3, 8), (0, 0, 0))
        self.assertEqual(good_import, expected_good_import)

        # Make sure import_data catches expected errors
        db.drop_data()
        bad_import = db.import_data('data', 'products.csv',
                                    'bad_customers', 'bad_rentals')
        expected_bad_import = ((5, 0, 0), (0, 1, 1))
        self.assertEqual(bad_import, expected_bad_import)


    def test_show_available_products(self):
        db.drop_data()
        db.import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
        test = db.show_available_products()
        expected = {'prod_1': {'description': 'big stack of paper',
                               'product_type': 'paper',
                               'quantity_available': 5000},
                    'prod_2': {'description': 'medium stack of paper',
                               'product_type': 'paper',
                               'quantity_available': 10000},
                    'prod_3': {'description': 'pre-folded paper airplanes',
                               'product_type': 'airplane',
                               'quantity_available': 747},
                    'prod_4': {'description': 'magazine cover',
                               'product_type': 'media',
                               'quantity_available': 50},
                    'prod_5': {'description': 'internet takeover',
                               'product_type': 'media',
                               'quantity_available': 7}}

        self.assertEqual(test, expected)


    def test_show_rentals(self):
        db.drop_data()
        db.import_data('data', 'products.csv', 'customers.csv', 'test.csv')
        test = db.show_rentals('prod_1')
        expected = {'cust_1': {'name': 'Rhianna Flygirl',
                               'address': 'The Stage',
                               'phone': '3241232455',
                               'email': 'star@skycloud.com'},
                    'cust_2': {'name': 'John Muir', 'address':
                               'Yosemite', 'phone': '3241232455',
                               'email': 'muir@skycloud.com'}}

        self.assertEqual(test, expected)


    def test_drop_data(self):
        db.drop_data()

        # Populate the database
        db.import_data('data', 'products.csv', 'customers.csv', 'test.csv')

        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection.media
            record_count = database['rentals'].count_documents({})

        self.assertEqual(record_count, 4)

        # Make sure the database successfully clears
        db.drop_data()
        with mongo:
            database = mongo.connection.media
            record_count = database['rentals'].count_documents({})

        self.assertEqual(record_count, 0)
