from unittest import TestCase
from unittest.mock import patch

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.main as main
from inventory_management.market_prices import get_latest_price


class ModultTests(TestCase):

    def test_module(self):
        electric_appliance = [1, "item", 5, "n", "y", "brand", 5.5]
        furniture = [2, "item", 5, "y", "material", "XL"]
        inventory = [3, "item", 5, "n", "n"]
        main.FULL_INVENTORY = {}
        expected = {1: {'product_code': 1, 'description': "item", 'market_price': 24,
                'rental_price': 5, 'brand': "brand", 'voltage': 5.5}}

        with patch('builtins.input', side_effect = electric_appliance):
            main.add_new_item()
            self.assertEqual(expected, main.FULL_INVENTORY)

        expected = {
        1: {'product_code': 1, 'description': "item", 'market_price': 24,
            'rental_price': 5, 'brand': "brand", 'voltage': 5.5}
        ,2: {'product_code': 2, 'description': "item", 'market_price': 24,
            'rental_price': 5, 'material': "material", 'size': "XL"}
        }

        with patch('builtins.input', side_effect = furniture):
            main.add_new_item()
            self.assertEqual(expected, main.FULL_INVENTORY)

        expected = {
        1: {'product_code': 1, 'description': "item", 'market_price': 24,
            'rental_price': 5, 'brand': "brand", 'voltage': 5.5}
        ,2: {'product_code': 2, 'description': "item", 'market_price': 24,
            'rental_price': 5, 'material': "material", 'size': "XL"}
        ,3: {'product_code': 3, 'description': "item", 'market_price': 24,
                'rental_price': 5}
        }

        with patch('builtins.input', side_effect = inventory):
            main.add_new_item()
            self.assertEqual(expected, main.FULL_INVENTORY)