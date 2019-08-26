#!/usr/bin/env python3

# Russell Felts
# Assignment 4 - Integration Tests

""" Integration test for the basic_operations """

from unittest import TestCase
import logging
from customer_model import DATABASE, Customer
from basic_operations import search_customer, delete_customer, update_customer_credit,\
    list_active_customers, add_customers, list_active_customer_names


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class BasicOperationsIntegrationTest(TestCase):
    """ Integration testcase for the basic operations """

    test_customer = [[1, "Stephen", "Strange", "177A Bleecker Street New York City",
                      "476-6626-7899", "sse@mcu.com", False, 200.00],
                     [2, "Tony", "Stark", "10880 Malibu Point",
                      "4766626769", "tony@starkinc.com", True, 30000000.00],
                     [3, "Reed", "Richards", "42nd Street New York City",
                      "555-555-5555", "mrfantastic@ff.net", True, 200000.00]]

    def test_basic_operations(self):
        """" Integration test for the basic operations """

        DATABASE.drop_tables([Customer])
        DATABASE.close()
        DATABASE.create_tables([Customer])
        DATABASE.close()

        # Add customers to the db
        add_customers(self.test_customer)

        cust_found = search_customer(2)
        self.assertEqual(self.test_customer[1][5], cust_found.get("email"))

        update_customer_credit(1, 500.00)
        self.assertEqual(500.00, Customer.get_by_id(1).credit_limit)

        # Find out how many customers are active
        active_cust = list_active_customers()
        self.assertEqual(2, active_cust)

        # Delete a customer then try to find it
        delete_customer(2)
        self.assertDictEqual({}, search_customer(2))

        # Find out how many customers are active and list their names
        self.assertEqual(1, list_active_customers())
        self.assertEqual(["Reed Richards"], list_active_customer_names())
