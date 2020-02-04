# pylint: disable=wildcard-import, unused-wildcard-import
# pylint: disable=too-few-public-methods
"""Class to test the basic operations module adn customer model class."""
import sys
import os
from unittest import TestCase
from peewee import *
sys.path.append('basic_operations')
from customer_model import *
from basic_operations import *


class MyTestCase(TestCase):
    """Class to test the basic operations module adn customer model class."""
    maxDiff = None

    def setUp(self):
        """Method used to create database, tables and test data"""
        #  database.connect()
        #database.create_tables([Customer, CustomerContact])
        main()
        add_customer('101', 'Calvin', 'Fannin', '5678 Park Wood Drive Mount Pleasant AL 58741', '236-789-7865',
                     'plants@NO.com', 0, 85000)
        add_customer('201', 'Malvin', 'Sannin', '5678 Park Wood Drive Mount Pleasant AL 58741', '236-789-7865',
                     'plants@NO.com', 0, 85000)
        add_customer('301', 'Malvin', 'Sannin', '5678 Park Wood Drive Mount Pleasant AL 58741', '236-789-7865',
                     'plants@NO.com', 1, 85000)
        add_customer('401', 'Malvin', 'Sannin', '5678 Park Wood Drive Mount Pleasant AL 58741', '236-789-7865',
                     'plants@NO.com', 1, 85000)

    def test_add_customer(self):
        """Test add customer method"""
        # qry = (Customer.select().join(CustomerContact).where(Customer.customerid == '10235').dicts()[0])
        self.assertEqual(Customer.name, 'Calvin')
        self.assertEqual(Customer.lastname, 'Fannin')
        self.assertEqual(Customer.customerid, '101')
        self.assertEqual(CustomerContact.phonenumber, '236-789-7865')

    def test_search_customer(self):
        """Test searching for customer by id"""
        expected = {'name': 'Calvin', 'lastname': 'Fannin', 'emailaddress': 'plants@NO.com', 'phonenumber': '236-789-7865'}
        foundcustomer = search_customer('101')
        self.assertEqual(foundcustomer, expected)

    def test_delete_customer(self):
        """Test deleting customer from database"""
        expected = {'name': 'Calvin', 'lastname': 'Fannin', 'emailaddress': 'plants@NO.com', 'phonenumber': '236-789-7865'}
        delete_customer(101)
        foundcustomer = search_customer('101')
        self.assertNotEqual(foundcustomer, expected)
        self.assertEqual(foundcustomer, {})

    def test_delete_customer_fail(self):
        """Test deleting customer not in the database"""
        with self.assertRaises(IndexError):
            delete_customer(1001)

    def test_customer_table_exists(self):
        """Test if table was created in database"""
        self.assertTrue(Customer.table_exists())

    def test_customer_contact_table_exists(self):
        """Test if table was created in database"""
        self.assertTrue(CustomerContact.table_exists())

    def test_customer_update(self):
        """Test updating create limit of customer"""
        update_customer_credit('101', 12)
        qry = (Customer.select(Customer.creditlimit).where(Customer.customerid == '101').dicts()[0])
        self.assertEqual(qry, {'creditlimit': 12})

    def test_customer_update_fail(self):
        """Test updating customer that doesnt exist"""
        with self.assertRaises(ValueError):
            update_customer_credit('777', 12)

    def test_active_customer(self):
        """Test method to count active users"""
        count = list_active_customers()
        self.assertEqual(count, 2)
        with self.assertRaises(Exception):
            database.drop_tables([Customer, CustomerContact])
            count = list_active_customers()

    def tearDown(self):
        """Delete database after test cases have ran"""
        try:
            database.drop_tables([Customer, CustomerContact])
            database.close()
        finally:
            database.close()


if __name__ == '__main__':
    main()
