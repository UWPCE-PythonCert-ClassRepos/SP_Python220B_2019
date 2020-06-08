"""
Unit tests for database.py
"""

# pylint: disable=C0103
# pylint: disable=W

import logging
from unittest import TestCase
from database import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class TestBasicOperations(TestCase):
    '''Test all Database functions'''
    def setUp(self):
        """Remove collections and start with no data"""
        mongo = MongoDBConnection()

        with mongo:
            db = mongo.connection.hp_norton
            db["customers"].drop()
            db["products"].drop()
            db["rentals"].drop()

    def tearDown(self):
        """Remove collections"""
        mongo = MongoDBConnection()

        with mongo:
            db = mongo.connection.hp_norton
            db["customers"].drop()
            db["products"].drop()
            db["rentals"].drop()

    def test_import_data(self):
        """Test importing data from csv into mongodb"""
        result = import_data("../lesson05", "products.csv", "customers.csv", "rentals.csv")
        compare = ((5, 5, 6), (0, 0, 0))
        self.assertEqual(result, compare)

    def test_import_data_fail(self):
        """Test import failures are counted and handled"""
        result = import_data("../lesson05", "products.csv", "customers_fail.csv", "rentals.csv")
        compare = ((5, 0, 0), (0, 1, 0))
        self.assertEqual(result, compare)


    def test_show_available_products(self):
        """Test showing all available prods , greater than 1"""
        import_data("../lesson05", "products.csv", "customers.csv", "rentals.csv")
        result = show_available_products()
        compare = {'prd003': {'description': 'king-sized bed',
                              'quantity_available': '4',
                              'product_type': 'bedroom'},
                   'prd001': {'description': '60-inch TV stand',
                              'quantity_available': '1',
                              'product_type': 'livingroom'},
                   'prd005': {'description': 'large mixer',
                              'quantity_available': '12',
                              'product_type': 'kitchen'},
                   'prd004': {'description': 'small nightstand',
                              'quantity_available': '3',
                              'product_type': 'bedroom'}}
        self.assertEqual(result, compare)

    def test_show_rentals(self):
        """Test showing who rented a product"""
        import_data("../lesson05", "products.csv", "customers.csv", "rentals.csv")
        result = show_rentals('prd005')
        compare = {'user003': {'name': 'John Charles',
                               'address': '345 Main street',
                               'phone_number': '718-555-4893',
                               'email': 'jackdude@yahoo.com'},
                   'user005': {'name': 'Optimus G',
                               'address': '101 Cybertron St.',
                               'phone_number': '212-555-0001',
                               'email': 'spacerobot@gmail.com'}}
        self.assertEqual(result, compare)
