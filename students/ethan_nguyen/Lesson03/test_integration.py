from unittest import TestCase
from unittest.mock import patch
import pytest

import basic_operations

gold = {'id': 1, 'name': 'Michael', 'last_name': 'Jordan', 'home_address': '3421 S Bull \
Street North Carolina', 'phone_number': '203-231-3223',
        'email': 'goat_test@gmail.com', 'status': 'Active',
        'credit_limit': 212109}


class CustomerDBIntegrationTest(TestCase):

    def test_whole_system(self):
        '''make sure the database is exist'''
        self.assertIsNotNone(basic_operations.DATABASE)

        '''make sure the Customer table exist'''
        self.assertIsNotNone(basic_operations.Customer)

        '''start with an empty database'''
        basic_operations.delete_all_customers()

        '''add a new customer'''
        basic_operations.add_customer(1, 'Michael', 'Jordan', '3421 S Bull Street \
North Carolina', '203-231-3223', 'goat_test@gmail.com', 'Active', 212109)

        customer = basic_operations.search_customer(1)
        self.assertDictEqual(gold, customer)

        '''add another customer'''
        basic_operations.add_customer(2, 'Shawn', 'Kemp', '3423 Green Lake \
Street Seattle WA', '206-240-4023', 'dunk_test@gmail.com', 'Active', 212109)

        count = basic_operations.list_active_customers()
        self.assertEqual(2, count)

        '''update customer 1 credit'''
        basic_operations.update_customer_credit(1, 200)
        customer = basic_operations.search_customer(1)
        self.assertEqual(200, customer['credit_limit'])

        '''update non-exist customer and catch the error'''
        try:
            basic_operations.update_customer_credit(10, 300)
        except ValueError:
            self.assertRaises(ValueError)

        '''delete customer 1'''
        basic_operations.delete_customer(1)
        customer = basic_operations.search_customer(1)
        self.assertIsNone(customer)
