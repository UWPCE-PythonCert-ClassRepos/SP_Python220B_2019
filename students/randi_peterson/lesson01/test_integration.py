"""
Created by Randi Peterson, 6/22/2019
"""

"""This file conducts integration testing for the Norton code"""
import sys
sys.path.append('inventory_management')
from inventory_class import Inventory
from furniture_class import Furniture
from electric_appliances_class import ElectricAppliances
from market_prices import get_latest_price
from main import FULL_INVENTORY, main_menu, get_price, add_new_item, item_info, exit_program
from unittest import TestCase
from unittest.mock import MagicMock, patch

class ModuleTest(TestCase):
    def test_module(self):
        new_furniture = ('1', 123, 'Bed', 500, 'y', 'spring', 'L')
        current_inventory = {123: {'product_code': 123, 'description': 'Bed',
                                  'market_price': 24, 'rental_price': 500,
                                  'material': 'spring', 'size': 'L'}}
        with patch('builtins.input', side_effect= new_furniture):
            main_menu()()
            self.assertEqual(current_inventory, FULL_INVENTORY)

        electrical_input = ('\n', '1', 154, 'Stove', 150, 'n', 'y', 'Bosch', 120)
        comparison_inventory = {123: {'product_code': 123, 'description': 'Bed',
                                  'market_price': 24, 'rental_price': 500,
                                  'material': 'spring', 'size': 'L'},
                                154: {'product_code': 154, 'description': 'Stove',
                                        'market_price': 24, 'rental_price': 150,
                                        'brand': 'Bosch', 'voltage': 120}}

        with patch('builtins.input', side_effect = electrical_input):
            main_menu()()
        self.assertEqual(FULL_INVENTORY, comparison_inventory)

        with patch('builtins.input', side_effect = ['\n', '2', 154]):
            self.assertEqual(main_menu(), item_info)

        with patch('builtins.input', side_effect = ['\n', 'q']):
            self.assertEqual(main_menu(),exit_program)