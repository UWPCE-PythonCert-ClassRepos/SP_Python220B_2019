#!/usr/bin/env python3
"""
Unit tests for electric_appliances_class, furniture_class, inventory_class,
main, and market_prices
"""

import io
import sys
from electric_appliances_class import *
from furniture_class import *
from inventory_class import *
from main import *
import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch


class ElectricAppliancesTest(TestCase):

    def test_electric_appliances_init(self):
        """
        Tests that ElectricAppliances can be initiated
        """
        e = ElectricAppliances("test product code", "test description", "test market price",
                               "test rental price", "test brand", "test voltage")

        self.assertEqual(e.product_code, "test product code")
        self.assertEqual(e.description, "test description")
        self.assertEqual(e.market_price, "test market price")
        self.assertEqual(e.rental_price, "test rental price")
        self.assertEqual(e.brand, "test brand")
        self.assertEqual(e.voltage, "test voltage")

    def test_electric_appliances_return(self):
        """
        Tests ElectricAppliances return_as_dictionary
        """
        e = ElectricAppliances("test product code", "test description", "test market price",
                               "test rental price", "test brand", "test voltage")
        expected_dictionary = {"product_code": "test product code", "description": "test description",
                               "market_price": "test market price", "rental_price": "test rental price",
                               "brand": "test brand", "voltage": "test voltage"}
        self.assertEqual(e.return_as_dictionary(), expected_dictionary)


class FurnitureTest(TestCase):

    def test_furniture_init(self):
        """
        Tests that Furniture can be initiated
        """
        e = Furniture("test product code", "test description", "test market price", "test rental price",
                      "test material", "test size")

        self.assertEqual(e.product_code, "test product code")
        self.assertEqual(e.description, "test description")
        self.assertEqual(e.market_price, "test market price")
        self.assertEqual(e.rental_price, "test rental price")
        self.assertEqual(e.material, "test material")
        self.assertEqual(e.size, "test size")

    def test_furniture_return(self):
        """
        Tests Furniture return_as_dictionary
        """
        e = Furniture("test product code", "test description", "test market price", "test rental price",
                      "test material", "test size")
        expected_dictionary = {"product_code": "test product code", "description": "test description",
                               "market_price": "test market price", "rental_price": "test rental price",
                               "material": "test material", "size": "test size"}
        self.assertEqual(e.return_as_dictionary(), expected_dictionary)


class InventoryTest(TestCase):

    def test_inventory_init(self):
        """
        Tests that Inventory can be initiated
        """
        e = Inventory("test product code", "test description", "test market price", "test rental price")

        self.assertEqual(e.product_code, "test product code")
        self.assertEqual(e.description, "test description")
        self.assertEqual(e.market_price, "test market price")
        self.assertEqual(e.rental_price, "test rental price")

    def test_inventory_return(self):
        """
        Tests Inventory return_as_dictionary
        """
        e = Inventory("test product code", "test description", "test market price", "test rental price")
        expected_dictionary = {"product_code": "test product code", "description": "test description",
                               "market_price": "test market price", "rental_price": "test rental price"}
        self.assertEqual(e.return_as_dictionary(), expected_dictionary)


class MarketPricesTest(TestCase):

    def test_get_latest_price(self):
        """
        Tests that get_latest_price works from market_prices
        """
        self.assertEqual(market_prices.get_latest_price("test"), 24)
        market_prices.get_latest_price = MagicMock(return_value=10)
        self.assertEqual(market_prices.get_latest_price("test"), 10)


class MainTest(TestCase):

    def test_main_init(self):
        """
        Tests that Main can be initiated
        """
        e = MainInventoryManagement()
        self.assertEqual(len(e.full_inventory), 0)

    def test_main_menu(self):
        """
        Tests that main menu can call correct functions
        """
        e = MainInventoryManagement()
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(e.main_menu().__name__, "add_new_item")
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(e.main_menu().__name__, "item_info")
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(e.main_menu().__name__, "exit_program")

    def test_get_price(self):
        """
        Tests that get_price works
        """
        e = MainInventoryManagement()
        with patch('market_prices.get_latest_price', return_value=10):
            self.assertEqual(e.get_price("fake code"), 10)

    def test_add_new_item(self):
        """
        Tests add_new_item
        """
        e = MainInventoryManagement()
        furniture_input = ['code1', 'test description', 'test rental price', 'y',
                           'test material', 'test size']
        electric_input = ['code2', 'test description', 'test rental price', 'n', 'y',
                          'test brand', 'test voltage']
        other_input = ['code3', 'test description', 'test rental price', 'n', 'n']
        with patch('builtins.input', side_effect=furniture_input), \
                patch('market_prices.get_latest_price', return_value=10):
            e.add_new_item()
            furniture_check = {'product_code': 'code1',
                               'description': 'test description',
                               'market_price': 10,
                               'rental_price': 'test rental price',
                               'material': 'test material',
                               'size': 'test size'}
            self.assertEqual(e.full_inventory.get("code1"), furniture_check)
        with patch('builtins.input', side_effect=electric_input), \
                patch('market_prices.get_latest_price', return_value=20):
            e.add_new_item()
            electric_check = {'product_code': 'code2',
                              'description': 'test description',
                              'market_price': 20,
                              'rental_price': 'test rental price',
                              'brand': 'test brand',
                              'voltage': 'test voltage'}
        self.assertEqual(e.full_inventory.get("code2"), electric_check)
        with patch('builtins.input', side_effect=other_input), \
                patch('market_prices.get_latest_price', return_value=30):
            e.add_new_item()
            other_check = {'product_code': 'code3',
                           'description': 'test description',
                           'market_price': 30,
                           'rental_price': 'test rental price'}
        self.assertEqual(e.full_inventory.get("code3"), other_check)

    def test_item_info_not_found(self):
        """
        Tests item_info not found
        """
        e = MainInventoryManagement()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', side_effect='code3'):
            e.item_info()
            return_value = captured_output.getvalue()
            self.assertEqual(return_value, "Item not found in inventory\n")

    def test_item_info_found(self):
        """
        Tests item_info found
        """
        e = MainInventoryManagement()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        e.full_inventory = {'1': {'product_code': '1',
                                  'description': 'test description',
                                  'market_price': 10,
                                  'rental_price': 'test rental price',
                                  'material': 'test material',
                                  'size': 'test size'}}
        with patch('builtins.input', side_effect='1'):
            e.item_info()
            return_value = captured_output.getvalue()
            expected_value ='''product_code:1
description:test description
market_price:10
rental_price:test rental price
material:test material
size:test size
'''
            self.assertEqual(return_value, expected_value)

    def test_exit_program(self):
        """
        Tests exit_program
        """
        e = MainInventoryManagement
        with self.assertRaises(SystemExit):
            e.exit_program()


if __name__ == '__main__':
    unittest.main()
