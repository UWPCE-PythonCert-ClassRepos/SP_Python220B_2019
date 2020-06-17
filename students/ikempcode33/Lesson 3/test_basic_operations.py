"""Tests customer model operations"""

import logging
from customer_model import *
from basic_operations import *
from unittest import TestCase

#Set up logging info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("logger is active_")


class TestBasicOp(TestCase):
    logger.info("testing basic operations")

    def setUp(self):
        #used to create database tables and set up the test customers data
        logger.info('creating tables')
        database.drop_tables([Customer])
        database.create_tables([Customer])
        logger.info('tables are created.')

        logger.info('Adding data to database')
        # Test customer 1
        add_customer(1773, 'Karen', 'Smith',
                     '142 42 st, Bellevue, WA 98105',
                     '123-456-7890', 'ksmith99@gmail.com',
                     True, 40000.00)
        # Test customer 2
        add_customer(1223, 'Georgia', 'Smith',
                     '123 5 st, Palmsprings, CA 94930',
                     '415-890-8787', 'gsmith@gmail.com',
                     True, 60000.00)
        # Test customer 3
        add_customer(1003, 'Paul', 'Stevens',
                     '773 7 st, Los Angeles, CA 90005',
                     '415-770-3434', 'pstevens199@gmail.com',
                     True, 50000.00)
        logger.info("data is uploaded, ready to begin tests")

    def test_add_customer(self):
        """Tests adding customers to database, Customer 1"""
        cus_1 = Customer.get(Customer.customer_id == 1773)
        self.assertEqual(cus_1.customer_id, 1773)
        self.assertEqual(cus_1.first_name, 'Karen')
        self.assertEqual(cus_1.last_name, 'Smith')
        self.assertEqual(cus_1.home_address, '142 42 st, Bellevue, WA 98105')
        self.assertEqual(cus_1.phone_number, '123-456-7890')
        self.assertEqual(cus_1.status, True)
        self.assertEqual(cus_1.credit_limit, 40000.00)

    def test_search_customer(self):
        """Tests that a customer can be searched via ID"""
        cus_2 = search_customer(1003)
        logger.info("searching for customer ID 1003")
        expected = {'first_name': 'Paul',
                    'last_name': 'Stevens',
                    'phone_number': '415-770-3434',
                    'email_address': 'pstevens199@gmail.com'}
        self.assertEqual(cus_2, expected)
    
    def test_invalid_customer_id(self):
        """If there is an unknown ID this tests that an empty object returned"""
        cus_1 = search_customer(123232)
        self.assertEqual(cus_1, {})

    def test_update_customer_credit(self):
        """Tests that customers credit can be updated"""
        update_customer_credit(1773, 60000)
        cus_1 = Customer.get(Customer.customer_id == 1773).credit_limit
        self.assertEqual(cus_1, 60000)

        with self.assertRaises(DoesNotExist):
            update_customer_credit(3334, 10000)

    def test_list_active_customers(self):
        """Test if active customer function works"""
        num = list_active_customers()
        self.assertEqual(num, 3)
    
    def test_delete_customer(self):
        '''Tests that a customer can be deleted properly'''
        delete_customer(1773)
        expected = search_customer(1773)
        self.assertEqual(expected, {})
        with self.assertRaises(DoesNotExist):
            delete_customer(3334)

