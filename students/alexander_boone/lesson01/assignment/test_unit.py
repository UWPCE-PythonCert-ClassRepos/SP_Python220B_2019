#!/usr/bin/env python3
"""
This module includes unit tests for the inventory management system.
"""


from unittest import TestCase
from unittest.mock import MagicMock
from inventory_management import inventory_class as inv
from inventory_management import market_prices as mp
from inventory_management import main
from inventory_management import furniture_class as fc
from inventory_management import electric_appliances_class as ea


class InventoryTests(TestCase):
    """Perform tests on inventory_class module."""

    def setUp(self):
        """Define set up characteristics of inventory tests."""

        self.item_code = 12345
        self.description = "First Product"
        self.market_price = 800
        self.rental_price = 25
        self.test_inv = inv.Inventory(self.item_code,
                                      self.description,
                                      self.market_price,
                                      self.rental_price
                                      )
        self.test_inv_dict = self.test_inv.return_as_dictionary()

    def test_inv_creation(self):
        """Compare setup dict to intended dict created."""
        compare_dict = {'item_code': 12345,
                        'description': "First Product",
                        'market_price': 800,
                        'rental_price': 25
                        }
        self.assertEqual(self.item_code, 12345)
        self.assertEqual(self.description, "First Product")
        self.assertEqual(self.market_price, 800)
        self.assertEqual(self.rental_price, 25)
        self.assertDictEqual(self.test_inv_dict, compare_dict)


class MarketPricesTests(TestCase):
    """Perform tests on market_prices module."""
    def setUp(self):
        """Define set up characteristics of Market Price tests."""
        self.item_code = 12345
        self.market_price = 800

    def test_get_latest_price(self):
        """Test get_latest_price module using MagicMock."""
        actual_price = mp.get_latest_price(12345)
        expected_price = 24
        self.assertEqual(actual_price, expected_price)

    def test_mock_get_latest_price(self):
        """Test get_latest_price module using MagicMock."""
        mock = MagicMock(return_value=800)
        actual_price = mock.return_value
        expected_price = self.market_price
        self.assertEqual(actual_price, expected_price)


class FurnitureTests(TestCase):
    """Perform tests on furniture_class module."""
    def setUp(self):
        """Define set up characteristics of furniture class tests."""
        item_code = 123456
        description = "Couch"
        market_price = 600
        rental_price = 10
        material = "Cloth"
        size = "Loveseat"
        self.test_furniture_item = fc.Furniture(item_code,
                                                description,
                                                market_price,
                                                rental_price,
                                                material,
                                                size)
        self.test_furn_dict = self.test_furniture_item.return_as_dictionary()

    def test_furniture_creation(self):
        """Test creation of furniture item."""
        compare_dict = {'item_code': 123456,
                        'description': "Couch",
                        'market_price': 600,
                        'rental_price': 10,
                        'material': "Cloth",
                        'size': "Loveseat",
                        }
        self.assertEqual(self.test_furniture_item.item_code, 123456)
        self.assertEqual(self.test_furniture_item.description, "Couch")
        self.assertEqual(self.test_furniture_item.market_price, 600)
        self.assertEqual(self.test_furniture_item.rental_price, 10)
        self.assertEqual(self.test_furniture_item.material, "Cloth")
        self.assertEqual(self.test_furniture_item.size, "Loveseat")

        self.assertDictEqual(self.test_furn_dict, compare_dict)

class ElectricAppliancesTest(TestCase):
    """Perform tests on Electric Appliances module."""
    def setUp(self):

