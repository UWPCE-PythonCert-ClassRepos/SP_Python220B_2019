'''
Integration tests for basic operations
'''

# pylint: disable=W

from unittest import TestCase
import logging
import peewee
from customers_model import *
from basic_operations import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class TestIntegration(TestCase):
    '''Integration test'''
    def setUp(self):
        '''Create tables'''
        database.create_tables([Customers])
        LOGGER.info('Create table successful')

    def tearDown(self):
        '''Destroy tables'''
        database.drop_tables([Customers])
        LOGGER.info('Database tables dropped')

    def test_integration(self):
        '''add a customer, delete customer, count number of active'''
        test_customer_1 = {
            'customer_id': '12345',
            'name': 'Eric Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }
        test_customer_2 = {
            'customer_id': '45678',
            'name': 'Jack Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': False,
            'credit_limit': 25000
        }
        test_customer_3 = {
            'customer_id': '54321',
            'name': 'Vivie Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        }
        add_customer(**test_customer_1)
        add_customer(**test_customer_2)
        add_customer(**test_customer_3)
        delete_customer(test_customer_1['customer_id'])
        self.assertEqual(list_active_customers(), 1)
        