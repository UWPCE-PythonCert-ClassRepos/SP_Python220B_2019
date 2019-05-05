#!/usr/bin/env python3
"""
Integration tests for electric_appliances_class, furniture_class, inventory_class,
main, and market_prices
"""

from main import *
from unittest import TestCase
from unittest.mock import patch
import io


class InventoryIntegrationTest(TestCase):

    def test_integration(self):
        """
        Tests that an item can be added, then the info checked, then the program closed
        """
        e = MainInventoryManagement()
        furniture_input = ['1', 'test description', 'test rental price', 'y',
                           'test material', 'test size']
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', side_effect=furniture_input), \
                patch('market_prices.get_latest_price', return_value=10):
            e.add_new_item()
        with patch('builtins.input', side_effect='1'):
            e.item_info()
            return_value = captured_output.getvalue()
            expected_value = '''New inventory item added
product_code:1
description:test description
market_price:10
rental_price:test rental price
material:test material
size:test size
'''
        self.assertEqual(return_value,expected_value)
        with self.assertRaises(SystemExit):
            e.exit_program()
