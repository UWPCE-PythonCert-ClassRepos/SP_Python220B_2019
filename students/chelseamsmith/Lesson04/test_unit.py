# pylint: disable=W0401, W0614

"""Customer Model unit tests"""
from unittest import TestCase
from peewee import *
from customer_model import *
from basic_operations import add_customer, search_customer, delete_customer
from basic_operations import update_customer_credit, list_active_customers

DB.init('test.db')

def create_db():
    """creates an empty db"""
    DB.drop_tables([Customer])
    DB.create_tables([Customer])


class BasicOperationsTests(TestCase):
    """tests functions in basic_operations.py"""

    def test_add_customers(self):
        """tests add_customer function"""
        create_db()
        add_customer(123, "Bob", "Smith", "123 Lane Lane", "123-4567",
                     "bob@gmail.com", True, 10000)
        query = Customer.get(Customer.customer_id == 123)
        self.assertEqual(123, query.customer_id)
        self.assertEqual("Bob", query.name)
        self.assertEqual("Smith", query.last_name)
        self.assertEqual("123 Lane Lane", query.home_address)
        self.assertEqual("123-4567", query.phone_number)
        self.assertEqual("bob@gmail.com", query.email_address)
        self.assertEqual(True, query.status)
        self.assertEqual(10000, query.credit_limit)

    def test_search_customer_success(self):
        """tests search customer function"""
        create_db()
        add_customer(123, "Bob", "Smith", "123 Lane Lane", "123-4567",
                     "bob@gmail.com", True, 10000)
        add_customer(456, "Jane", "Jones", "456 Road Road", "234-5678",
                     "jane@gmail.com", True, 20000)
        actual = search_customer(456)
        expected = {"name": "Jane", "last name" : "Jones",
                    "email address" : "jane@gmail.com", "phone number" : "234-5678"}
        self.assertEqual(actual, expected)

    def test_search_customer_fail(self):
        """tests search customer function"""
        create_db()
        add_customer(123, "Bob", "Smith", "123 Lane Lane", "123-4567",
                     "bob@gmail.com", True, 10000)
        add_customer(456, "Jane", "Jones", "456 Road Road", "234-5678",
                     "jane@gmail.com", True, 20000)
        actual = search_customer(234)
        expected = {}
        self.assertEqual(actual, expected)

    def test_delete_customer(self):
        """tests delete customer function"""
        create_db()
        add_customer(123, "Bob", "Smith", "123 Lane Lane", "123-4567",
                     "bob@gmail.com", True, 10000)
        add_customer(456, "Jane", "Jones", "456 Road Road", "234-5678",
                     "jane@gmail.com", True, 20000)
        delete_customer(123)
        actual = search_customer(123)
        self.assertEqual(actual, {})

    def test_delete_custome_error(self):
        """tests delete_customer exception block"""
        create_db()
        self.assertRaises(ValueError, delete_customer, 123)

    def test_update_customer_credit(self):
        """tests update_customer_credit"""
        create_db()
        add_customer(123, "Bob", "Smith", "123 Lane Lane", "123-4567",
                     "bob@gmail.com", True, 10000)
        update_customer_credit(123, 15000)
        query = Customer.get(Customer.customer_id == 123)
        self.assertEqual(query.credit_limit, 15000)

    def test_update_customer_credit_error(self):
        """tests update_customer_credit exception block"""
        create_db()
        self.assertRaises(ValueError, update_customer_credit, 234, 15000)

    def test_list_active_customers(self):
        """tests list active customers function"""
        create_db()
        add_customer(123, "Bob", "Smith", "123 Lane Lane", "123-4567",
                     "bob@gmail.com", True, 10000)
        add_customer(456, "Jane", "Jones", "456 Road Road", "234-5678",
                     "jane@gmail.com", True, 20000)
        add_customer(789, "Alice", "Doe", "789 Street Street", "345-6789",
                     "alice@gmail.com", False, 30000)
        actual = list_active_customers()
        self.assertEqual(actual, 2)
