"""
Module to test Customers Database and
functionality from basic_operations module.
"""

# pylint:disable=wildcard-import
# pylint: disable=unused-wildcard-import
# pylint: disable=invalid-name
# pylint: disable=no-value-for-parameter

import logging
from unittest import TestCase
from basic_operations import *
from customer_model import *

# Set up logger for program.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Logger is active.')

class TestBasicOperations(TestCase):
    """Tests basic operations module and functionality of database."""

    logger.info('Testing Basic Operations...')
    def setUp(self): # Create database

        logger.info('Creating tables')
        database.drop_tables([Customer])
        database.create_tables([Customer])
        logger.info('Tables created.')

        logger.info('Adding test data to database...')
        add_customer(37431, 'Bill', 'Gates',
                     '500 5th Ave, Seattle, WA',
                     '206-709-3100', 'bgates@microsoft.com',
                     50000.00, False)
        add_customer(18720, 'Steve', 'Ballmer',
                     '123 Bel Air Road Los Angeles, CA',
                     '425-882-8080', 'sballmer@microsoft.com',
                     25000.00, True)
        add_customer(700459, 'Elliot', 'Alderson',
                     '135 East 57th Street, New York, NY',
                     '212-867-5309', 'alderson@gmail.com',
                     3500.00, True)
        logger.info('Test data uploaded.  Ready to test.')

    def test_add_customer(self):
        """Tests adding a customer to the database."""

        c_1 = Customer.get(Customer.customer_id == 37431)

        self.assertEqual(c_1.customer_id, 37431)
        self.assertEqual(c_1.first_name, 'Bill')
        self.assertEqual(c_1.last_name, 'Gates')
        self.assertEqual(c_1.home_address, '500 5th Ave, Seattle, WA')
        self.assertEqual(c_1.phone_number, '206-709-3100')
        self.assertEqual(c_1.email_address, 'bgates@microsoft.com')
        self.assertEqual(c_1.credit_limit, 50000)
        self.assertEqual(c_1.active_status, False)

    def test_invalid_input(self):
        """Tests customer will not be added without function parameters being met."""

        with self.assertRaises(TypeError):
            add_customer(12345, 'Paul', 'Allen')

    def test_search_customer(self):
        """Tests a customer's info can be found by searching their ID."""

        c_2 = search_customer(18720)
        logger.info('Searching for customer ID 18720')
        expected = {'first_name': 'Steve',
                    'last_name': 'Ballmer',
                    'email_address': 'sballmer@microsoft.com',
                    'phone_number':  '425-882-8080'}

        self.assertEqual(c_2, expected)

    def test_invalid_id(self):
        """Tests empty object will be return with unknown id."""

        c_1 = search_customer(112233)
        self.assertEqual(c_1, {})

    def test_delete_customer(self):
        """Deletes a given customer from given ID."""

        delete_customer(37431)
        expected = search_customer(37431)
        self.assertEqual(expected, {})

    def test_update_credit(self):
        """Tests functionality of updating a customer's credit limit."""

        update_customer_credit(700459, 5500)
        c_1 = Customer.get(Customer.customer_id == 700459).credit_limit
        self.assertEqual(c_1, 5500)

    def test_list_active_customers(self):
        """Tests if function works with listing numbe of active customers."""

        n = list_active_customers()
        self.assertEqual(n, 2)

    def test_integration(self):
        """Tests database integration as a whole."""

        t = list_active_customers()
        self.assertEqual(2, t)

        add_customer(99250, 'Raylan', 'Givens',
                     '210 Chery Street, Harlan, KY',
                     '606-110-1870', 'givens@usmarshals.gov',
                     5000.00, True)
        c_1 = Customer.get(Customer.customer_id == 99250)
        self.assertEqual(5000.00, c_1.credit_limit)

        update_customer_credit(99250, 10000.00)
        c_2 = Customer.get(Customer.customer_id == 99250)
        self.assertEqual(10000.00, c_2.credit_limit)

        n = list_active_customers()
        self.assertEqual(3, n)

        delete_customer(99250)
        expected = search_customer(99250)
        self.assertEqual(expected, {})

        n_2 = list_active_customers()
        self.assertEqual(2, n_2)
