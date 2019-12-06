""" Tests for customer database module """
from unittest import TestCase
from customer_model import *
from basic_operations import *
from peewee import *
import sqlite3, traceback

class BasicOperationsTests(TestCase):
    """ Tests for basic_operations file """

    def test_add_customer(self):
        add_customer(customer_id=9,
          firstname='John',
          lastname='Deere',
          address='5555 Street',
          phone_no='509-888-9999',
          email='john.deere@gmail.com',
          status=1,
          credit_limit=4000)
        cust = Customer.get_by_id(9)
        self.assertEqual(cust.firstname, 'John')
        self.assertEqual(cust.phone_no, '509-888-9999')

    def test_add_invalid_customer(self):
        with self.assertRaises(IntegrityError) as cm:
            add_customer(customer_id=8,
              firstname=50,
              lastname=None,
              address='5555 Street',
              phone_no='509-888-9999',
              email='john.deere@gmail.com',
              status=1,
              credit_limit='invalid')

    def test_search_customer(self):
        test_dict = {'firstname':'John', 
         'lastname':'Deere', 
         'email':'john.deere@gmail.com', 
         'phone_no':'509-888-9999'}
        cust_dict = search_customer(9)
        self.assertEqual(cust_dict, test_dict)

    def test_update_customer_credit(self):
        update_customer_credit(9, 150000)
        cust_credit = Customer.get_by_id(9).credit_limit
        self.assertEqual(cust_credit, 150000)

    def test_list_active_customers(self):
        ct_active = list_active_customers()
        self.assertEqual(ct_active,1)
