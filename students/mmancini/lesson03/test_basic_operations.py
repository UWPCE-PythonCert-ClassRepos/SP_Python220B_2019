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
        add_customer(self.customer_111[0], self.customer_111[1], self.customer_111[2],
                     self.customer_111[3], self.customer_111[4],
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

        # test we are unable to add same customer
        with self.assertRaises(IntegrityError):
            add_customer(self.customer_111[0], self.customer_111[1], self.customer_111[2],
                         self.customer_111[3], self.customer_111[4],
                         self.customer_111[5], self.customer_111[6], self.customer_111[7])

            
    def test_search_customer(self):
        '''test search customer'''
        pass
        add_customer(self.customer_111[0], self.customer_111[1], self.customer_111[2],
                     self.customer_111[3], self.customer_111[4],
                     self.customer_111[5], self.customer_111[6], self.customer_111[7])

        customer_dict = search_customer(self.customer_111[0])
        expected_dict = {'first_name': self.customer_111[1],
                         'last_name': self.customer_111[2],
                         'email_address': self.customer_111[5],
                         'phone_number': self.customer_111[4]}
        self.assertEqual(customer_dict, expected_dict)

        # Test customer not in db
        with self.assertRaises(ValueError):
            search_customer('222')

        LOGGER.info('test search customer completed')

    def test_delete_customer(self):
        '''test delete customer'''
        pass
        add_customer(self.customer_111[0], self.customer_111[1], self.customer_111[2],
                     self.customer_111[3], self.customer_111[4],
                     self.customer_111[5], self.customer_111[6], self.customer_111[7])
        delete_customer(self.customer_111[0])
        LOGGER.info('customer deleted')
        LOGGER.info('customer %s %s deleted', self.customer_111[1], self.customer_111[2])

        # ensure its deleted
        with self.assertRaises(ValueError):
            delete_customer(self.customer_111[0])

        LOGGER.info('test delete customer completed')

    def test_update_customer_credit(self):
        '''test update customer'''
        pass
        add_customer(self.customer_111[0], self.customer_111[1], self.customer_111[2],
                     self.customer_111[3], self.customer_111[4],
                     self.customer_111[5], self.customer_111[6], self.customer_111[7])
        customer = Customer.get(Customer.customer_id == self.customer_111[0])
        LOGGER.info("test update customer credit limit before update is %s", customer.credit_limit)
        update_customer_credit(self.customer_111[0], 3000)
        customer = Customer.get(Customer.customer_id == self.customer_111[0])
        LOGGER.info("test update customer credit limit after update is %s", customer.credit_limit)
        self.assertEqual(customer.credit_limit, 3000)
        LOGGER.info('test update customer completed')

        # Test update of invalid customer id
        with self.assertRaises(ValueError):
            update_customer_credit('222', 7500)
        
        
    def test_list_active_customers(self):
        '''test list active customers'''
        pass
        add_customer(self.customer_111[0], self.customer_111[1], self.customer_111[2],
                     self.customer_111[3], self.customer_111[4],
                     self.customer_111[5], self.customer_111[6], self.customer_111[7])
        active_count = list_active_customers()
        self.assertEqual(1, active_count)
        customer = Customer.get(Customer.customer_id == self.customer_111[0])
        customer.delete_instance()
        active_count = list_active_customers()
        self.assertEqual(0, active_count)

        LOGGER.info('test list active customers completed')
