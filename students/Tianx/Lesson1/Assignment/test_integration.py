"""Integration testing of the Inventory Management script"""

import sys
sys.path.append('./inventory_management')
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from inventory_class import Inventory
from electric_appliances_class import ElectricAppliances
from furniture_class import Furniture
from market_prices import get_latest_price
import main


class ModuleTests(TestCase):
    """A class for Integration testing"""
    def test_integration(self):
        # Test main
        with patch('builtins.input', side_effect=['123', 'RiceCooker', '5.99', 'n', 'y',
                                                  'GE', '220']):
            main.add_new_item()
        with patch('builtins.input', side_effect=['345', 'Table', '59.99', 'y',
                                                  'Wood', 'L']):
            main.add_new_item()
        with patch('builtins.input', side_effect=['456', 'Test item', '19.99', 'n', 'n'
                                                  ]):
            main.add_new_item()

        expected_app = {'product_code': '123', 'description': 'RiceCooker', 'market_price': 24,
                        'rental_price': '5.99', 'brand': 'GE', 'voltage': '220'}
        expected_furn = {'product_code': '345', 'description': 'Table', 'market_price': 24,
                         'rental_price': '59.99', 'material': 'Wood', 'size': 'L'}
        expected_inv = {'product_code': '456', 'description': 'Test item',
                        'market_price': 24, 'rental_price': '19.99'}

        self.assertEqual(main.FULL_INVENTORY['123'], expected_app)
        self.assertEqual(main.FULL_INVENTORY['345'], expected_furn)
        self.assertEqual(main.FULL_INVENTORY['456'], expected_inv)

        # Test item_info
        with patch('builtins.input', side_effect=['123']):
            self.assertEqual(main.item_info(), True)
        with patch('builtins.input', side_effect=['678']):
            self.assertEqual(main.item_info(), False)
        # Test get_lastest_price
        self.market_price = get_latest_price(123)
        self.assertEqual(self.market_price, 24)
