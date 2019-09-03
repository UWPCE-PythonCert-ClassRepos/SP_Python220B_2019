#! /usr/bin/env python3
""" The Inventory Management Database Integration Test Suite """

import io
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest import TestCase
from unittest.mock import patch
from database_basic import basic_operations

class TestIntegrationScenario(TestCase):
    """ Integration Test Class """
    @classmethod
    def test_end_to_end(cls):
        """ Lifecyle End To End Test """
        basic_operations.create_database()
        assert os.path.exists(basic_operations.DATABASE_NAME)
        basic_operations.add_customer(0,
                                     'jaimes',
                                     'hernandez',
                                     '101 Elliot Ave. SE',
                                     '205-222-1111',
                                     'jh@gmail.com',
                                     True,
                                     2000)
        assert basic_operations.search_customer(1)

        assert basic_operations.update_customer_credit(1, 2000)
        results = basic_operations.search_customer_status(1)
        for result in results:
            assert int(result['customer_id']) == 1
            assert result['status']
            assert int(result['credit_limit']) == 2000

        assert basic_operations.update_customer_credit(1, 3000)
        results = basic_operations.search_customer_status(1)
        for result in results:
            assert int(result['customer_id']) == 1
            assert result['status']
            assert int(result['credit_limit']) == 3000

        assert int(basic_operations.get_active_customer_count()) > 0
        assert basic_operations.delete_customer(1)
        assert int(basic_operations.get_active_customer_count()) == 0

        basic_operations.delete_database()
        assert not os.path.exists(basic_operations.DATABASE_NAME)