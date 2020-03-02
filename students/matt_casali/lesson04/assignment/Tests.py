#!/usr/bin/env python3

""" Unit testing for basic_operations.py """

# pylint: disable= W0614, C0103, W0401

from unittest import TestCase
from basic_operations import *
from peewee import IntegrityError, DoesNotExist


test_customer = {'customer_id': 123,
                 'customer_name': 'Kota',
                 'customer_last_name': 'Smith',
                 'customer_address': '123 Fake Street',
                 'customer_phone_number': '123-456-7890',
                 'customer_email': 'wooooo@gmail.com',
                 'customer_status': 'active',
                 'customer_credit_limit': 100000.00}


class BasicOperationsTests(TestCase):
    """Class to test basic operations script """

    def setUp(self):
        """ Set up table """

    logger_setup()
    data.drop_tables([Customer])
    data.create_tables([Customer])

    def test_add_customer(self):
        """ Test adding customers """

        add_customer(**test_customer)
        test = Customer.get(Customer.customer_id == test_customer['customer_id'])
        self.assertEqual(test.customer_id, test_customer['customer_id'])

        # Make sure test fails
        with self.assertRaises(IntegrityError):
            add_customer(**test_customer)

        # Delete user
        delete_customer(test_customer['customer_id'])

    def test_search_customer(self):
        """ Test searching for customers """

        add_customer(**test_customer)
        test = search_customer(test_customer['customer_id'])
        self.assertEqual(test.customer_name, test_customer['customer_name'])

        # Make sure test fails
        with self.assertRaises(DoesNotExist):
            test = search_customer(111)

        # Delete user
        delete_customer(test_customer['customer_id'])

    def test_delete_customer(self):
        """ Test deleting customers """

        add_customer(**test_customer)
        delete_customer(test_customer['customer_id'])

        # Make sure test fails
        with self.assertRaises(DoesNotExist):
            delete_customer('333')

    def test_update_customer_credit(self):
        """ Test changing credit limit """

        add_customer(**test_customer)
        update_customer_credit(test_customer['customer_id'], 2500.00)
        test = Customer.get(Customer.customer_id == test_customer['customer_id'])
        self.assertEqual(test.customer_credit_limit, 2500.00)

        # Make sure test fails
        with self.assertRaises(DoesNotExist):
            update_customer_credit(321, 2500.00)

    def test_list_customers(self):
        """ Test listing all active customers """

        add_customer(**test_customer)

        inactive_customer = {'customer_id': 321,
                             'customer_name': 'Dwayne',
                             'customer_last_name': 'Johnson',
                             'customer_address': '321 Not-Fake Street',
                             'customer_phone_number': '321-654-7890',
                             'customer_email': 'pebble@gmail.com',
                             'customer_status': 'inactive',
                             'customer_credit_limit': 10000000.00}
        add_customer(**inactive_customer)

        active_customers = list_active_customers()
        self.assertEqual(active_customers, 1)

    def tearDown(self):
        """ Clean up database """

        data.drop_tables([Customer])
        data.create_tables([Customer])
