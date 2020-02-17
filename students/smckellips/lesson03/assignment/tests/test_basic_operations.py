#!/usr/bin/env python
from unittest import TestCase
from peewee import *
from basic_operations import *
from customer_model import Customer,DB

class TestBasicOperations(TestCase):
    '''Unit test class for testing basic_operations.'''

    def SetUp(self):
        self.db = DB
        self.db.drop_tables([Customer])
        self.db.create_tables([Customer])
        self.db.close()

        self.customer1 = {
            'customer_id': "Dexter",
            'name': 'Dexter',
            'lastname': 'Hamilton',
            'home_address': 'amkytflseg',
            'phone_number': '218-3604-29',
            'email_address': 'd.hamilton@washington.edu',
            'status': True,
            'credit_limit': 62649
        }
        self.customer2 = {
            'customer_id': "Carina",
            'name': 'Carina',
            'lastname': 'Bailey',
            'home_address': 'qkcuxswpmi',
            'phone_number': '914-4365-64',
            'email_address': 'c.bailey@aol.com',
            'status': True,
            'credit_limit': 81073
        }
        self.customer3 = {
            'customer_id': "Vanessa",
            'name': 'Vanessa',
            'lastname': 'Allen',
            'home_address': 'hlrxsenuzy',
            'phone_number': '857-5470-62',
            'email_address': 'v.allen@hotmail.com',
            'status': True,
            'credit_limit': 132266
        }
        self.customer4 = {
            'customer_id': "John",
            'name': 'John',
            'lastname': 'Adams',
            'home_address': 'tydzdtvgaf',
            'phone_number': '945-2288-69',
            'email_address': 'j.adams@gmail.com',
            'status': True,
            'credit_limit': 155810
        }
        self.customer5 = {
            'customer_id': "Valeria",
            'name': 'Valeria',
            'lastname': 'Tucker',
            'home_address': 'xszgdfovzd',
            'phone_number': '561-8608-77',
            'email_address': 'v.tucker@uw.edu',
            'status': True,
            'credit_limit': 83351
        }

    def test_add_customer(self):
        basic_operations.add_customer(**self.customer1)
        check = Customer.get(Customer.customer_id='Dexter')
        self.assertEqual(Customer.get(Customer.customer_id='Dexter'), True)
        self.assertEqual(check.credit_limit, 62649)
        pass

    def test_search_customer(self):
        pass

    def test_delete_customer(self):
        pass

    def test_update_customer_credit(self):
        pass

    def test_list_active_customers(self):
        pass

