"""
Test the customer model.
"""

import unittest
import peewee as pw
import os
import sys

_dir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.dirname(_dir))
from customer_model import Customer

TEST_DB = pw.SqliteDatabase(':memory:')


class TestCustomer(unittest.TestCase):
    """Test the Customer model."""

    db = None

    def setUp(self) -> None:

        TEST_DB.bind([Customer])
        TEST_DB.connect()
        TEST_DB.create_tables([Customer])

        self.definitions = {'Bob': {'id': 1, 'name': 'Bob', 'last_name': 'Xavi',
                                    'address': "505 N Thayer", 'phone': '713-874-2356',
                                    'email': 'bobxavi@comcast.net', 'status': True,
                                    'credit_limit': 3400.12},
                            'Alice': {'id': 2, 'name': 'Alice', 'last_name': 'Wond',
                                      'address': "507 N Thayer", 'phone': '713-874-0001',
                                      'email': 'alice@gmail.com', 'status': False,
                                      'credit_limit': 12000},
                            'Bob2': {'id': 3, 'name': 'Bob', 'last_name': 'Xavi',
                                     'address': "509 S Main", 'phone': '281-874-2356',
                                     'email': 'bobxavi2@comcast.net', 'status': True,
                                     'credit_limit': 1}
                            }

        # Add all 3 people to database
        for person, defin in self.definitions.items():
            created = Customer.create(**defin)
            created.save()

    def tearDown(self) -> None:
        # Delete everything from database
        TEST_DB.drop_tables([Customer])
        TEST_DB.close()

    def test_create_customer(self):
        """Tests creating a customer."""

        new_cust = {'id': 5, 'name': 'Bob', 'last_name': 'Xavi',
                    'address': "509 S Main", 'phone': '281-874-2356',
                    'email': 'bobxavi2@comcast.net', 'status': True,
                    'credit_limit': 1}

        created = Customer.create(**new_cust)

        # Assert that customer was created correctly
        for attr, val in new_cust.items():
            self.assertEqual(val, getattr(created, attr))

    def test_create_dup(self):
        """Tests creating a customer with same ID."""

        with self.assertRaises(Exception):
            created = Customer.create(**self.definitions['Bob'])




