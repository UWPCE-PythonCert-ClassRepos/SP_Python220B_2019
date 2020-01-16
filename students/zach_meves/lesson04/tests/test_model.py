"""
Test the customer model.
"""

import unittest
import peewee as pw
import os
import sys
from itertools import cycle, count, tee

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

    def test_create_add_customers(self):
        """Tests creating and adding numerous customers to database."""

        # Add all people to database
        for i, fname, lname, addr, phone, email, status, limit in \
                zip(range(1, self.num_customers + 1), self.fnames, self.lnames,
                    self.addresses, self.phones, self.emails,
                    self.statuses, self.credit_limits):
            created = Customer.create(id=i, name=fname, last_name=lname, address=addr,
                                      phone=phone, email=email, status=status, credit_limit=limit)
            created.save()

        # Assert have self.num_customers customers in DB
        customer_count = Customer.select().count()
        self.assertEqual(self.num_customers, customer_count)

    def test_create_dup(self):
        """Tests creating a customer with same ID."""

        customer = {'id': 1, 'name': 'Bob', 'last_name': 'Xavi',
                    'address': '123', 'phone': '412-569-8467',
                    'email': 'me@gmail.com', 'status': True,
                    'credit_limit': 100}

        created = Customer.create(**customer)

        with self.assertRaises(pw.IntegrityError):
            created = Customer.create(**customer)
