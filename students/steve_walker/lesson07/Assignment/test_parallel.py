"""Tests for parallel.py"""

# pylint: disable=C0116

from unittest import TestCase
from collections import OrderedDict
import parallel


class DatabaseTests(TestCase):
    """Unit tests for database.py."""

    def test_csv_to_dict(self):
        test_dict = parallel.csv_to_dict('data/test.csv')
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
        parallel.drop_data()
        good_import = parallel.import_data('data', 'products.csv',
                                           'customers.csv', 'rentals.csv')
        self.assertEqual(good_import[0][0], 9999)
        self.assertEqual(good_import[0][1], 0)
        self.assertEqual(good_import[0][2], 9999)
        self.assertEqual(type(good_import[0][3]), type(float(1.02)))
        self.assertEqual(good_import[0], good_import[1])


    def test_drop_data(self):
        parallel.drop_data()

        # Populate the database
        parallel.import_data('data', 'products.csv', 'customers.csv', 'test.csv')

        mongo = parallel.MongoDBConnection()
        with mongo:
            database = mongo.connection.media
            record_count = database['rentals'].count_documents({})

        self.assertEqual(record_count, 4)

        # Make sure the database successfully clears
        parallel.drop_data()
        with mongo:
            database = mongo.connection.media
            record_count = database['rentals'].count_documents({})

        self.assertEqual(record_count, 0)
