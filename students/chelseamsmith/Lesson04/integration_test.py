# pylint: disable=W0401, W0614

"""Customer Model integration test"""
from unittest import TestCase
from peewee import *
from customer_model import *
from basic_operations import add_customer, delete_customer
from basic_operations import list_active_customers

DB.init('integrationtest.db')
DB.create_tables([Customer])

class IntegrationTest(TestCase):
    """integration test for basic_operations.py"""

    def test_one(self):
        """tests add customer, delete customer, and list active customers"""
        add_customer(123, "Bob", "Smith", "123 Lane Lane", "123-4567",
                     "bob@gmail.com", True, 10000)
        add_customer(456, "Jane", "Jones", "456 Road Road", "234-5678",
                     "jane@gmail.com", True, 20000)
        add_customer(789, "Alice", "Doe", "789 Street Street", "345-6789",
                     "alice@gmail.com", False, 30000)
        delete_customer(456)
        actual = list_active_customers()
        self.assertEqual(actual, 1)
