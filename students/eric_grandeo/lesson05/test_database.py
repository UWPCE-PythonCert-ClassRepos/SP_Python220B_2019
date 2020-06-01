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
        import_data("/home/ejgrandeo/uwpython/SP_Python220B_2019/students/eric_grandeo/lesson05", "products.csv")
    
    def test_show_available_products(self):
        pass
    
    def test_show_rentals(self):
        pass
    