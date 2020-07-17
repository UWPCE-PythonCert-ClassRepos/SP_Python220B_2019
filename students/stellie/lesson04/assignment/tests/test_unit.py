# Stella Kim
# Assignment 4: Iterables, Iterators & Generators

"""Unit tests for storing customer data"""

from unittest import TestCase
from peewee import SqliteDatabase
from customer_model import Customer
import basic_operations as main

CUSTOMER_1 = (1, 'John', 'Smith', '123 Main Street', '2065551234',
              'smith.john@example.com', 'Active', 10000)
CUSTOMER_2 = (1, 'Jane', 'Doe', '1000 Market Street', '2065555678',
              'doe.jane@example.com', 'Active', 5000)
CUSTOMER_3 = (3, 'Alice', 'Wonderland', '200 Cherry Street', '2065551357',
              'wonderland.alice@example.com', 'Active', 1000)


class DBTest(TestCase):
    """Base model test"""

    def test_database(self):
        """Test to check that database was successfully created"""
        self.assertIsInstance(main.CUSTOMER_DB, SqliteDatabase)


def reset_database():
    """Clears table data in database"""
    main.CUSTOMER_DB.drop_tables([Customer])
    main.CUSTOMER_DB.create_tables([Customer])


class CustomerTests(TestCase):
    """Customer information tests"""

    def test_add_customer(self):
        """Test to check that customer was added to DB properly"""
        reset_database()  # clear database tables
        main.add_customer(*CUSTOMER_1)
        customer = Customer.get(Customer.customer_id == 1)
        self.assertEqual(CUSTOMER_1[1], customer.first_name)
        with self.assertRaises(ValueError):
            main.add_customer(*CUSTOMER_2)

    def test_search_customer(self):
        """Test to check that customer search outputs properly"""
        search = main.search_customer(1)
        expected = {'First Name': 'John',
                    'Last Name': 'Smith',
                    'Email Address': 'smith.john@example.com',
                    'Phone Number': '2065551234'}
        self.assertEqual(search, expected)
        self.assertEqual(main.search_customer(4), {})

    def test_search_all_customers(self):
        """Test to check that customer list correctly outputs customer info"""
        reset_database()
        main.add_customer(*CUSTOMER_1)
        main.add_customer(*CUSTOMER_3)
        expected = main.search_all_customers()
        self.assertEqual(expected,
                         [{'First Name': 'John',
                           'Last Name': 'Smith',
                           'Email Address': 'smith.john@example.com',
                           'Phone Number': '2065551234'},
                          {'First Name': 'Alice',
                           'Last Name': 'Wonderland',
                           'Email Address': 'wonderland.alice@example.com',
                           'Phone Number': '2065551357'}])

    def test_delete_customer(self):
        """Test to check that deleting a customer behaves properly"""
        main.add_customer(*CUSTOMER_3)
        main.delete_customer(3)
        search = main.delete_customer(3)
        self.assertEqual(search, None)

    def test_update_customer_credit(self):
        """Test to check that updating a customer behaves properly"""
        main.update_customer_credit(1, 12000)
        customer = Customer.get(Customer.customer_id == 1)
        self.assertEqual(12000, customer.credit_limit)
        update = main.update_customer_credit(2, 2000)
        self.assertEqual(update, None)

    def test_list_active_count(self):
        """Test to check that customer list correctly outputs count"""
        reset_database()
        main.add_customer(*CUSTOMER_1)
        main.add_customer(*CUSTOMER_3)
        expected = main.list_active_count()
        self.assertEqual(expected, 2)

    def test_list_active_customers(self):
        """Test to check that customer list correctly outputs customer names"""
        reset_database()
        main.add_customer(*CUSTOMER_1)
        main.add_customer(*CUSTOMER_3)
        expected = main.list_active_customers()
        self.assertEqual(expected, ['Smith, John', 'Wonderland, Alice'])
