# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 17:48:18 2019

@author: Humberto
"""

from unittest import TestCase
from assignment.basic_operations import add_customer
from assignment.basic_operations import search_customer
from assignment.basic_operations import delete_customer
from assignment.basic_operations import update_customer_credit
from assignment.basic_operations import list_active_customers
from assignment.customer_model import DATABASE as database
from assignment.customer_model import Customer

class TestBasicOperations(TestCase):
    """tests for all basic operations"""
    def setUp(self):
        """sets up the tests"""
        database.create_tables([Customer])

    def tearDown(self):
        """Remves tables created by tests"""
        database.drop_tables([Customer])

    def test_add_customer(self):
        """tests the add_customer functionality"""
        added_customer = {'customer_id':'EJ9ER',
                          'first_name':'Jennifer',
                          'last_name':'Robot',
                          'home_address':'2324 Main Street',
                          'phone_number':'6197602020',
                          'email_address':'jenny@yahoo.com',
                          'status':'Active',
                          'credit_limit':15000.00}
        add_customer(**added_customer)
        result = Customer.get(Customer.customer_id == added_customer['customer_id'])
        self.assertEqual(result.customer_id, added_customer['customer_id'])

    def test_add_customer_fail(self):
        """tests the add_customer functionality"""
        added_customer = {'customer_id':'EJ9ER',
                          'first_name':'Jennifer',
                          'last_name':'Robot',
                          'home_address':'2324 Main Street',
                          'phone_number':'6197602020',
                          'email_address':'jenny@yahoo.com',
                          'status':'Active',
                          'credit_limit':15000.00}
        dupli_customer = {'customer_id':'EJ9ER',
                          'first_name':'Jennifer',
                          'last_name':'Robot',
                          'home_address':'2324 Main Street',
                          'phone_number':'6197602020',
                          'email_address':'jenny@yahoo.com',
                          'status':'Active',
                          'credit_limit':15000.00}
        add_customer(**added_customer)
        with self.assertRaises(ValueError):
            add_customer(**dupli_customer)

    def test_search_customer(self):
        """tests the search_customer functionality"""
        added_customer = {'customer_id':'EJ9ER',
                          'first_name':'Jennifer',
                          'last_name':'Robot',
                          'home_address':'2324 Main Street',
                          'phone_number':'6197602020',
                          'email_address':'jenny@yahoo.com',
                          'status':'Active',
                          'credit_limit':15000.00}
        add_customer(**added_customer)
        compare = {'first_name':'Jennifer',
                   'last_name':'Robot',
                   'phone_number':'6197602020',
                   'email_address':'jenny@yahoo.com'}
        result = search_customer(added_customer['customer_id'])
        self.assertEqual(compare, result)

    def test_search_customer_fail(self):
        """tests the search_customer functionality"""
        added_customer = {'customer_id':'EJ9ER',
                          'first_name':'Jennifer',
                          'last_name':'Robot',
                          'home_address':'2324 Main Street',
                          'phone_number':'6197602020',
                          'email_address':'jenny@yahoo.com',
                          'status':'Active',
                          'credit_limit':15000.00}
        add_customer(**added_customer)
        compare = {}
        self.assertEqual(compare, search_customer('LS123'))

    def test_delete_customer(self):
        """tests the delete_customer functionality"""
        added_customer = {'customer_id':'EJ9ER',
                          'first_name':'Jennifer',
                          'last_name':'Robot',
                          'home_address':'2324 Main Street',
                          'phone_number':'6197602020',
                          'email_address':'jenny@yahoo.com',
                          'status':'Active',
                          'credit_limit':15000.00}
        add_customer(**added_customer)
        self.assertEqual(delete_customer(added_customer['customer_id']), None)

    def test_delete_customer_fail(self):
        """tests the delete_customer functionality"""
        added_customer = {'customer_id':'EJ9ER',
                          'first_name':'Jennifer',
                          'last_name':'Robot',
                          'home_address':'2324 Main Street',
                          'phone_number':'6197602020',
                          'email_address':'jenny@yahoo.com',
                          'status':'Active',
                          'credit_limit':15000.00}
        add_customer(**added_customer)
        with self.assertRaises(ValueError):
            delete_customer('DNE745')

    def test_update_customer_credit(self):
        """tests the update_customer_credit functionality"""
        added_customer = {'customer_id':'EJ9ER',
                          'first_name':'Jennifer',
                          'last_name':'Robot',
                          'home_address':'2324 Main Street',
                          'phone_number':'6197602020',
                          'email_address':'jenny@yahoo.com',
                          'status':'Active',
                          'credit_limit':15000.00}
        add_customer(**added_customer)
        update_customer_credit(added_customer['customer_id'], 25000.00)
        customer_lu = Customer.get(Customer.customer_id == added_customer['customer_id'])
        self.assertEqual(float(customer_lu.credit_limit), 25000.00)

    def test_update_customer_credit_fail(self):
        """tests the update_customer_credit functionality"""
        added_customer = {'customer_id':'EJ9ER',
                          'first_name':'Jennifer',
                          'last_name':'Robot',
                          'home_address':'2324 Main Street',
                          'phone_number':'6197602020',
                          'email_address':'jenny@yahoo.com',
                          'status':'Active',
                          'credit_limit':15000.00}
        add_customer(**added_customer)
        with self.assertRaises(ValueError):
            update_customer_credit('DNE543', 25000.00)

    def test_list_active_customers(self):
        """tests the list_active_customers functionality"""
        added_customer = {'customer_id':'EJ9ER',
                          'first_name':'Jennifer',
                          'last_name':'Robot',
                          'home_address':'2324 Main Street',
                          'phone_number':'6197602020',
                          'email_address':'jenny@yahoo.com',
                          'status':'Active',
                          'credit_limit':15000.00}
        add_customer(**added_customer)
        added_customer_2 = {'customer_id':'CS194',
                            'first_name':'Cloud',
                            'last_name':'Strife',
                            'home_address':'2324 Acorn Avenue',
                            'phone_number':'4257774659',
                            'email_address':'Cloud@yahoo.com',
                            'status':'Active',
                            'credit_limit':15000.00}
        add_customer(**added_customer_2)
        result = list_active_customers()
        self.assertEqual(result, 2)
        