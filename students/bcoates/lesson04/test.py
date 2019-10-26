""" Unit testing for basic_operations """

from unittest import TestCase
from peewee import IntegrityError, DoesNotExist
from customer_model import Customer, DATABASE
import logging
import basic_operations as bo

TEST_USER1 = {'customer_id': 1,
              'name': 'Sterling',
              'lastname': 'Archer',
              'home_address': '123 Elm Street',
              'phone_number': '123-456-7890',
              'email_address': 'sterling.archer@gmail.com',
              'status': 'active',
              'credit_limit': 1000.00}

TEST_USER2 = {'customer_id': 2,
              'name': 'Lana',
              'lastname': 'Kane',
              'home_address': '123 Aspen Street',
              'phone_number': '123-456-7891',
              'email_address': 'lana.kane@gmail.com',
              'status': 'inactive',
              'credit_limit': 1500.00}

class OperationalTests(TestCase):
    """ Define a class for testing operations """

    def setUp(self):
        """ Ensure we start with a clean table """

        # Configure logging for test activity
        bo.configure_logger()

        logging.info("Dropping Customer table")
        DATABASE.drop_tables([Customer])
        logging.info("Creating Customer table")
        DATABASE.create_tables([Customer])

    def test_add_customer(self):
        """ Test adding customers """

        # Add a customer and ensure it is in the DB
        bo.add_customer(**TEST_USER1)
        test_customer = Customer.get(Customer.customer_id == TEST_USER1['customer_id'])
        self.assertEqual(test_customer.name, TEST_USER1['name'])

        # Ensure adding a non-unique customer_id fails
        with self.assertRaises(IntegrityError):
            bo.add_customer(**TEST_USER1)

        # Delete the test user
        bo.delete_customer(TEST_USER1['customer_id'])

    def test_search_customer(self):
        """ Test searching for a customer """

        # Add a customer and ensure it is in the DB
        bo.add_customer(**TEST_USER1)

        # Search for a valid user created in the first test
        test_customer = bo.search_customer(TEST_USER1['customer_id'])
        self.assertEqual(test_customer.name, TEST_USER1['name'])

        # Search for an invalid user
        with self.assertRaises(DoesNotExist):
            test_customer = bo.search_customer(50)

        # Delete the test user
        bo.delete_customer(TEST_USER1['customer_id'])

    def test_delete_customer(self):
        """ Test deleting customers """

        # Add a user to ensure we have something to delete
        bo.add_customer(**TEST_USER2)

        # Delete the test user
        bo.delete_customer(TEST_USER2['customer_id'])

        # Search for an invalid user
        with self.assertRaises(DoesNotExist):
            Customer.get(Customer.customer_id == TEST_USER2['customer_id'])

    def test_update_customer_credit(self):
        """ Test updating a customer's credit limit """

        # Add a user to ensure we have something to delete
        bo.add_customer(**TEST_USER1)

        # Update the limit for the first test user
        bo.update_customer_credit(TEST_USER1['customer_id'], 2500.00)
        test_customer = Customer.get(Customer.customer_id == TEST_USER1['customer_id'])
        self.assertEqual(test_customer.credit_limit, 2500.00)

        # Update the limit for a customer that doesn't exist
        with self.assertRaises(DoesNotExist):
            bo.update_customer_credit(50, 3000.00)

        # Delete the test user
        bo.delete_customer(TEST_USER1['customer_id'])

    def test_list_customers(self):
        """ Test listing all customers in the database """

        # Add an active customer
        bo.add_customer(**TEST_USER1)

        # Add an inactive customer
        bo.add_customer(**TEST_USER2)

        # Print the active customers
        active_customers = bo.list_active_customers()
        self.assertEqual(active_customers, 1)

    def tearDown(self):
        """ Ensure we start with a clean table """

        DATABASE.drop_tables([Customer])
        DATABASE.create_tables([Customer])
