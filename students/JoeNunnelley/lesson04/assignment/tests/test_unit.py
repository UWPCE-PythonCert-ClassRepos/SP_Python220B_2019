#! /usr/bin/env python3
""" The Inventory Management Database Unit Test Suite """

import io
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest import TestCase
from unittest.mock import patch
from database_basic import basic_operations

# Tests for market_prices
class TestBasicOperations(TestCase):
    """ Class for testing the basic database operations """
    @classmethod
    def test_database_creation(self):
        """ Create the database """
        assert basic_operations.create_database()
        basic_operations.DATABASE.connect()
        assert not basic_operations.DATABASE.is_closed()


    @classmethod
    def test_add_customer(cls):
        """ Ensure can add a customer to the database """
        assert basic_operations.create_database()
        added_user = basic_operations.add_customer(0,
                                                   'jaimes',
                                                   'hernandez',
                                                   '101 Elliot Ave. SE',
                                                   '205-222-1111',
                                                   'jh@gmail.com',
                                                   True,
                                                   2000)
        assert added_user['customer_id'] > 0
        assert added_user['customer_status_id'] > 0
        basic_operations.delete_customers()


    @classmethod
    def test_add_customer_with_id(cls):
        """ Ensure can add a customer to the database with id """
        assert basic_operations.create_database()
        added_user = basic_operations.add_customer(0,
                                                   'jaimes',
                                                   'hernandez',
                                                   '101 Elliot Ave. SE',
                                                   '205-222-1111',
                                                   'jh@gmail.com',
                                                   True,
                                                   2000)
        added_user = basic_operations.add_customer(1,
                                                   'jaimes',
                                                   'hernandez',
                                                   '101 Elliot Ave. SE',
                                                   '205-222-1111',
                                                   'jh@gmail.com',
                                                   True,
                                                   2000)
        assert added_user['customer_id'] == 1
        assert added_user['customer_status_id'] == 1
        basic_operations.delete_customers()


    @classmethod
    def test_search_customer_valid(cls):
        """ Ensure can search a customer to the database """
        assert basic_operations.create_database()
        basic_operations.add_customer(0,
                                     'jaimes',
                                     'hernandez',
                                     '101 Elliot Ave. SE',
                                     '205-222-1111',
                                     'jh@gmail.com',
                                     True,
                                     2000)
        assert basic_operations.search_customer(1)
        basic_operations.delete_customers()


    @classmethod
    def test_search_customer_invalid(cls):
        """ Ensure proper result when searching for invalid customer """
        assert basic_operations.create_database()
        assert basic_operations.search_customer(2) is None


    @classmethod
    def test_update_customer_credit_valid(cls):
        """ Ensure can update an active customer's credit in the database """
        assert basic_operations.create_database()
        basic_operations.add_customer(0,
                                     'jaimes',
                                     'hernandez',
                                     '101 Elliot Ave. SE',
                                     '205-222-1111',
                                     'jh@gmail.com',
                                     True,
                                     2000)
        assert basic_operations.update_customer_credit(1, 3000)
        results = basic_operations.search_customer_status(1)
        for result in results:
            assert int(result['customer_id']) == 1
            assert result['status']
            assert int(result['credit_limit']) == 3000

        basic_operations.delete_customers()


    @classmethod
    def test_update_customer_credit_invalid(cls):
        """
        Ensure can update an invalid customer's credit in the database  fails
        """
        assert basic_operations.create_database()
        basic_operations.add_customer(0,
                                     'jaimes',
                                     'hernandez',
                                     '101 Elliot Ave. SE',
                                     '205-222-1111',
                                     'jh@gmail.com',
                                     True,
                                     2000)
        assert not basic_operations.update_customer_credit(10, 3000)
        result = basic_operations.search_customer_status(10)
        assert len(result) == 0
        basic_operations.delete_customers()


    @classmethod
    def test_list_active_customer(cls):
        """ Ensure can list all active customers from the database """
        assert basic_operations.create_database()
        basic_operations.add_customer(0,
                                     'jaimes',
                                     'hernandez',
                                     '101 Elliot Ave. SE',
                                     '205-222-1111',
                                     'jh@gmail.com',
                                     True,
                                     2000)
        assert int(basic_operations.get_active_customer_count()) == 1
        basic_operations.delete_customers()


    @classmethod
    def test_delete_customer_valid(cls):
        """ Ensure can delete a customer from the database """
        assert basic_operations.create_database()
        basic_operations.add_customer(0,
                                     'jaimes',
                                     'hernandez',
                                     '101 Elliot Ave. SE',
                                     '205-222-1111',
                                     'jh@gmail.com',
                                     True,
                                     2000)
        before = basic_operations.get_active_customer_count()
        assert before > 0
        assert basic_operations.delete_customer(1)
        after = basic_operations.get_active_customer_count()
        assert before > after
        basic_operations.delete_customers()


    @classmethod
    def test_delete_customer_invalid(cls):
        """ Ensure can delete a customer from the database """
        assert basic_operations.create_database()
        basic_operations.add_customer(0,
                                     'jaimes',
                                     'hernandez',
                                     '101 Elliot Ave. SE',
                                     '205-222-1111',
                                     'jh@gmail.com',
                                     True,
                                     2000)
        before = basic_operations.get_active_customer_count()
        assert before > 0
        basic_operations.delete_customer(10)
        after = basic_operations.get_active_customer_count()
        assert before == after
        basic_operations.delete_customers()


    @classmethod
    def test_delete_customers(cls):
        """ Ensure that the delete_customers function deletes all customers"""
        assert basic_operations.create_database()
        basic_operations.load_customers()
        assert basic_operations.get_active_customer_count() > 0
        basic_operations.delete_customers()
        basic_operations.get_active_customer_count() == 0


    @classmethod
    def test_load_customers(cls):
        """ Ensure that the delete_customers function deletes all customers"""
        assert basic_operations.create_database()
        assert basic_operations.get_active_customer_count() == 0
        basic_operations.load_customers()
        assert basic_operations.get_active_customer_count() > 0
        basic_operations.delete_customers()


    @classmethod
    def test_list_active_customers(cls):
        """ Ensure that active customer count is correct """
        assert basic_operations.create_database()
        basic_operations.load_customers()
        assert len(basic_operations.list_active_customers()) > 0
        basic_operations.delete_customers()


    @classmethod
    def test_list_inactive_customers(cls):
        """ Ensure that active customer count is correct """
        assert basic_operations.create_database()
        basic_operations.load_customers()
        assert len(basic_operations.list_inactive_customers()) > 0
        basic_operations.delete_customers()


    @classmethod
    def test_get_existing_customer(cls):
        """
        Ensure that creating a customer that already exists
        gets the existing customer
        """
        assert basic_operations.create_database()
        basic_operations.load_customers()
        customer = basic_operations.create_or_get_customer(1, '', '', '', '', '')
        created_customer = basic_operations.create_or_get_customer(0,
                                                                   customer.name,
                                                                   customer.last_name,
                                                                   customer.address,
                                                                   customer.phone_number,
                                                                   customer.email)
        assert customer.name == created_customer.name
        assert customer.last_name == created_customer.last_name
        assert customer.address == created_customer.address
        assert customer.phone_number == created_customer.phone_number
        assert customer.email == created_customer.email
        found = basic_operations.search_customer(1)
        assert len(found) == 1
        basic_operations.delete_customers()
