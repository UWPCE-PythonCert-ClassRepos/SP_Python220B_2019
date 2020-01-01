"""Module for test integration for inventory management"""

import unittest
from unittest import TestCase
from unittest.mock import patch
import inventory_management.main as Main


class ModuleTest(TestCase):
    """Test Module"""

    def test_add_items(self):
        """Test add items"""
        inventory_item = [901, "Keyboard", 5, "n", "n"]
        inventory_1 = {901: {"product_code": 901, "description": "Keyboard",
                             "market_price": 24, "rental_price": 5}}
        with patch("builtins.input", side_effect=inventory_item):
            Main.add_new_item()
        self.assertEqual(Main.FULL_INVENTORY, inventory_1)
        
        
        furniture_item = [902, "Bed Frame", 95, "y", "Steel", "L"]
        inventory_2 = {901: {"product_code": 901, "description": "Keyboard",
                             "market_price": 24, "rental_price": 5},
                       902: {"product_code": 902, "description": "Bed Frame",
                             "market_price": 24, "rental_price": 95,
                             "material": "Steel", "size": "L"}}
        with patch("builtins.input", side_effect=furniture_item):
            Main.add_new_item()
        self.assertEqual(Main.FULL_INVENTORY, inventory_2)

        electric_item = [903, "Dryer", 350, "n", "y", "Samsung", 800]
        inventory_3 = {901: {"product_code": 901, "description": "Keyboard",
                             "market_price": 24, "rental_price": 5},
                       902: {"product_code": 902, "description": "Bed Frame",
                             "market_price": 24, "rental_price": 95,
                             "material": "Steel", "size": "L"},
                       903: {"product_code": 903, "description": "Dryer",
                             "market_price": 24, "rental_price": 350,
                             "brand": "Samsung", "voltage": 800}}
        with patch("builtins.input", side_effect=electric_item):
            Main.add_new_item()
        self.assertEqual(Main.FULL_INVENTORY, inventory_3)


if __name__ == "__main__":
    unittest.main()
