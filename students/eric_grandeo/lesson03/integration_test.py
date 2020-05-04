'''
Integration tests for basic operations
'''



from unittest import TestCase
from customers_model import *
from basic_operations import *
import peewee
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestIntegration(TestCase):
    def setUp(self):
        '''insert docstring''' 
        database.create_tables([Customers])
        logger.info('Create table successful')
        
    def tearDown(self):
        '''insert docstring''' 
        database.drop_tables([Customers])
        logger.info('Database tables dropped')
    
    def test_integration(self):
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
        self.assertEqual(list_active_customers(),1)
        
        