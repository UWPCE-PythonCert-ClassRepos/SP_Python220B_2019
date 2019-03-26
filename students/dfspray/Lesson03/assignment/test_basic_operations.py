"""Creates a full suite of tests for basic_operations.py"""

import unittest
import basic_operations
import customer_model_schema
from customer_model_schema import *
from peewee import *
import create_customer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestOperations(unittest.TestCase):
    """Tests the methods of basic_operations"""
    def test_add_customer(self):
        """This method tests that 3 customers are successfully added to the database"""
        basic_operations.add_customer(
            '001', 'Joey', 'Smith', '123 Jackson Street', 1234567890,
            'joey@gmail.com', 'active', 1000.00
        )
        basic_operations.add_customer(
            '002', 'Alex', 'Peterson', '123 Jefferson Street', 2345678901,
            'alex@gmail.com', 'active', 1000.00
        )
        basic_operations.add_customer(
            '003', 'Aaron', 'Dickson', '123 Rainier Street', 3456789012,
            'aaron@gmail.com', 'inactive', 1000.00
        )

        database = SqliteDatabase('customers.db')

        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            added_customer1 = Customers.get(Customers.customer_id == '001')
            actual_customer1 = (added_customer1.customer_id, added_customer1.name,
            added_customer1.lastname, added_customer1.home_address,
            added_customer1.phone_number, added_customer1.email_address,
            added_customer1.status, added_customer1.credit_limit)
            expected_customer1 = ('001', 'Joey', 'Smith', '123 Jackson Street', '1234567890',
            'joey@gmail.com', 'active', 1000.00)

            added_customer2 = Customers.get(Customers.customer_id == '002')
            actual_customer2 = (added_customer2.customer_id, added_customer2.name,
            added_customer2.lastname, added_customer2.home_address,
            added_customer2.phone_number, added_customer2.email_address,
            added_customer2.status, added_customer2.credit_limit)
            expected_customer2 = ('002', 'Alex', 'Peterson', '123 Jefferson Street', '2345678901',
            'alex@gmail.com', 'active', 1000.00)

            added_customer3 = Customers.get(Customers.customer_id == '003')
            actual_customer3 = (added_customer3.customer_id, added_customer3.name,
            added_customer3.lastname, added_customer3.home_address,
            added_customer3.phone_number, added_customer3.email_address,
            added_customer3.status, added_customer3.credit_limit)
            expected_customer3 = ('003', 'Aaron', 'Dickson', '123 Rainier Street', '3456789012',
            'aaron@gmail.com', 'inactive', 1000.00)
        except Exception as e:
            logger.info(e)

        self.assertEqual(actual_customer1, expected_customer1)
        self.assertEqual(actual_customer2, expected_customer2)
        self.assertEqual(actual_customer3, expected_customer3)
				
    def test_search_customer(self):
        """This method tests that the customer search function works properly"""
        actual_searched_customer1 = basic_operations.search_customer('001')
        expected_searched_customer1 = {'customer_id': '001',
                'name': 'Joey', 'lastname': 'Smith', 'home_address': '123 Jackson Street',
                'phone_number': '1234567890', 'email_address': 'joey@gmail.com',
                'status': 'active', 'credit_limit': 1000.00}

        actual_searched_customer2 = basic_operations.search_customer('002')
        expected_searched_customer2 = {'customer_id': '002',
                'name': 'Alex', 'lastname': 'Peterson', 'home_address': '123 Jefferson Street',
                'phone_number':  '2345678901', 'email_address': 'alex@gmail.com',
                'status': 'active', 'credit_limit': 1000.00}

        actual_searched_customer3 = basic_operations.search_customer('003')
        expected_searched_customer3 = {'customer_id': '003',
                'name': 'Aaron', 'lastname': 'Dickson', 'home_address': '123 Rainier Street',
                'phone_number': '3456789012', 'email_address': 'aaron@gmail.com',
                'status': 'inactive', 'credit_limit': 1000.00}

        actual_searched_customer4 = basic_operations.search_customer('004')
        expected_searched_customer4 = {}

        self.assertEqual(actual_searched_customer1, expected_searched_customer1)
        self.assertEqual(actual_searched_customer2, expected_searched_customer2)
        self.assertEqual(actual_searched_customer3, expected_searched_customer3)
        self.assertEqual(actual_searched_customer4, expected_searched_customer4)
