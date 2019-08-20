#!/usr/bin/env python3

# Russell Felts
# Assignment 4 - Unit Tests

""" Unit test for the basic_operations """

from unittest import TestCase
import logging
from peewee import DoesNotExist
from customer_model import DATABASE, Customer
from basic_operations import add_customer, search_customer, delete_customer, \
    update_customer_credit, list_active_customers, list_active_customer_names, add_customers


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def set_up_db():
    """
    Set up routine needed for all tests to make sure the db is in a
    known/empty state
    """
    DATABASE.drop_tables([Customer])
    DATABASE.close()
    DATABASE.create_tables([Customer])
    DATABASE.close()


class BasicOperationsUnitTest(TestCase):
    """
    Unittests for verifying the basic_operations functionality
    """

    test_customers = [[1, "Bruce", "Wayne", "1007 Mountain Drive, Gotham",
                       "228-626-7699", "b_wayne@gotham.net", True, 200000.00],
                      [2, "Clark", "Kent", None, "228-626-7899", "ckent@dailyplanet.com",
                       True, 200.00],
                      [3, "Diana", "Prince", None, "587-8423", "ww@justiceleague.net",
                       False, 100.00]]

    def test_add_customer(self):
        """ Test adding a valid customer record to the DB """
        set_up_db()
        add_customer(*self.test_customers[0])
        test_customer = Customer.get_by_id(1)
        self.assertEqual("Bruce", test_customer.name)
        self.assertEqual("Wayne", test_customer.last_name)
        self.assertEqual("1007 Mountain Drive, Gotham", test_customer.home_address)
        self.assertEqual("228-626-7699", test_customer.phone_number)
        self.assertEqual("b_wayne@gotham.net", test_customer.email)
        self.assertEqual(True, test_customer.status)
        self.assertEqual(200000.00, test_customer.credit_limit)

    def test_add_customers(self):
        """ Test adding a valid customer records to the DB """
        set_up_db()
        add_customers(self.test_customers)
        test_customer = Customer.get_by_id(1)
        self.assertEqual(self.test_customers[0][1], test_customer.name)
        test_customer = Customer.get_by_id(2)
        self.assertEqual(self.test_customers[1][1], test_customer.name)
        test_customer = Customer.get_by_id(3)
        self.assertEqual(self.test_customers[2][1], test_customer.name)

    def test_search_customer(self):
        """
        Test that search_customer returns a dict containing name, last name,
        email address and phone number
        """
        expected_result = {"name": "Bruce", "last_name": "Wayne", "email": "b_wayne@gotham.net",
                           "phone_number": "228-626-7699"}
        set_up_db()
        add_customer(*self.test_customers[0])
        self.assertDictEqual(expected_result, search_customer(1))

    def test_search_no_customer(self):
        """ Test the search_customer returns an empty dict when the customer is not found """
        set_up_db()
        self.assertEqual({}, search_customer(1))

    def test_delete_customer(self):
        """ Tests that a customer can be deleted """
        set_up_db()
        add_customer(*self.test_customers[0])
        delete_customer(1)
        try:
            Customer.get_by_id(1)
        except DoesNotExist:
            LOGGER.info("Customer was deleted.")

    def test_update_customer(self):
        """ Tests that customer can be updated """
        set_up_db()
        add_customer(*self.test_customers[0])
        update_customer_credit(1, 500000.00)
        self.assertEqual(500000.00, Customer.get_by_id(1).credit_limit)

    def test_update_no_customer(self):
        """ Test that a ValueError is raised when trying to update a customer that doesn't exist """
        set_up_db()
        with self.assertRaises(ValueError):
            update_customer_credit(2, 5.50)

    def test_list_active_customers(self):
        """ Test that the correct number of active customers is returned """
        set_up_db()
        add_customer(*self.test_customers[0])
        add_customer(*self.test_customers[1])
        add_customer(*self.test_customers[2])
        self.assertEqual(2, list_active_customers())

    def test_list_active_customer_names(self):
        """ Test that the correct names of active customers is returned """
        set_up_db()
        add_customer(*self.test_customers[0])
        add_customer(*self.test_customers[1])
        add_customer(*self.test_customers[2])
        self.assertEqual(['Bruce Wayne', 'Clark Kent'], list_active_customer_names())
