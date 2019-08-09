"""Tests basic_operations.py"""

import sys
sys.path.append("../src")
from peewee import *
from customer_schema import *
from basic_operations import *
from unittest import TestCase


def setup():
    database.drop_tables([Customer])
    database.create_tables([Customer])
    database.close()


class TestingBasicOperations(TestCase):

    def test_add_customer(self):
        setup()
        test_customer = ('42', 'Ron', 'Swanson', 'Pawnee, Ind', '773-202-LUNA',
                         'whiskeybusiness@aol.com', True, 500)
        add_customer(*test_customer)
        test = Customer.get(Customer.customer_id == '42')
        self.assertEqual(test.first_name, 'Ron')
        self.assertEqual(test.last_name, 'Swanson')
        self.assertEqual(test.address, 'Pawnee, Ind')
        self.assertEqual(test.phone, '773-202-LUNA')
        self.assertEqual(test.email, 'whiskeybusiness@aol.com')
        self.assertEqual(test.status, True)
        self.assertEqual(test.credit_limit, 500)

        #   Test failing case
        with self.assertRaises(IntegrityError):
            #   Tries to add the same customer/same ID
            add_customer(*test_customer)

    def test_search_customer(self):
        setup()
        test_customer = ('42', 'Ron', 'Swanson', 'Pawnee, Ind', '773-202-LUNA',
                         'whiskeybusiness@aol.com', True, 500)
        add_customer(*test_customer)
        retrieved_data = search_customer('42')
        expected_data = {'Name' : 'Ron','Last Name' : 'Swanson',
                'Email': 'whiskeybusiness@aol.com', 'Phone Number': '773-202-LUNA'}
        self.assertEqual(retrieved_data, expected_data)

        '''Test negative case (ID not found)'''
        nonexisting_search = search_customer('345')
        self.assertEqual(nonexisting_search,{})

    def test_delete_customer(self):
        setup()
        test_customer = ('42', 'Ron', 'Swanson', 'Pawnee, Ind', '773-202-LUNA',
                         'whiskeybusiness@aol.com', True, 500)
        add_customer(*test_customer)
        delete_customer('42')

        '''Tests customer not existing'''
        with self.assertRaises(DoesNotExist):
            '''Uses an invalid customer ID'''
            delete_customer('12')

    def test_update_customer_credit(self):
        setup()
        test_customer = ('42', 'Ron', 'Swanson', 'Pawnee, Ind', '773-202-LUNA',
                         'whiskeybusiness@aol.com', True, 500)
        add_customer(*test_customer)
        update_customer_credit('42', 700)
        test_cust = Customer.get(Customer.customer_id == '42')
        self.assertEqual(test_cust.credit_limit, 700)

        '''Tests customer not existing'''
        with self.assertRaises(DoesNotExist):
            '''Uses an invalid customer ID'''
            update_customer_credit('12',750)

    def test_list_active_customers(self):
        setup()
        test_customer = ('42', 'Ron', 'Swanson', 'Pawnee, Ind', '773-202-LUNA',
                         'whiskeybusiness@aol.com', True, 500)
        add_customer(*test_customer)
        self.assertEqual(list_active_customers(), 1)

    def test_list_customer_names(self):
        setup()
        customers_to_add = [
            ('123', 'Harry', 'Potter', 'London', '7503456234', 'magictouch@hogwarts.com',
             True, 750), ('456', 'Bob', 'Vance', 'Scranton', '9573930342',
                          'keepcool@vancefridge.com', True, 600),
            ('789', 'Luke', 'Skywalker', 'Tattooine', '6574839475', 'xwingpilot@rebel.com',
             True, 300)]

        for person in customers_to_add:
            add_customer(*person)

        test_list = ['123: Potter, Harry', '456: Vance, Bob', '789: Skywalker, Luke']
        self.assertEqual(list_customer_names(), test_list)
