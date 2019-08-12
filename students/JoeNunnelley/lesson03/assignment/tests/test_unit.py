#! /usr/bin/env python3
""" The Inventory Management Database Unit Test Suite """

import io
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest import TestCase
from unittest.mock import patch
import database_basic

# Tests for market_prices
class TestBasicOperations(TestCase):
    """ Class for testing the basic database operations """
    def setUp(self):
        """ Create the database """
        pass


    @classmethod
    def test_add_customer(cls):
        """ Ensure that you can add a customer to the database """
        assert 0


    @classmethod
    def test_search_customer(cls):
        """ Ensure that you can search a customer to the database """
        assert 0


    @classmethod
    def test_delete_customer(cls):
        """ Ensure that you can delete a customer from the database """
        assert 0


    @classmethod
    def test_update_customer_credit(cls):
        """ Ensure that you can update an active customer's credit in the database """
        assert 0


    @classmethod
    def test_list_active_customer(cls):
        """ Ensure that you can list all active customers from the database """
        assert 0


