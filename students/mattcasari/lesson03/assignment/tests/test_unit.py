""" Unit tests for Lesson 03 Database Basic Operations"""

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=broad-except

import logging
from unittest import TestCase
from peewee import *
from src.customer_model import Customers
from src import basic_operations

DATABASE = SqliteDatabase('customers.db')

try:
    logging.info("Creating tables in database")
    DATABASE.create_tables([Customers])
except Exception as e_val:
    logging.info("Could not create tables")
    logging.info(e_val)

logging.disable(logging.CRITICAL)

CUSTOMER1 = (
    "FY2020-001",
    "Sally",
    "Ride",
    "123 Orbital Way, Mars, WA",
    "206-999-9987",
    "sally.ride@shuttle.org",
    True,
    500000.00,
)
CUSTOMER2 = (
    "FY2011-003",
    "Jerry",
    "Linenger",
    "1997 Mir Drive, Blaze, MS",
    "987-654-3210",
    "jerry.linenger@badco2canister.rz",
    False,
    125000.00,
)
CUSTOMER3 = (
    "FY1997-123",
    "Buzz",
    "Aldrin",
    "656 Moon Rock Rd, Dusty, WY",
    "111-867-5309",
    "buzzaldrin@apollo11.com",
    True,
    333333.33,
)


class CustomerAdd(TestCase):
    """Tests ability to add customer to database before moving to full test"""

    def test_add_customer(self):
        """Testing ability to add customer to database"""
        # Given

        # When
        basic_operations.add_customer(*CUSTOMER1)
        basic_operations.add_customer(*CUSTOMER2)
        basic_operations.add_customer(*CUSTOMER3)

        # Then
        db_customer1 = Customers.get(Customers.customer_id == "FY2020-001")
        db_customer2 = Customers.get(Customers.customer_id == "FY2011-003")
        db_customer3 = Customers.get(Customers.customer_id == "FY1997-123")

        self.assertEqual(CUSTOMER1[1], db_customer1.name)
        self.assertEqual(CUSTOMER1[2], db_customer1.last_name)
        self.assertEqual(CUSTOMER1[3], db_customer1.home_address)
        self.assertEqual(CUSTOMER1[4], db_customer1.phone_number)
        self.assertEqual(CUSTOMER1[5], db_customer1.email_address)
        self.assertEqual(CUSTOMER1[6], db_customer1.status)
        self.assertEqual(CUSTOMER1[7], db_customer1.credit_limit)

        self.assertEqual(CUSTOMER2[6], db_customer2.status)

        self.assertEqual(CUSTOMER3[3], db_customer3.home_address)

        db_customer1.delete_instance()
        db_customer2.delete_instance()
        db_customer3.delete_instance()

    def test_add_customer_exisiting(self):
        """Testing adding existing customer to database"""
        # Given

        # When
        basic_operations.add_customer(*CUSTOMER1)

        # Then
        try:
            basic_operations.add_customer(*CUSTOMER1)
        except Exception as e_val:
            self.fail(e_val)

        db_customer1 = Customers.get(Customers.customer_id == "FY2020-001")
        db_customer1.delete_instance()


class CustomerTest(TestCase):
    """Test class for Customer Functions"""

    def setUp(self):
        try:
            DATABASE.connect()
        except Exception as e_val:
            logging.debug(e_val)
        basic_operations.add_customer(*CUSTOMER1)

    def tearDown(self):
        try:
            db_customer = Customers.get(Customers.customer_id == "FY2020-001")
            db_customer.delete_instance()
        except Exception as e_val:
            logging.debug(e_val)
        try:
            DATABASE.close()
        except Exception as e_val:
            logging.debug(e_val)

    def test_search_customer_exists(self):
        """ Testing search for existing customer"""

        # Given
        expected_customer = {
            "name": "Sally",
            "last_name": "Ride",
            "phone_number": "206-999-9987",
            "email_address": "sally.ride@shuttle.org",
        }

        # When
        actual_customer = basic_operations.search_customer("FY2020-001")

        # Then
        self.assertEqual(expected_customer, actual_customer)

    def test_search_customer_does_not_exist(self):
        """ Testing search for non-existing customer"""

        # Given
        expected_customer = {}

        # When
        actual_customer = basic_operations.search_customer("FY2020-999")

        # Then
        self.assertEqual(expected_customer, actual_customer)

    def test_delete_customer_exists(self):
        """Test if the delete_customer function works for existing customers"""
        # Given
        expected_customer = {
            "name": CUSTOMER1[1],
            "last_name": CUSTOMER1[2],
            "phone_number": CUSTOMER1[4],
            "email_address": CUSTOMER1[5],
        }

        # When

        actual_customer = basic_operations.search_customer("FY2020-001")
        self.assertEqual(expected_customer, actual_customer)
        basic_operations.delete_customer("FY2020-001")
        actual_customer = basic_operations.search_customer("FY2020-001")
        self.assertEqual({}, actual_customer)

    def test_delete_customer_does_not_exist(self):
        """Test if trying to delete non-existing customer"""
        # Given

        # When

        # Then
        try:
            # Just log warning, no exception and no failure
            basic_operations.delete_customer("Scooby")
        except Exception as e_val:
            self.fail(e_val)

    def test_update_customer_credit(self):
        """Test the ability to change customer credit"""
        # Given
        new_credit = 333.33

        # When
        # basic_operations.add_customer(*CUSTOMER1)
        basic_operations.update_customer_credit("FY2020-001", new_credit)

        # Then
        actual_customer = Customers.get(Customers.customer_id == "FY2020-001")
        self.assertEqual(new_credit, float(actual_customer.credit_limit))

    def test_update_customer_credit_bad_id(self):
        """Test response when credit changed to non-existing id"""
        # Given
        new_credit = 3.95

        # When

        # Then
        try:
            basic_operations.update_customer_credit("FY2024-401", new_credit)
        except Exception as e_val:
            self.fail("Non-existing id credit limit failure")
            logging.warning(e_val)

    def test_list_active_customers(self):
        """Test that the function lists all active customers"""
        # Given
        basic_operations.add_customer(*CUSTOMER2)
        basic_operations.add_customer(*CUSTOMER3)

        # When

        # Then
        self.assertEqual(2, basic_operations.list_active_customers())

        basic_operations.delete_customer(CUSTOMER2[0])
        basic_operations.delete_customer(CUSTOMER3[0])
