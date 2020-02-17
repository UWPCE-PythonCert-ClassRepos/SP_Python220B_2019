# Advanced Programming in Python -- Lesson 3 Assignment 1
# Jason Virtue
# Start Date 2/10/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import

import sys
sys.path.append('C:\\temp')
from unittest import TestCase
import logging
from peewee import *
from basic_operations import *

logging.basicConfig(level=logging.ERROR)
LOGGER = logging.getLogger(__name__)

# Sample customer data
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


class SetupDB(TestCase):
    """ Tests cases to validate database and schema"""
    def setUp(self):
        """ Create Customer table"""
        create_tables()

    def tearDown(self):
        """ Delete Customer table"""
        delete_customer_table()

    def test_create_customer_model(self):
        """ Create a customer model"""
        LOGGER.info("test_create_customer_model")
        customer_model = Customer()
        self.assertIsInstance(customer_model, BaseModel)
        self.assertIsInstance(customer_model, Model)

        # Test schema has right columns
        self.assertTrue(hasattr(customer_model, "customer_id"))
        self.assertTrue(hasattr(customer_model, "name"))
        self.assertTrue(hasattr(customer_model, "last_name"))
        self.assertTrue(hasattr(customer_model, "home_address"))
        self.assertTrue(hasattr(customer_model, "phone_number"))
        self.assertTrue(hasattr(customer_model, "email_address"))
        self.assertTrue(hasattr(customer_model, "status"))
        self.assertTrue(hasattr(customer_model, "credit_limit"))

    def test_create_customer_table(self):
        """ Add a Customer table to database and validate it exists"""
        LOGGER.info("test_create_customer_table")

        create_tables()

        database.close()
        database.connect()
        self.assertTrue(Customer.table_exists())
        database.close()

    def test_add_customer_to_db(self):
        """ Add first customer records to table and verify"""
        LOGGER.info("test_add_customer_to_db")

        cust_01 = CUSTOMERS["cust_01"]

        add_customer(customer_id=cust_01["customer_id"],
                     name=cust_01["first_name"],
                     lastname=cust_01["last_name"],
                     home_address=cust_01["address"],
                     phone_number=cust_01["phone"],
                     email_address=cust_01["email_address"],
                     status=cust_01["status"],
                     credit_limit=cust_01["credit_limit"])

        acustomer = Customer.get(Customer.customer_id == cust_01["customer_id"])

        self.assertEqual(acustomer.customer_id, cust_01["customer_id"])
        self.assertEqual(acustomer.email_address, cust_01["email_address"])
        self.assertEqual(acustomer.name, cust_01["first_name"])
        self.assertEqual(acustomer.last_name, cust_01["last_name"])
        self.assertEqual(acustomer.home_address, cust_01["address"])
        self.assertEqual(acustomer.phone_number, cust_01["phone"])
        self.assertEqual(acustomer.status, cust_01["status"])
        self.assertEqual(acustomer.credit_limit, cust_01["credit_limit"])


class PopulateTables(TestCase):
    """ Test cases with customer data in table and validate modules"""
    def setUp(self):
        """ Create table and add customer data"""
        LOGGER.info('in TestCase:setUp')

        create_tables()
        LOGGER.info('Created the tables')
        add_customers(CUSTOMERS)
        LOGGER.info('Added the customers')

    def tearDown(self):
        """ Delete the Customer table.
        """
        delete_customer_table()

    def test_search_customer(self):
        """ Search for a customer by customer_id"""
        LOGGER.info("test_search_customer")

        cust_02 = CUSTOMERS["cust_02"]
        acustomer = search_customer(cust_02["customer_id"])

        self.assertEqual(acustomer["name"], cust_02["first_name"])
        self.assertEqual(acustomer["last_name"], cust_02["last_name"])
        self.assertEqual(acustomer["phone_number"], cust_02["phone"])
        self.assertEqual(acustomer["email_address"], cust_02["email_address"])

    def test_search_customer_not_found(self):
        """ Test for customer out of range of sample data"""
        LOGGER.info("test_search_customer_not_found")
        acustomer = search_customer(4)

        self.assertDictEqual(acustomer, {})

    def test_delete_customer(self):
        """ Delete a customer row"""
        LOGGER.info("test_delete_customer")
        cust_03 = CUSTOMERS["cust_03"]
        delete_customer(cust_03["customer_id"])

        self.assertDictEqual(search_customer(cust_03["customer_id"]), {})

    def test_delete_customer_not_in_the_db(self):
        """ Delete a customer not in database"""
        LOGGER.info("test_delete_customer_not_in_the_db")

        # first delete the customer
        cust_03 = CUSTOMERS["cust_03"]
        delete_customer(cust_03["customer_id"])

        with database.transaction():
            try:
                Customer.get(Customer.customer_id == cust_03["customer_id"])
            except DoesNotExist:
                assert True
            else:
                LOGGER.error("test_delete_customer_not_in_the_db: customer was not deleted")
                assert False

        with self.assertRaises(ValueError):
            delete_customer(cust_03["customer_id"])

    def test_update_customer_credit(self):
        """ Update credit limit"""
        LOGGER.info("test_update_customer_credit")

        cust_01 = CUSTOMERS["cust_01"]
        self.assertEqual(cust_01["credit_limit"], 1000.00)

        update_customer_credit(cust_01["customer_id"], 13000.01)
        acustomer = Customer.get(Customer.customer_id == cust_01["customer_id"])
        self.assertEqual(float(acustomer.credit_limit), 13000.01)

    def test_update_customer_credit_not_in_the_db(self):
        """ Update the credit of a customer not in database"""

        with database.transaction():
            try:
                Customer.get(Customer.customer_id == 4)
            except DoesNotExist:
                assert True
            else:
                LOGGER.error("test_update_customer_credit_not_in_the_db: customer is in the db")
                assert False

        # Now try updating credit for a customer that isn't there.
        with self.assertRaises(ValueError):
            update_customer_credit(4, 13000.00)

    def test_list_active_customers(self):
        """ Find the number of active customers"""
        LOGGER.info("test_list_active_customers")
        active_customers = [acustomer for acustomer in CUSTOMERS.values()
                            if acustomer["status"] is True]

        self.assertEqual(list_active_customers(), len(active_customers))
