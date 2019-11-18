# Advanced Programming In Python - Lesson 4 Assigmnet 1: Iterators, Generators and Comprehensions
# RedMine Issue - SchoolOps-14
# Code Poet: Anthony McKeever
# Start Date: 11/13/2019
# End Date: 11/14/2019

"""
Tests integration between basic_operations and customer_db_schema.
"""

from unittest import TestCase
from unittest.mock import MagicMock

import peewee
import basic_operations as BaseOps
from test_unit import MockCustomer

class TestIntegration(TestCase):
    """ Tests integration """

    def setUp(self):
        customer_mock = MockCustomer()

        # Mock Peewee as we don't need to test Peewee specific things.
        peewee.SqliteDatabase = MagicMock()
        peewee.SqliteDatabase.connect = MagicMock()
        peewee.execute_sql = MagicMock()
        peewee.Model.save = MagicMock()
        peewee.Model.delete = MagicMock()
        peewee.Model.get_or_create = MagicMock(return_value=[customer_mock])
        peewee.Model.get_or_none = MagicMock(return_value=customer_mock)
        peewee.Model.select = MagicMock()
        peewee.Model.select().where = MagicMock(return_value=[1, 2, 3])

    def test_integration(self):
        """
        Validates the intergration of the customer model and base_operations
        """
        BaseOps.add_customer("123",
                             "Amelia",
                             "Bedelia",
                             "123 Starshine Ln.",
                             "Pennsylvania 65000",
                             "amelia@rogersfamily.com",
                             "active",
                             3.14)

        customer = BaseOps.search_customer("123")

        self.assertEqual(customer,
                         MockCustomer.as_contact_info_dictionary(MockCustomer))

        BaseOps.update_customer_credit("123", 2.71)
        customer = BaseOps.Customers.get_or_none("123")
        self.assertEqual(customer.credit_limit, 2.71)

        BaseOps.delete_customer("123")
        self.assertEqual(3, BaseOps.list_active_customers())
