'''Test Integration Module'''
# Advanced Programming in Python -- Lesson 3 Assignment 1
# Jason Virtue
# Start Date 2/10/2020

#Supress pylint warnings here
# pylint: disable=wildcard-import,unused-wildcard-import

import sys
sys.path.append('C:\\temp')
from unittest import TestCase
import logging
from peewee import *
from basic_operations import *

logging.basicConfig(level=logging.ERROR)
LOGGER = logging.getLogger(__name__)

CUSTOMERS = {"cust_01": {"customer_id": 1,
                         "first_name": "Fred",
                         "last_name": "Flintstone",
                         "address": "123 Bedrock Place",
                         "phone": "123.456.7890",
                         "email_address": "fstone@gmail.com",
                         "status": True,
                         "credit_limit": 1000.00},
             "cust_02": {"customer_id": 2,
                         "first_name": "Wilma",
                         "last_name": "Flintstone",
                         "address": "123 Bedrock Place",
                         "phone": "123.456.7890",
                         "email_address": "wstone@gmail.com",
                         "status": True,
                         "credit_limit": 8000.00},
             "cust_03": {"customer_id": 3,
                         "first_name": "Barney",
                         "last_name": "Rubble",
                         "address": "456 Bedrock Lane",
                         "phone": "111.222.3333",
                         "email_address": "troublee@gmail.com",
                         "status": False,
                         "credit_limit": 5000.00}}

class CustomerDBIntegrationTests(TestCase):
    '''Integration tests performed:
    1. Create table
    2. Delete table
    3. Add all customers
    4. Search active customers
    5. Delete customer that doesn't exist
    6. Update credit limit
    7. Count of active customers
    8. Search for customer
    '''

    def test_it_all(self):
        """ Create a customer model.
        """
        LOGGER.info("Integration tests -- All test cases")

        create_tables()
        delete_customer_table()

        add_customers(CUSTOMERS)

        customer_id_deleted = -1
        customer_id_credit_updated = -1

        with DATABASE.transaction():
            query = Customer.select().where(Customer.status == True)
            self.assertTrue(len(query) == 2)
            customer_id_deleted = query[0].customer_id
            delete_customer(customer_id_deleted)
            customer_id_credit_updated = query[1].customer_id
            update_customer_credit(customer_id_credit_updated, 1300.01)

        self.assertEqual(list_active_customers(), 1)

        customer_lookup = {"Fred": "cust_01",
                           "Wilma": "cust_02",
                           "Barney": "cust_03"}

        for customer_id in range(1, 4):
            if customer_id is customer_id_deleted:
                continue

            acustomer = search_customer(customer_id)
            original_customer_key = customer_lookup[acustomer["name"]]
            original_customer = CUSTOMERS[original_customer_key]

            self.assertEqual(acustomer["name"], original_customer["first_name"])
            self.assertEqual(acustomer["last_name"], original_customer["last_name"])
            self.assertEqual(acustomer["email_address"], original_customer["email_address"])
            self.assertEqual(acustomer["phone_number"], original_customer["phone"])

            if customer_id is customer_id_credit_updated:
                with DATABASE.transaction():
                    query = Customer.select().where(Customer.customer_id == customer_id)
                    self.assertEqual(float(query[0].credit_limit), 1300.01)

        with self.assertRaises(ValueError):
            update_customer_credit(customer_id_deleted, 12345.00)

        with self.assertRaises(ValueError):
            delete_customer(customer_id_deleted)

        acustomer = search_customer(customer_id_deleted)
        self.assertDictEqual(acustomer, {})
