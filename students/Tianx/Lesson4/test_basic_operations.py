"""
Unittest for basic_operations
"""
# pylint: disable = W0614, W0401, C0301, C0114,R0913,W0703,W1203
from unittest import TestCase
import sys
sys.path.append('./src')
from os import path
from customer_model import Customer
from basic_operations import add_customer, search_customer, delete_customer,\
    update_customer_credit, list_active_customers, display_customer_credit
from peewee import DoesNotExist


class TestBasicOperations(TestCase):
    """
    Unit tests
    """
    def test_db(self):
        """tests db creation"""
        self.assertTrue(path.exists("customers.db"))

    def test_add_customer(self):
        """tests add_customer function"""
        add_customer("C00001",
                     "Tim",
                     "Cook",
                     "123 fake st, Seattle, WA",
                     "206-123-4567",
                     "timc@apple.com",
                     True,
                     10000.00)
        self.assertEqual(Customer.get(Customer.customer_id == "C00001").first_name, "Tim")
        delete_customer('C00001')

    def test_search_customer(self):
        """tests search_customer function"""
        add_customer("C00001",
                     "Tim",
                     "Cook",
                     "123 fake st, Seattle, WA",
                     "206-123-4567",
                     "timc@apple.com",
                     True,
                     10000.00)
        actual = search_customer('C00001')
        expected = {'first_name': 'Tim',
                    'last_name': 'Cook',
                    'email':  'timc@apple.com',
                    'phone_number': '206-123-4567'}
        self.assertEqual(actual, expected)
        delete_customer('C00001')

    def test_update_customer_credit(self):
        """tests update_customer_credit function"""
        add_customer("C00001",
                     "Tim",
                     "Cook",
                     "123 fake st, Seattle, WA",
                     "206-123-4567",
                     "timc@apple.com",
                     True,
                     10000.00)
        update_customer_credit('C00001', 50000.00)
        self.assertEqual(Customer.get(Customer.customer_id == "C00001").credit_limit, 50000.00)
        delete_customer('C00001')

    def test_delete_customer(self):
        """tests delete_customer function"""
        add_customer("C00001",
                     "Tim",
                     "Cook",
                     "123 fake st, Seattle, WA",
                     "206-123-4567",
                     "timc@apple.com",
                     True,
                     10000.00)
        delete_customer('C00001')
        active_customers = list_active_customers()
        self.assertEqual(active_customers, 0)

    def test_delete_customer_not_found(self):
        """tests delete_customer function not found"""
        with self.assertRaises(DoesNotExist):
            delete_customer("C00003")

    def test_list_active_customers(self):
        """tests list_active_customers function"""
        add_customer("C00001",
                     "Tim",
                     "Cook",
                     "123 fake st, Seattle, WA",
                     "206-123-4567",
                     "timc@apple.com",
                     True,
                     10000.00)
        add_customer("C00002",
                     "Steve",
                     "Jobs",
                     "456 fake st, Seattle, WA",
                     "206-999-9999",
                     "stevej@apple.com",
                     True,
                     10000.00)
        active_customers = Customer.select().where(Customer.active_status).count()
        self.assertEqual(active_customers, 2)
        delete_customer('C00001')
        delete_customer('C00002')

    def test_list_active_customers_not_found(self):
        """tests list_active_customers function when not found"""
        with self.assertRaises(DoesNotExist):
            update_customer_credit("C00003", 500)

    def test_display_customer_credit(self):
        """tests display_customer_credit"""
        add_customer("C00001",
                     "Tim",
                     "Cook",
                     "123 fake st, Seattle, WA",
                     "206-123-4567",
                     "timc@apple.com",
                     True,
                     5000.00)
        add_customer("C00002",
                     "Steve",
                     "Jobs",
                     "456 fake st, Seattle, WA",
                     "206-999-9999",
                     "stevej@apple.com",
                     True,
                     10000.00)
        self.assertEqual(display_customer_credit(10000),
                         ['Nmae:Steve Jobs, Phone number:206-999-9999, Credit limist:10000'])

