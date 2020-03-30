""" test customer_model operations """

from unittest import TestCase
from customer_model import *
import basic_operations as bo
import peewee as pw

class BasicTests(TestCase):

    def test_a_add_customer(self):
        name = "Aaren"
        lastname = "Sue"
        home_address = "123 100 st, Bothell, WA 98044"
        phone_number = 1234567899
        email_address = "asue@uw.edu"
        status = 1
        credit_limit = 2000

        a_customer = bo.add_customer(name, lastname, home_address, phone_number, email_address,
                                     status, credit_limit)
        customer_id = 1

        self.assertEqual(customer_id, a_customer.customer_id)
        self.assertEqual(name, a_customer.name)
        self.assertEqual(lastname, a_customer.lastname)
        self.assertEqual(home_address, a_customer.home_address)
        self.assertEqual(phone_number, a_customer.phone_number)
        self.assertEqual(email_address, a_customer.email_address)
        self.assertEqual(status, a_customer.status)
        self.assertEqual(credit_limit, a_customer.credit_limit)

        a_customer = bo.add_customer(name, lastname, home_address, phone_number,
                                     email_address, status, credit_limit)


    def test_b_search_customer(self):
        expected =  {'name': "Aaren",
                     'lastname': "Sue",
                     'phone_number': 1234567899,
                     'email_address': "asue@uw.edu"}
        self.assertEqual (expected, bo.search_customer(1))


    def test_c_update_customer_credit(self):
        expected = 3000
        bo.update_customer_credit(1, 3000)
        a_customer = Customer.get(Customer.customer_id == 1)
        self.assertEqual(expected, a_customer.credit_limit)


    def test_d_list_active_customers(self):
        expected = 1
        self.assertEqual(expected, bo.list_active_customers())


    def test_e_delete_customer(self):
        bo.delete_customer(1)
        try:
            a_customer = Customer.get(Customer.customer_id == 1)
            raise Exception
        except pw.DoesNotExist:
            pass


    def test_f_search_customer_empty(self):
        expected =  {}
        self.assertEqual (expected, bo.search_customer(1))


    def test_g_list_active_customers_empty(self):
        expected = 0
        self.assertEqual(expected, bo.list_active_customers())
