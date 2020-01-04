"""
Test the operations.
"""

import unittest
import peewee as pw
import os
import sys

_dir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.dirname(_dir))
from customer_model import Customer
import basic_operations as bo

DB = pw.SqliteDatabase(':memory:')


class TestOperations(unittest.TestCase):
    """Test all basic operations."""

    def setUp(self) -> None:
        DB.bind([Customer])
        DB.connect()
        DB.create_tables([Customer])

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

        # Add Bob
        bob = self.definitions['Bob']
        bo.add_customer(bob['id'], bob['name'], bob['last_name'], bob['address'],
                        bob['phone'], bob['email'], bob['status'], bob['credit_limit'])

    def tearDown(self) -> None:
        DB.drop_tables([Customer])
        DB.close()

    def test_add_customer(self):
        # Add Bob2
        bob = self.definitions['Bob2']
        bo.add_customer(bob['id'], bob['name'], bob['last_name'], bob['address'],
                        bob['phone'], bob['email'], bob['status'], bob['credit_limit'])

        # Check that Bob2 is in the database
        res = Customer.get(Customer.id == bob['id'])
        for attr, val in bob.items():
            self.assertEqual(val, getattr(res, attr))

        self.assertEqual(2, Customer.select().count())

        # Add Bob2 again - can't do this
        with self.assertRaises(ValueError):
            bo.add_customer(bob['id'], bob['name'], bob['last_name'], bob['address'],
                            bob['phone'], bob['email'], bob['status'], bob['credit_limit'])

    def test_search_customer(self):
        # Get Bob
        res = bo.search_customer(1)
        for key, val in res.items():
            self.assertEqual(self.definitions['Bob'][key], val)
        self.assertListEqual(list(res.keys()), ['name', 'last_name', 'email', 'phone'])

        # Get non-existent ID
        res = bo.search_customer(6)
        self.assertEqual({}, res)

    def test_delete_customer(self):

        self.assertGreater(Customer.select().count(), 0)

        # Delete Bob
        bo.delete_customer(1)

        self.assertEqual(0, Customer.select().count())

        # # Delete non-existent ID
        # with self.assertRaises(ValueError):
        #     bo.delete_customer(6)

    def test_update_customer_credit(self):
        # Update Bob's credit
        bo.update_customer_credit(1, 3000)

        bob = Customer.get(Customer.id == 1)
        self.assertEqual(3000, bob.credit_limit)

    def test_list_active_customers(self):
        self.assertEqual(1, bo.list_active_customers())

        bo.add_customer(2, 'new', 'last', 'abc', '123', 'abc', True, 100)
        self.assertEqual(2, bo.list_active_customers())

    def test_integration(self):
        # Add Alice and Bob2
        alice = self.definitions['Alice']
        bob2 = self.definitions['Bob2']

        bo.add_customer(alice['id'], alice['name'], alice['last_name'], alice['address'],
                            alice['phone'], alice['email'], alice['status'], alice['credit_limit'])
        bo.add_customer(bob2['id'], bob2['name'], bob2['last_name'], bob2['address'],
                            bob2['phone'], bob2['email'], bob2['status'], bob2['credit_limit'])

        # Assert that all 3 are in the DB
        self.assertEqual(3, Customer.select().count())

        # Modify Alice's credit limit
        bo.update_customer_credit(alice['id'], 12.32)
        self.assertEqual(12.32, Customer.get(Customer.name == 'Alice').credit_limit)

        # Search for Bob2
        res = bo.search_customer(bob2['id'])
        for k in ['id', 'name', 'last_name', 'email', 'phone']:
            self.assertEqual(bob2[k], res[k])

        # Delete Bob2
        bo.delete_customer(bob2['id'])
        res = bo.search_customer(bob2['id'])
        self.assertEqual({}, res)
