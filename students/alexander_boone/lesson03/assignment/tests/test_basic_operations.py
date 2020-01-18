'''
This module includes the tests for module basic_operations.py.
'''

from unittest import TestCase
import sys
sys.path.append('..')
from basic_operations import *


class TestBasicOperations(TestCase):
    '''Test adding a customer to the database.'''
    def setUp(self):
        database.drop_tables([Customer])
        database.create_tables([Customer])
        add_customer(12345, 'Jeff', 'Bezos', '3582 Main St',
                     1234567890, 'Jeff@amazon.com', 'active',
                     200000)
        add_customer(1234567, 'MacKenzie', 'Bezos', '3582 Main St',
                     9999999999, 'MB@amazon.com', 'active',
                     100000)
        add_customer(123, 'Elon', 'Musk', '123 Main St',
                     0000000000, 'EM@spacex.com', 'inactive',
                     300000)

    def test_add_customer(self):
        '''Test adding a customer using the add_customer method.'''
        with database.transaction():
            jeff = Customer.get(Customer.customer_id == 12345)
            self.assertEqual(jeff.customer_id, 12345)
            self.assertEqual(jeff.name, 'Jeff')
            self.assertEqual(jeff.lastname, 'Bezos')
            self.assertEqual(jeff.home_address, '3582 Main St')
            self.assertEqual(jeff.phone_number, 1234567890)
            self.assertEqual(jeff.email_address, 'Jeff@amazon.com')
            self.assertEqual(jeff.status, 'active')
            self.assertEqual(jeff.credit_limit, 200000)

    def test_failure_add_customer(self):
        '''Test adding a customer without enough inputs.'''
        with self.assertRaises(TypeError):
            add_customer(12345, 'Jeff', 'Bezos')

    def test_search_customer(self):
        '''Test searching for a customer using customer id.'''
        jeff_dict = search_customer(12345)
        self.assertEqual(jeff_dict['name'], 'Jeff')
        self.assertEqual(jeff_dict['lastname'], 'Bezos')
        self.assertEqual(jeff_dict['home_address'], '3582 Main St')
        self.assertEqual(jeff_dict['phone_number'], 1234567890)
        self.assertEqual(jeff_dict['email_address'], 'Jeff@amazon.com')
        self.assertEqual(jeff_dict['status'], 'active')
        self.assertEqual(jeff_dict['credit_limit'], 200000)

    def test_search_customer_not_found(self):
        '''Test searching for a customer with an invalid id.'''
        jeff_dict = search_customer(8675309)
        self.assertEqual(jeff_dict, {})

    def test_delete_customer(self):
        '''Test deleting a customer from the database.'''
        customer_deleted = delete_customer(12345)

        self.assertTrue(customer_deleted)
        customer_in_db = Customer.get_or_none(Customer.customer_id == 12345)
        self.assertIsNone(customer_in_db)

    def test_update_customer_credit(self):
        '''Test updating a customer's credit.'''
        credit_updated = update_customer_credit(12345, 300000)
        new_credit = Customer.get(Customer.customer_id == 12345).credit_limit
        self.assertTrue(credit_updated)
        self.assertEqual(new_credit, 300000)

    def test_list_active_customers(self):
        '''Test list of active customers.'''
        count_active = list_active_customers()
        self.assertEqual(count_active, 2)

    def test_integration(self):
        '''Test multiple functions together.'''
        delete_customer(123)
        add_customer(999, 'Brad', 'Pitt', '157 Main St',
                     1000000000, 'BP@gmail.com', 'active',
                     400000)
        count_active = list_active_customers()
        self.assertEqual(count_active, 3)
        update_customer_credit(999, 100)
        brad = search_customer(999)
        self.assertEqual(brad['credit_limit'], 100)
