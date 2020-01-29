""" Test the full integration of the Inventory Management System"""
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

from inventory_management.inventory import Inventory
from inventory_management.electric_appliances import ElectricAppliances
from inventory_management.furniture import Furniture

# from inventory_management.market_prices import get_latest_price

import inventory_management.main as main
import inventory_management.market_prices as market_prices
import io


class TestIntegration(TestCase):
    def test_integration(self):
        """ Test the full integration of the program"""

        # Given
        main.FULL_INVENTORY = {}
        item_1 = ("1", "1001", "Kumiko Panel", 5.00, "n", "n")
        item_2 = ("\n", "1", "1002", "Dining Room Table", 93.00, "y", "Walnut", "L")
        item_3 = ("\n", "1", "1003", "Desk lamp", 12.00, "n", "y", "LiteBrite", 110)

        expected_dict = {
            "1001": {
                "product_code": "1001",
                "description": "Kumiko Panel",
                "market_price": 24,
                "rental_price": 5.00,
            },
            "1002": {
                "product_code": "1002",
                "description": "Dining Room Table",
                "market_price": 24,
                "rental_price": 93.00,
                "material": "Walnut",
                "size": "L",
            },
            "1003": {
                "product_code": "1003",
                "description": "Desk lamp",
                "market_price": 24,
                "rental_price": 12.00,
                "brand": "LiteBrite",
                "voltage": 110,
            },
        }

        expected_info = """product_code:1003
description:Desk lamp
market_price:24
rental_price:12.0
brand:LiteBrite
voltage:110
"""

        # When

        with patch("builtins.input", side_effect=item_1):
            main.main_menu()()
        with patch("builtins.input", side_effect=item_2):
            main.main_menu()()
        with patch("builtins.input", side_effect=item_3):
            main.main_menu()()
        with patch("builtins.input", side_effect="2"):
            self.assertEqual(main.item_info, main.main_menu())

        market_prices.get_latest_price = MagicMock(return_value=300)
        self.assertEqual(300, main.get_price("1003"))

        with patch("builtins.input", side_effect=["1003"]):
            with patch("sys.stdout", new=io.StringIO()) as actual_result:
                main.item_info()
                self.assertEqual(expected_info, actual_result.getvalue())

        with patch("builtins.input", side_effect=["1004"]):
            with patch("sys.stdout", new=io.StringIO()) as actual_result:
                main.item_info()
                self.assertEqual(
                    "Item not found in inventory\n", actual_result.getvalue()
                )

        with patch("builtins.input", side_effect=["q"]):
            with self.assertRaises(SystemExit):
                main.main_menu()()
            # self.assertEqual(main.exit_program,main.main_menu())
        # Then
        self.assertEqual(expected_dict, main.FULL_INVENTORY)
