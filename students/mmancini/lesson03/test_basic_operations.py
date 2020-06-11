'''
Test basic_operations
'''

# pylint: disable=too-few-public-methods
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
# pylint: disable=unnecessary-pass
# pylint: disable=no-self-use


import logging
from unittest import TestCase
from peewee import *
from customers_model import *
from basic_operations import add_customer, search_customer, delete_customer
from basic_operations import update_customer_credit, list_active_customers

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger initialized')

LOGGER.info('creating test db')
database.init('test.db')

class SuiteOfTests(TestCase):
    '''testing basic operation'''
    customer_111 = ('111', 'John', 'Smith', '111 Main St', 1112223333,
        'johnsmith@gmail.com', True, 1500)
    
    def setUp(self):
        '''sets up the database'''
        
        
        database.drop_tables([Customer])
        database.create_tables([Customer])

        LOGGER.info('test setup complete')

    def test_add_customer(self):
        '''test add customer'''
        pass
        add_customer(self.customer_111[0], self.customer_111[1], self.customer_111[2], self.customer_111[3], self.customer_111[4],
                     self.customer_111[5], self.customer_111[6], self.customer_111[7])
        customer = Customer.get(Customer.customer_id == self.customer_111[0])
        self.assertEqual(customer.customer_id, self.customer_111[0])
        self.assertEqual(customer.first_name, self.customer_111[1])
        self.assertEqual(customer.last_name, self.customer_111[2])
        self.assertEqual(customer.home_address, self.customer_111[3])
        self.assertEqual(customer.phone_number, self.customer_111[4])
        self.assertEqual(customer.email_address, self.customer_111[5])
        self.assertEqual(customer.activity_status, self.customer_111[6])
        self.assertEqual(customer.credit_limit, self.customer_111[7])
        LOGGER.info('test add customer completed')

    def Xtest_search_customer(self):
        '''test search customer'''
        pass
        LOGGER.info('test search customer completed')

    def Xtest_delete_customer(self):
        '''test delete customer'''
        pass
        LOGGER.info('test delete customer completed')

    def Xtest_update_customer_credit(self):
        '''test update customer'''
        pass
        LOGGER.info('test update customer completed')

    def Xtest_list_active_customers(self):
        '''test list active customers'''
        pass
        LOGGER.info('test list active customers completed')
