'''
Test basic_operations
'''

import logging
from unittest import TestCase
from peewee import *
from customers_model import *
from basic_operations import add_customer, search_customer, delete_customer
from basic_operations import update_customer_credit, list_active_customers

#pylint Disable=wildcard-import, unused-wildcard-import

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger initialized')

LOGGER.info('creating test db')
database.init('test.db')

class SuiteOfTests(TestCase):
    '''testing basic operation'''
    def setUp(self):
        '''sets up the database'''
        database.drop_tables([Customer])
        database.create_tables([Customer])

        LOGGER.info('test setup complete')

    def test_add_customer(self):
        '''test add customer'''
        pass
        LOGGER.info('test delete customer completed')

        pass
        
    def test_search_customer(self):
        '''test search customer'''
        pass
        LOGGER.info('test search customer completed')
        
    def test_delete_customer(self):
        '''test delete customer'''
        LOGGER.info('test delete customer completed')

    def test_update_customer_credit(self):
        '''test update customer'''
        pass
        LOGGER.info('test update customer completed')

    def test_list_active_customers(self):
        '''test list active customers'''
        LOGGER.info('test list active customers completed')

