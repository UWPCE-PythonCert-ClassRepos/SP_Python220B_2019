"""
Unit tests for database.py
"""

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
        result = import_data("/home/ejgrandeo/uwpython/SP_Python220B_2019/students/eric_grandeo/lesson05", "products.csv", "customers.csv", "rentals.csv")
        compare = ((5, 5, 6), (0, 0, 0))
        self.assertEqual(result, compare)
    
    def test_import_data_fail(self):
        result = import_data("/home/ejgrandeo/uwpython/SP_Python220B_2019/students/eric_grandeo/lesson05", "products.csv", "customers_fail.csv", "rentals.csv")
        compare = ((5, 0, 0), (0, 1, 0))
        self.assertEqual(result, compare)
        #figure out how to cause an error on upload into mongo, create a test data file
    
    def test_show_available_products(self):
        import_data("/home/ejgrandeo/uwpython/SP_Python220B_2019/students/eric_grandeo/lesson05", "products.csv", "customers.csv", "rentals.csv")
        result = show_available_products()
        compare = {'prd003': {'description': 'king-sized bed', 'quantity_available': '4', 'product_type': 'bedroom'}, 'prd001': {'description': '60-inch TV stand', 'quantity_available': '1', 'product_type': 'livingroom'}, 'prd005': {'description': 'large mixer', 'quantity_available': '12', 'product_type': 'kitchen'}, 'prd004': {'description': 'small nightstand', 'quantity_available': '3', 'product_type': 'bedroom'}}
        self.assertEqual(result, compare)
    
    def test_show_rentals(self):
        pass
    