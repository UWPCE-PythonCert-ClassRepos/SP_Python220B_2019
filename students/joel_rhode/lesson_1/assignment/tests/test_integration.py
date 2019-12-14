"""Integration tests for the inventory_management system."""

import sys
from unittest import TestCase
from unittest.mock import patch

sys.path.append('./inventory_management')
import main

class InventoryManagementTestCases(TestCase):
    """Class for integrated testing of the Inventory Management system."""
    @patch('builtins.input')
    def test_main_inventory_management(self, mock_input):
        """Tests input and resulting dictionary output for main.py"""
        main.FULL_INVENTORY = {}

        expected_out_dict = {
            'F-1': {
                'rental_price': 75.,
                'market_price': 24,
                'product_code': 'F-1',
                'description': 'Table',
                'size': 'L',
                'material': 'Wood'
            },
            'GI-1': {
                'rental_price': 50.,
                'product_code': 'GI-1',
                'market_price': 24,
                'description': 'Fake Plant'
            },
            'EA-2': {
                'rental_price': 100.,
                'market_price': 24,
                'product_code': 'EA-2',
                'description': 'Dishwasher',
                'voltage': '240',
                'brand': 'Maytag'
            }
        }
        mock_input.side_effect = ['F-1', 'Table', 75., 'y', 'Wood', 'L', 'GI-1',
                                  'Fake Plant', 50., 'n', 'n', 'EA-2', 'Dishwasher',
                                  100., 'n', 'y', 'Maytag', '240', '2', 'GI-1', 'q']

        for __ in range(3):
            main.main_menu('1')
        self.assertDictEqual(main.FULL_INVENTORY, expected_out_dict)




