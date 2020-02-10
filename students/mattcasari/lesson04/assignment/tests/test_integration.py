""" Unit tests for Lesson 03 Database Basic Operations"""

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=broad-except

import logging
from unittest import TestCase
from peewee import *
from src.customer_model import Customers
from src import basic_operations

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info("START: test_integration")


class TestCustomerIntegration(TestCase):
    """Testing Program Integration for Basic Operations of Database"""

    # Set up Database
    DATABASE = SqliteDatabase("customers.db")
    DATABASE.connect()
    DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

    try:
        LOGGER.info("Creating tables in database")
        DATABASE.create_tables([Customers])
    except Exception as e_val:
        LOGGER.info("Could not create tables")
        LOGGER.info(e_val)

    def test_basic_operations(self):
        """Test all basic operations in one integration test"""

        # Add customer
        basic_operations.add_customer(
            "TEST001",
            "Matt",
            "Casari",
            "Washington",
            "999-999-9999",
            "matt.casari@email.com",
            True,
            500000.00,
        )

        # Add a second customer
        basic_operations.add_customer(
            "TEST002",
            "Ringo",
            "Bingo",
            "California",
            "999-999-9990",
            "ringo.bingo@themail.com",
            True,
            20000.00,
        )

        # Try to add another customer TEST002
        basic_operations.add_customer(
            "TEST002",
            "Ringo",
            "Bingo",
            "California",
            "999-999-9990",
            "ringo.bingo@themail.com",
            True,
            20000.00,
        )

        # Update customer 1 credit
        basic_operations.update_customer_credit("TEST001", 999999.99)

        # Delete customer 2
        basic_operations.delete_customer("TEST002")

        # Update customer 2 credit (who no longer exists)
        basic_operations.update_customer_credit("TEST002", 55.99)

        # Delete a non-existing customer
        basic_operations.delete_customer("Happy1")

        # Search customer 1
        customer1 = basic_operations.search_customer("TEST001")

        # Search customer 2 (who no longer exists)
        customer2 = basic_operations.search_customer("TEST002")

        # list number customers
        customer_count = basic_operations.list_active_customers()

        # Get the email list
        email_list = basic_operations.list_active_emails()

        # Assert all
        self.assertEqual({}, customer2)
        self.assertEqual("Matt", customer1["name"])
        self.assertEqual("999-999-9999", customer1["phone_number"])
        self.assertEqual(1, customer_count)
        self.assertEqual(["matt.casari@email.com"], email_list)

        # Delete the remaining customer
        basic_operations.delete_customer("TEST001")

        # Mark end of test
        LOGGER.info("END: test_integration")
