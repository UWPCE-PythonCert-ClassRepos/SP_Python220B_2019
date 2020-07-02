# Stella Kim
# Assignment 3: Storing Customer Data

"""Integration tests for storing customer data"""

from unittest import TestCase
from peewee import SqliteDatabase
from customer_model import Customer
import basic_operations as main


def reset_database():
    """Clears table data in database"""
    main.CUSTOMER_DB.drop_tables([Customer])
    main.CUSTOMER_DB.create_tables([Customer])


class ModuleTests(TestCase):
    """Class for customer storage integration testing"""

    def test_integration(self):
        """Test functionality of entire application."""
        self.assertIsInstance(main.CUSTOMER_DB, SqliteDatabase)
        reset_database()
        test_db = [(1, 'John', 'Smith', '123 Main Street', '2065551234',
                    'smith.john@example.com', 'Active', 10000),
                   (2, 'Jane', 'Doe', '1000 Market Street', '2065555678',
                    'doe.jane@example.com', 'Active', 5000),
                   (3, 'Alice', 'Wonderland', '200 Cherry Street',
                    '2065551357', 'wonderland.alice@example.com',
                    'Active', 1000),
                   (3, 'Mark', 'Allen', '555 Columbia Avenue', '2065552468',
                    'allen.mark@example.com', 'Active', 8500)]

        main.add_customer(*test_db[0])
        main.add_customer(*test_db[1])
        main.add_customer(*test_db[2])

        customer_1 = Customer.get(Customer.customer_id == 1)
        customer_2 = Customer.get(Customer.customer_id == 2)
        customer_3 = Customer.get(Customer.customer_id == 3)

        self.assertEqual(test_db[0][1], customer_1.first_name)
        self.assertEqual(test_db[1][2], customer_2.last_name)
        self.assertEqual(test_db[2][3], customer_3.home_address)

        with self.assertRaises(ValueError):
            main.add_customer(*test_db[3])

        search = main.search_customer(1)
        expected = {'First Name': 'John',
                    'Last Name': 'Smith',
                    'Email Address': 'smith.john@example.com',
                    'Phone Number': '2065551234'}
        self.assertEqual(search, expected)
        self.assertEqual(main.search_customer(4), {})

        main.delete_customer(2)
        search = main.delete_customer(2)
        self.assertEqual(search, None)

        main.update_customer_credit(1, 12000)
        customer = Customer.get(Customer.customer_id == 1)
        self.assertEqual(12000, customer.credit_limit)
        update = main.update_customer_credit(4, 2000)
        self.assertEqual(update, None)
