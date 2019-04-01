"""Creates an integration test for basic_operations.py"""

import logging
import unittest
#import sys
#sys.path.append('C:/Users/allth/OneDrive/Desktop/Python/Python220/SP_Python220B_2019/'
                'students/dfspray/Lesson03/assignment/src')
from peewee import *
import src
from src import basic_operations
from src import customer_model_schema
from src.customer_model_schema import Customers

DATABASE = SqliteDatabase('customers.db')
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class TestOperations(unittest.TestCase):
    """Tests all the methods in basic_operations in one go"""
    def test_full_integration(self):
        """Integrates all methods into one test"""
        basic_operations.add_customer('004', 'Joey', 'Smith', '123 Jackson Street', 1234567890,
                                      'joey@gmail.com', 'active', 1000.00)
        basic_operations.update_customer_credit('004', 2000)
        basic_operations.update_status('004', 'inactive')
        expected_customer = {'customer_id': '004', 'name': 'Joey', 'lastname': 'Smith',
                             'home_address': '123 Jackson Street', 'phone_number': '1234567890',
                             'email_address': 'joey@gmail.com', 'status': 'inactive',
                             'credit_limit': 2000.00}
        actual_searched_customer = basic_operations.search_customer('004')
        self.assertEqual(actual_searched_customer, expected_customer)
        actual_customer_count = basic_operations.list_active_customers()
        self.assertEqual(actual_customer_count, 0)
        basic_operations.delete_customer('004')

        try:
            DATABASE.connect()
            DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
            LOGGER.info('Successfully connected to the database')
            searched_customer = Customers.get(Customers.customer_id == '004')
            LOGGER.info('Customer Found!')
            deleted_customer = {'customer_id': searched_customer.customer_id,
                                'name': searched_customer.name,
                                'lastname': searched_customer.lastname,
                                'home_address': searched_customer.home_address,
                                'phone_number': searched_customer.phone_number,
                                'email_address': searched_customer.email_address,
                                'status': searched_customer.status,
                                'credit_limit': searched_customer.credit_limit}

        except Exception as ex:
            LOGGER.info('Error finding customer 004')
            LOGGER.info(ex)
            deleted_customer = {}

        self.assertEqual(deleted_customer, {})
        LOGGER.info('Closing database')
        DATABASE.close()
