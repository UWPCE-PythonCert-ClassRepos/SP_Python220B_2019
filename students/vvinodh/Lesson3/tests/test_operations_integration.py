"""Creates an integration test for basic_operations.py"""

import logging
import unittest
import sys
from peewee import *
from src import basic_operations
from src.customer_model_schema import Customers

sys.path.append(r"C:\UW-Python-Advanced\SP_Python220B_2019\students\vvinodh\Lesson3")



DATABASE = SqliteDatabase('customers.db')
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class TestOperations(unittest.TestCase):
    """Tests all the methods in basic_operations in one go"""
    def test_full_integration(self):
        """Integrates all methods into one test"""
        basic_operations.add_customer('010', 'James', 'Bond', '123 Turnberry Street', 8885671000,
                                      'bond@bond.com', 'active', 1000.00)
        basic_operations.update_customer_credit('010', 3000)
        basic_operations.update_status('010', 'inactive')
        expected_customer = {'customer_id': '010', 'name': 'James', 'lastname': 'Bond',
                             'home_address': '123 Turnberry Street', 'phone_number': '8885671000',
                             'email_address': 'bond@bond.com', 'status': 'inactive',
                             'credit_limit': 3000.00}
        actual_searched_customer = basic_operations.search_customer('010')
        self.assertEqual(actual_searched_customer, expected_customer)
        actual_customer_count = basic_operations.list_active_customers()
        self.assertEqual(actual_customer_count, 1)
        basic_operations.delete_customer('010')

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
            LOGGER.info('Error finding customer 010')
            LOGGER.info(ex)
            deleted_customer = {}

        self.assertEqual(deleted_customer, {})
        LOGGER.info('Closing database')
        DATABASE.close()
