"""
Test the operations.
"""

import unittest
import peewee as pw
import os
import sys
from itertools import cycle, count

_dir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.dirname(_dir))
from customer_model import Customer
import basic_operations as bo

TEST_DB = pw.SqliteDatabase(':memory:')


class TestOperations(unittest.TestCase):
    """Test all basic operations."""

    def setUp(self) -> None:
        TEST_DB.bind([Customer])
        TEST_DB.connect()
        TEST_DB.create_tables([Customer])

        self.labels = ('id', 'name', 'last_name', 'address', 'phone', 'email',
                       'status', 'credit_limit')

        self.num_customers = 4  # Number of customers to create

        # Use iterators/generators to build an arbitrary number of test customers, without needing to
        # create Python-versions of all customers in memory
        self.fnames = cycle(["Bob", "Alice"])
        self.lnames = cycle(["Xavi", "Wond", "Xavi", "Erland", "Shark"])
        self.addresses = cycle(['505 N Thayer', '507 N Thayer', '509 S Main'])
        self.phones = (f"{a}-{b}-{c}" for a, b, c in zip(cycle(['713', '281']), cycle(['874', '564', '123']),
                                                         cycle(['1234', '5678', '1298', '3452'])))
        self.emails = (f"email_no{x}@gmail.com" for x in count(1))
        self.statuses = cycle([True, False])
        self.credit_limits = cycle([1000, 2000, 3000, 4000])

        # Create a generator for tuples used to create each customer
        self.def_tuples = ((i, f, l, a, p, e, s, c) for i, f, l, a, p, e, s, c in
                           zip(range(1, self.num_customers + 1), self.fnames,
                               self.lnames, self.addresses, self.phones,
                               self.emails, self.statuses, self.credit_limits))

        # Add first customer
        first_cust = next(self.def_tuples)
        self.first_cust = dict(zip(self.labels, first_cust))
        bo.add_customer(*first_cust)

        # self.definitions = {'Bob': {'id': 1, 'name': 'Bob', 'last_name': 'Xavi',
        #                             'address': "505 N Thayer", 'phone': '713-874-2356',
        #                             'email': 'bobxavi@comcast.net', 'status': True,
        #                             'credit_limit': 3400.12},
        #                     'Alice': {'id': 2, 'name': 'Alice', 'last_name': 'Wond',
        #                               'address': "507 N Thayer", 'phone': '713-874-0001',
        #                               'email': 'alice@gmail.com', 'status': False,
        #                               'credit_limit': 12000},
        #                     'Bob2': {'id': 3, 'name': 'Bob', 'last_name': 'Xavi',
        #                              'address': "509 S Main", 'phone': '281-874-2356',
        #                              'email': 'bobxavi2@comcast.net', 'status': True,
        #                              'credit_limit': 1}
        #                     }

        # # Add Bob
        # bob = self.definitions['Bob']
        # bo.add_customer(bob['id'], bob['name'], bob['last_name'], bob['address'],
        #                 bob['phone'], bob['email'], bob['status'], bob['credit_limit'])

    def tearDown(self) -> None:
        TEST_DB.drop_tables([Customer])
        TEST_DB.close()

    def test_add_customer(self):

        # Get second customer tuple
        second_cust = next(self.def_tuples)

        # Add second customer
        bo.add_customer(*second_cust)

        # Check that second customer is in DB
        res = Customer.get(Customer.id == second_cust[0])
        for attr, val in zip(self.labels, second_cust):
            self.assertEqual(val, getattr(res, attr))

        self.assertEqual(2, Customer.select().count())

        # Add second customer again - can't do this
        with self.assertRaises(ValueError):
            bo.add_customer(*second_cust)

    def test_search_customer(self):
        # Get first customer
        res = bo.search_customer(1)

        correct_labels = ['name', 'last_name', 'email', 'phone']
        for key in correct_labels:
            self.assertEqual(self.first_cust[key], res[key])
        self.assertListEqual(correct_labels, list(res.keys()))

        # Get non-existent ID
        res = bo.search_customer(-1)
        self.assertEqual({}, res)

    def test_delete_customer(self):

        self.assertGreater(Customer.select().count(), 0)

        # Delete first customer
        bo.delete_customer(self.first_cust['id'])

        self.assertEqual(0, Customer.select().count())

        # Delete non-existent ID
        bo.delete_customer(-1)

    def test_update_customer_credit(self):
        # Update first_cust's credit
        bo.update_customer_credit(1, 3000)

        first_cust = Customer.get(Customer.id == 1)
        self.assertEqual(3000, first_cust.credit_limit)

        # Update non-existent customer
        with self.assertRaises(ValueError):
            bo.update_customer_credit(-1, 100)

    def test_list_active_customers(self):
        self.assertEqual(1, bo.list_active_customers())

        counter = 1
        while True:  # Add all defined customers, check if status added correctly
            try:
                cust = next(self.def_tuples)
            except StopIteration:
                break
            else:
                status = cust[self.labels.index("status")]
                if status:
                    counter += 1
                bo.add_customer(*cust)
                self.assertEqual(counter, bo.list_active_customers())

    def test_integration(self):
        # Add customers 2 and 3
        c2, c3 = next(self.def_tuples), next(self.def_tuples)
        # alice = self.definitions['Alice']
        # bob2 = self.definitions['Bob2']

        bo.add_customer(*c2)
        bo.add_customer(*c3)

        # bo.add_customer(alice['id'], alice['name'], alice['last_name'], alice['address'],
        #                     alice['phone'], alice['email'], alice['status'], alice['credit_limit'])
        # bo.add_customer(bob2['id'], bob2['name'], bob2['last_name'], bob2['address'],
        #                     bob2['phone'], bob2['email'], bob2['status'], bob2['credit_limit'])

        # Assert that all 3 are in the DB
        self.assertEqual(3, Customer.select().count())

        # Modify c2's credit limit
        bo.update_customer_credit(c2[0], 12.32)
        self.assertEqual(12.32, float(Customer.get(Customer.name == c2[1]).credit_limit))

        # Search for c3
        res = bo.search_customer(c3[0])
        for k in ['name', 'last_name', 'email', 'phone']:
            self.assertEqual(c3[self.labels.index(k)], res[k])

        # Delete c3
        bo.delete_customer(c3[0])
        res = bo.search_customer(c3[0])
        self.assertEqual({}, res)
