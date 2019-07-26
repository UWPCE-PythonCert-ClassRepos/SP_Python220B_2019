"""Unit tests for basic_operations.py"""

import decimal
import unittest
# pylint: disable=wildcard-import, unused-wildcard-import
from basic_operations import *

DATABASE.init('unittest.db')


class CustomerTests(unittest.TestCase):
    """Unit test for the Customer class."""
    def setUp(self):
        DATABASE.drop_tables([Customer])
        DATABASE.create_tables([Customer])

    def test_add_customer(self):
        """Test that we can add a single customer."""
        added = add_customer(
            customer_id=111,
            name="Billy",
            lastname="Bones",
            home_address="123 4th Ave, Seattle WA",
            phone_number=1234567890,
            email_address="spam@gmail.com",
            status=True,
            credit_limit=1234.56
        )
        retrieved = Customer.get(Customer.customer_id == 111)
        self.assertEqual(added, retrieved)

    def test_add_all_customers(self):
        """Test that we can add a collection of customers."""
        add_all_customers(
            [
                {'customer_id': 111,
                 'name': 'Phoebe'},
                {'customer_id': 222,
                 'name': 'Jill'},
                {'customer_id': 333,
                 'name': 'Jose'},
                {'customer_id': 444,
                 'name': 'Nathan'},
                {'customer_id': 555,
                 'name': 'June'}
            ]
        )
        self.assertEqual(search_customer(111).first_name, 'Phoebe')
        self.assertEqual(search_customer(222).first_name, 'Jill')
        self.assertEqual(search_customer(333).first_name, 'Jose')
        self.assertEqual(search_customer(444).first_name, 'Nathan')
        self.assertEqual(search_customer(555).first_name, 'June')

    def test_add_duplicate_key(self):
        """Test that adding a duplicate key does nothing."""
        first = add_customer(
            customer_id=111,
            name="Billy",
            lastname="Bones",
            home_address="123 4th Ave, Seattle WA",
            phone_number=1234567890,
            email_address="spam@gmail.com",
            status=True,
            credit_limit=1234.56
        )
        second = add_customer(
            customer_id=111,
            name="Roger"
        )
        self.assertIsNone(second)
        retrieved = Customer.get(Customer.customer_id == 111)
        self.assertEqual(retrieved, first)
        self.assertEqual(len(Customer), 1)

    def test_search_customer(self):
        """Test that we can retrieve a customer by customer_id."""
        add_customer(customer_id=111, name="Aaron")
        retrieved = search_customer(111)
        self.assertEqual(retrieved.first_name, "Aaron")

    def test_search_all_customers(self):
        """Test that we can retrieve multiple customers by a list of IDs."""
        add_all_customers(
            [
                {'customer_id': 111,
                 'name': 'Phoebe'},
                {'customer_id': 222,
                 'name': 'Jill'},
                {'customer_id': 333,
                 'name': 'Jose'},
                {'customer_id': 444,
                 'name': 'Nathan'},
                {'customer_id': 555,
                 'name': 'June'}
            ]
        )
        res = search_all_customers([111, 333, 555, 777])
        self.assertEqual(next(res).first_name, 'Phoebe')
        self.assertEqual(next(res).first_name, 'Jose')
        self.assertEqual(next(res).first_name, 'June')
        self.assertIsNone(next(res))

    def test_search_customer_not_found(self):
        """Test that a nonexistent ID returns nothing."""
        add_customer(customer_id=111, name="Aaron")
        retrieved = search_customer(222)
        self.assertIsNone(retrieved)

    def test_delete_customer(self):
        """Test that we can delete a single customer."""
        add_customer(customer_id=111, name="Aaron")
        delete_customer(111)
        retrieved = search_customer(111)
        self.assertIsNone(retrieved)

    def test_update_credit(self):
        """Test that we can update the credit limit for a customer."""
        add_customer(customer_id=111, name="Aaron", credit_limit=123.45)
        update_customer_credit(111, 246.90)
        retrieved = search_customer(111)
        self.assertAlmostEqual(retrieved.credit_limit, decimal.Decimal(246.90))

    def test_update_credit_not_found(self):
        """Test that updating credit limit for a nonexistent customer raises
        an error."""
        self.assertRaises(ValueError, lambda: update_customer_credit(111, 7.1))

    def test_list_active_customers(self):
        """Test that we can count the active customers in our database."""
        add_customer(customer_id=111, name="Amy", status=True)
        add_customer(customer_id=222, name="Ben", status=False)
        add_customer(customer_id=333, name="Carrie", status=True)
        add_customer(customer_id=444, name="David")  # status unset
        add_customer(customer_id=555, name="Erin", status=True)
        self.assertEqual(list_active_customers(), 3)
