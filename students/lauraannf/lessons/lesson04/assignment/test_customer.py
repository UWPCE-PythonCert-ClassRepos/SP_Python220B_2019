# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:30:07 2019

@author: Laura.Fiorentino
"""

from unittest import TestCase, mock
from unittest.mock import patch
from peewee import *
from customer_model import Customer
from basic_operations import *

MODELS = [Customer]

# use an in-memory SQLite for tests.
TEST_DB = SqliteDatabase(':memory:')

CUSTOMERS = [
    ('00001', 'Dorothy', 'Zbornak', 'Miami', '5551234567',
     'd.zbornak@gmail.com', True, 1000),
    ('00002', 'Sophia', 'Petrillo', 'Miami', '5551234568',
     's.petrillo@gmail.com', True, 1000),
    ('00003', 'Blanche', 'Devereaux', 'Miami', '5551234569',
     'b.devereaux@gmail.com', True, 5000),
    ('00004', 'Rose', 'Nylund', 'Miami', '5551234570',
     'r.nylund@gmail.com', False, 2000),
    ('00005', 'Stan', 'Zbornak', 'Hawaii', '555',
     's.zbornak@gmail.com', False, 100),
    ]

class BaseTestCase(TestCase):
    """ test for customer database"""
    def setUp(self):
        TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TEST_DB.connect()
        TEST_DB.create_tables(MODELS)

    def tearDown(self):
        TEST_DB.drop_tables(MODELS)
        TEST_DB.close()

    def test_add_customer(self):
        """ tests add_customer"""
        TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TEST_DB.create_tables(MODELS)
        add_customer(*CUSTOMERS[0])
        test_c1 = Customer.get_by_id('00001')
        self.assertEqual(test_c1.customer_ID, '00001')
        self.assertEqual(test_c1.first_name, 'Dorothy')
        self.assertEqual(test_c1.last_name, 'Zbornak')
        self.assertEqual(test_c1.home_address, 'Miami')
        self.assertEqual(test_c1.phone_number, '5551234567')
        self.assertEqual(test_c1.email_address, 'd.zbornak@gmail.com')
        self.assertEqual(test_c1.status, True)
        self.assertEqual(test_c1.credit_limit, 1000)
        test_c1 = add_customer(*CUSTOMERS[0])
        self.assertRaises(Exception)
        test_c1 = add_customer(*CUSTOMERS[4])
        self.assertRaises(Exception)

    def test_search_customer(self):
        """tests search"""
        TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TEST_DB.create_tables(MODELS)
        add_customer(*CUSTOMERS[0])
        test_c2 = search_customer('00001')
        self.assertEqual({'Customer ID': '00001', 'First Name': 'Dorothy',
                          'Last Name': 'Zbornak', 'Home Address': 'Miami',
                          'Phone Number': '5551234567',
                          'Email Address': 'd.zbornak@gmail.com',
                          'Status': 'Active', 'Credit Limit': 1000}, test_c2)
        add_customer(*CUSTOMERS[3])
        test_c2 = search_customer('00004')
        self.assertEqual({'Customer ID': '00004', 'First Name': 'Rose',
                          'Last Name': 'Nylund', 'Home Address': 'Miami',
                          'Phone Number': '5551234570',
                          'Email Address': 'r.nylund@gmail.com',
                          'Status': 'Inactive', 'Credit Limit': 2000}, test_c2)
        test_c2 = search_customer('00009')
        self.assertRaises(Exception)

    def test_delete_customer(self):
        """ tests delete customer"""
        TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TEST_DB.create_tables(MODELS)
        add_customer(*CUSTOMERS[0])
        add_customer(*CUSTOMERS[1])
        delete_customer('00001')
        test_c3 = search_customer('00001')
        self.assertRaises(Exception)

    def test_update_customer_credit(self):
        """ tests updating the customer credit"""
        TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TEST_DB.create_tables(MODELS)
        add_customer(*CUSTOMERS[0])
        update_customer_credit('00001', 5000)
        test_c4 = search_customer('00001')
        self.assertEqual(test_c4['Credit Limit'], 5000)
        test_c4 = search_customer('00008')
        self.assertRaises(Exception)
    def test_list_active_customer(self):
        """tests counting number of active customers"""
        TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TEST_DB.create_tables(MODELS)
        for customer in CUSTOMERS:
            add_customer(*customer)
        test_c5 = list_active_customers()
        self.assertEqual(test_c5, 3)
