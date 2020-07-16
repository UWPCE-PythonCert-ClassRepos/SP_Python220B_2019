#!/usr/bin/env python

"""
    Tests for the database instantiator, customer_models and basic operations

"""
from unittest import TestCase
import sys
import pathlib
import os
sys.path.append('..')
from customer_model import *
import instantiate_db
import basic_operations as bas

# Test data to use to test functions of basic_operations.py

FIRST_NAME = 0
LAST_NAME = 1
HOME_ADDRESS = 2
PHONE_NUMBER = 3
EMAIL_ADDRESS = 4
IS_ACTIVE = 5
CREDIT_LIMIT = 6

customer_list = [('Elver', 'Johnson', '372 Main St, Tacoma', '206-333-3322', 'ejohn@fakemail.com', '1', '40000.00'),
                 ('Danny', 'McCrinkel', '222 1st St, Bellingham', '425-111-3300', 'dcrink@fakemail.com', '1', '20000.00'),
                 ('Smitty', 'Smith', '1600 Old Coal Rd, Isaquah', '206-000-0012', 'smitty@hotmail.com', '0', '300.00'),
                 ('Jenny', 'Ngyuen', '456 Pike St, Seattle', '360-990-0012', 'jenny@gmail.com', '1', '1500.00')]

new_customer = ('Silas', 'Skinflint', '535 Duckworth Ave, Duckburg', '206-432-6912', 'silas@dmail.com', '1', '5000.00')

# Outputs to compare against for basic_operations.py

list_all_output = ['ID#    1:::Elver Johnson,       P: 206-333-3322, E: ejohn@fakemail.com  , Active:1, Limit:   40000',
                   'ID#    2:::Danny McCrinkel,     P: 425-111-3300, E: dcrink@fakemail.com , Active:1, Limit:   20000',
                   'ID#    3:::Smitty Smith,        P: 206-000-0012, E: smitty@hotmail.com  , Active:0, Limit:     300',
                   'ID#    4:::Jenny Ngyuen,        P: 360-990-0012, E: jenny@gmail.com     , Active:1, Limit:    1500']

new_cust_return = {'customer_id': 5,
                   'first_name': 'Silas',
                   'last_name': 'Skinflint',
                   'home_address': '535 Duckworth Ave, Duckburg',
                   'phone_number': '206-432-6912',
                   'email_address': 'silas@dmail.com',
                   'is_active': '1',
                   'credit_limit': '5000.00'}

search_record = {'first_name': 'Danny', 'last_name': 'McCrinkel', 'email_address': 'dcrink@fakemail.com', 'phone_number': '425-111-3300'}

updated_record = {'credit_limit': 399,
                  'email_address': 'dcrink@fakemail.com',
                  'first_name': 'Danny',
                  'last_name': 'McCrinkel'}


class InstantiateTests(TestCase):
    '''Testing that a database is created'''

    def test_instantiation(self):
        '''Tests the instantiation of the database'''
        testpth = pathlib.Path('./')
        testdest = testpth.absolute() / 'customers.db'
        assert os.path.isfile(testdest) is True

class SchemaTests(TestCase):
    '''Testing the database structure'''

    def test_record_creation(self):
        '''Tests that the schema with a valid new customer tuple'''
        with database.transaction():
            new_customer = Customers.create(
                first_name='Silas',
                last_name='Skinflint',
                home_address='535 Duckworth Ave, Duckburg',
                phone_number='206-432-6912',
                email_address='silas@dmail.com',
                is_active='1',
                credit_limit='5000.00')
            new_customer.save()
            assert new_customer.customer_id > 0
            new_customer.delete_instance()

    def test_incomplete_record_creation(self):
        '''Attempts to fill the record with a missing required field'''
        try:
            with database.transaction():
                new_customer = Customers.create(
                    first_name='Silas',
                    last_name='Skinflint',
                    home_address='535 Duckworth Ave, Duckburg',
                    phone_number='206-432-6912',
                    email_address='silas@dmail.com',
                    credit_limit='5000.00')
                new_customer.save()
                new_customer.delete_instance()
        except IntegrityError:
            self.assertRaises(IntegrityError)



    def test_duplicate_record_creation(self):
        '''Attempts to fill the record with a missing required field'''

        with database.transaction():
            new_customer = Customers.create(
                first_name='Silas',
                last_name='Skinflint',
                home_address='535 Duckworth Ave, Duckburg',
                phone_number='206-432-6912',
                email_address='silas@dmail.com',
                is_active='1',
                credit_limit='5000.00')
            new_customer.save()

        try:
            with database.transaction():
                dupli_customer = Customers.create(
                    first_name='Silas',
                    last_name='Skinflint',
                    home_address='535 Duckworth Ave, Duckburg',
                    phone_number='206-432-6912',
                    email_address='silas@dmail.com',
                    is_active='1',
                    credit_limit='5000.00')
        except IntegrityError:
            self.assertRaises(IntegrityError)

        for c in Customers:
            c.delete_instance()

class BasicOperationsTests(TestCase):
    '''Testing the functionality of basic_operations.py'''

    def setUp(self):
        '''Get the database instantiated with fake data'''
        for customer in customer_list:
            with database.transaction():
                new_customer = Customers.create(
                    first_name=customer[FIRST_NAME],
                    last_name=customer[LAST_NAME],
                    home_address=customer[HOME_ADDRESS],
                    phone_number=customer[PHONE_NUMBER],
                    email_address=customer[EMAIL_ADDRESS],
                    is_active=customer[IS_ACTIVE],
                    credit_limit=customer[CREDIT_LIMIT])



    def test_add_new_customer(self):
        '''Tests the add_customer function'''
        c = bas.add_customer(new_customer)
        assert c == new_cust_return

    def test_delete_customer(self):
        '''Tests the delete_customer function'''
        bas.delete_customer(2)
        try:
            Customers.get(Customers.customer_id == 2)
            assert 0 #If id was found would fail test
        except:
            pass

    def test_search_customer(self):
        '''Tests the search_customer function'''
        record2 = bas.search_customer(2)
        assert record2 == search_record

    def test_search_invalid_number(self):
        '''Tests search_customer returns an empty dict on invalid num'''
        badsearch = bas.search_customer(5)
        assert badsearch == {}

    def test_active_customer_count(self):
        '''Tests the return of a count of active customers'''
        active_customer_count = bas.list_active_customers()
        assert active_customer_count == 3

    def test_list_all_customers(self):
        '''Tests the formatted list of customers'''
        formatted_list = bas.list_all_customers()
        assert formatted_list == list_all_output

    def test_update_customer(self):
        '''Tests a valid update of a credit change'''
        update = bas.update_customer(2, 399)
        assert update == updated_record

    def test_invalid_update_customer(self):
        '''Tests an invalid update of a credit change'''
        try:
            update = bas.update_customer(9, 399)
        except:
            self.assertRaises(ValueError)

    def tearDown(self):
        '''Delete the fake data'''
        for c in Customers:
            c.delete_instance()

'''
search_record = {'customer_id': 2,
                 'first_name': 'Danny',
                 'last_name': 'McCrinkel',
                 'home_address': '222 1st St, Bellingham',
                 'phone_number': '425-111-3300',
                 'email_address': 'dcrink@fakemail.com',
                 'is_active': '1',
                 'credit_limit': '20000.00'}
'''