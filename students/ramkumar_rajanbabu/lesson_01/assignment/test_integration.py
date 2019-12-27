"""Module for test integration for inventory management"""


from unittest import TestCase
from unittest.mock import patch
import inventory_management.main as Main


class ModuleTest(TestCase):
    """Test Module"""

    def test_add_items(self):
        """Test add items"""
        product_1 = [901, "Keyboard", "n", "n"]
        inventory_1 = {901: {"product_code": 901, "description": "Keyboard",
                             "market_price": 25, "rental_price": 5}}
        with patch("builtins.input", side_effect=product_1):
            Main.add_new_item()
        self.assertEqual(Main.FULL_INVENTORY, inventory_1)

        product_2 = [902, "Bed Frame", 650, 95, "Steel", "L"]
        inventory_2 = {901: {"product_code": 901, "description": "Keyboard",
                             "market_price": 25, "rental_price": 5},
                       902: {"product_code": 902, "description": "Bed Frame",
                             "market_price": 650, "rental_price": 95,
                             "material": "Steel", "size": "L"}}
        with patch("builtins.input", side_effect=product_2):
            Main.add_new_item()
        self.assertEqual(Main.FULL_INVENTORY, inventory_2)

        product_3 = [903, "Dryer", 5000, 350, "Samsung", 800]
        inventory_3 = {901: {"product_code": 901, "description": "Keyboard",
                             "market_price": 25, "rental_price": 5},
                       902: {"product_code": 902, "description": "Bed Frame",
                             "market_price": 650, "rental_price": 95,
                             "material": "Steel", "size": "L"},
                       903: {"product_code": 903, "description": "Dryer",
                             "market_price": 5000, "rental_price": 350,
                             "brand": "Samsung", "voltage": 800}}
        with patch("builtins.input", side_effect=product_3):
            Main.add_new_item()
        self.assertEqual(Main.FULL_INVENTORY, inventory_3)

        product_dict = {"product_code": 901, "description": "Keyboard",
                        "market_price": 25, "rental_price": 5}
        with patch("builtins.input", side_effect="901"):
            self.assertEqual(Main.item_info(), print(product_dict))
