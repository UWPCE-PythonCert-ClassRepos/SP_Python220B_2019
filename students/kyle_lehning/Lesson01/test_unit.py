#!/usr/bin/env python3
"""
Unit tests for electric_appliances_class, furniture_class, inventory_class,
main, and market_prices
"""

import sys
from electric_appliances_class import *
from furniture_class import *
from inventory_class import *
from main import *
from market_prices import *
import unittest
from unittest import TestCase
from unittest.mock import  MagicMock


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


if __name__ == '__main__':
    unittest.main()
