"""
Contains unit tests for the basic_operations file for interacting with the customer database.
"""
# pylint: disable=unused-argument, no-value-for-parameter

from unittest import TestCase
from unittest.mock import patch
import peewee

import basic_operations
from basic_operations import (add_customer, search_customer, delete_customer,
                              update_customer_credit, list_active_customers)
from customer_model import Customer, DATABASE as database

TEST_DATABASE = 'test.db'


class BasicOperationsUnitTests(TestCase):
    """Tests for each function in basic_operations.py."""
    def setUp(self):
        """Defines starting test database used for function testing."""
        starting_db = [(1, 'Bob', 'Bobbo', '12 Green St', '1112223344',
                        'bobbo@python.org', False, 85000),
                       (2, 'Jane', 'Janeo', '1550 Red Rd', '1118675309',
                        'jane@therealjane.com', True, 150000),
                       (5, 'Wilson', 'Volleyball', '1 Castaway Island', '0000000000',
                        'wilson@ImLost.com', True, 0)
                       ]
        database.init(TEST_DATABASE)
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON')
        database.create_tables([Customer])
        with database.transaction():
            Customer.delete().execute()
            Customer.insert_many(starting_db, fields=[Customer.customer_id, Customer.name,
                                                      Customer.lastname, Customer.home_address,
                                                      Customer.phone_number, Customer.email_address,
                                                      Customer.active_status, Customer.credit_limit
                                                      ]).execute()
        database.close()


    @patch('basic_operations.DATABASE_NAME')
    def test_add_customer(self, mock_database):
        """Testing adding a customer to the database via add_customer function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        add_customer(17, 'Bob', 'Testy', '111 Test St', 1234567890, 'bob@thetest.net', True, 70000)
        test_customer = Customer.get_by_id(17)
        self.assertEqual(test_customer.name, 'Bob')
        self.assertEqual(test_customer.lastname, 'Testy')
        self.assertEqual(test_customer.home_address, '111 Test St')
        self.assertEqual(test_customer.phone_number, '1234567890')
        self.assertEqual(test_customer.email_address, 'bob@thetest.net')
        self.assertEqual(test_customer.active_status, True)
        self.assertEqual(test_customer.credit_limit, 70000)

        self.assertFalse(add_customer(17, 'Bob', 'Testy', '111 Test St', 1234567890,
                                      'bob@thetest.net', True, 70000))


    @patch('basic_operations.DATABASE_NAME')
    def test_search_customer(self, mock_database):
        """Testing searching a customer to the database via search_customer function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        exp_dict = {
            'name': 'Wilson',
            'lastname': 'Volleyball',
            'email_address': 'wilson@ImLost.com',
            'phone_number': '0000000000'
            }
        self.assertDictEqual(search_customer(5), exp_dict)
        self.assertDictEqual(search_customer(3), {})


    @patch('basic_operations.DATABASE_NAME')
    def test_delete_customer(self, mock_database):
        """Testing deleting a customer to the database via delete_customer function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        self.assertTrue(delete_customer(1))
        with self.assertRaises(peewee.DoesNotExist):
            Customer.get_by_id(1)
        self.assertFalse(delete_customer(3))


    @patch('basic_operations.DATABASE_NAME')
    def test_update_customer_credit(self, mock_database):
        """Testing updating customer credit via update_customer_credit function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        self.assertTrue(update_customer_credit(5, 5000))
        self.assertEqual(Customer.get_by_id(5).credit_limit, 5000)
        with self.assertRaises(ValueError):
            update_customer_credit(4, 80000)


    @patch('basic_operations.DATABASE_NAME')
    def test_list_active_customers(self, mock_database):
        """Testing updating customer credit via update_customer_credit function."""
        basic_operations.DATABASE_NAME = TEST_DATABASE
        self.assertEqual(list_active_customers(), 2)
