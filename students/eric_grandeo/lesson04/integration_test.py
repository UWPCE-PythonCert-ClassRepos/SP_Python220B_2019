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
        test_customers = [{
            'customer_id': '54321',
            'name': 'Eric Grandeo',
            'lastname': 'Grandeo',
            'home_address': '123 Fake Street',
            'phone_number': '1-212-555-1234',
            'email_address': 'email@email.com',
            'status': True,
            'credit_limit': 25000
        },
                          {
                              'customer_id': '98765',
                              'name': 'Jack Charles',
                              'lastname': 'Charles',
                              'home_address': '123 Fake Street',
                              'phone_number': '1-212-555-1234',
                              'email_address': 'email@email.com',
                              'status': False,
                              'credit_limit': 25000
                          }
                          , {
                              'customer_id': '10846',
                              'name': 'Vivie Harper',
                              'lastname': 'Harper',
                              'home_address': '123 Fake Street',
                              'phone_number': '1-212-555-1234',
                              'email_address': 'email@email.com',
                              'status': True,
                              'credit_limit': 25000
                          }]
        add_multiple_customers(test_customers)
        delete_customer(test_customers[0]['customer_id'])
        self.assertEqual(list_active_customers(), 1)
    