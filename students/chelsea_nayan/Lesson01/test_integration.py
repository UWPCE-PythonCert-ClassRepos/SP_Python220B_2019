# test_integration.py
# Runs Inventory Management tests as a whole
'''Run Inventory Management Tests as a whole'''

import sys
sys.path.append('inventory_management')

from unittest import TestCase
from unittest.mock import patch, MagicMock
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.inventory_class import Inventory
import inventory_management.market_prices as market_prices
import inventory_management.main as main

class TestInventoryManagment(TestCase):
    def test_integration(self):
        # Set up clear inventory
        main.FULL_INVENTORY = {}
        print(main.FULL_INVENTORY)
        # Add some inventory items
        furn_details = ['code 1', 'item 1', 10.0, 'y', 'material', 'size']
        ea_details = ['code 2', 'item 2', 20.00, 'N', 'Y', 'brand', 2.4]
        inv_details = ['code 3', 'item 3', 30.00, 'n', 'n']

        # This is the expected full inventory as a dictionary
        expected = {
        'code 1': {'product_code': 'code 1',
                   'description': 'item 1',
                   'market_price': 24,
                   'rental_price': 10.00,
                   'material': 'material',
                   'size': 'size'},
        'code 2': {'product_code': 'code 2',
                   'description': 'item 2',
                   'market_price': 24,
                   'rental_price': 20.00,
                   'brand': 'brand',
                   'voltage': 2.4},
        'code 3': {'product_code': 'code 3',
                   'description': 'item 3',
                   'market_price': 24,
                   'rental_price': 30.00},
        }

        # Add each individual item
        with patch('builtins.input', side_effect=furn_details):
            main.add_new_item()
        with patch('builtins.input', side_effect=ea_details):
            main.add_new_item()
        with patch('builtins.input', side_effect=inv_details):
            main.add_new_item()

        # Test if all items were added to the expected full inventory
        self.assertEqual(main.FULL_INVENTORY, expected)


        # This is the expected item info output
        expected_1 = ('product_code: code 1\n',
                      'description: item 1\n',
                      'market_price: 10.0\n',
                      'rental_price: 10.00\n',
                      'material: material\n',
                      'size: size\n')

        expected_2 = ('product_code: code 2\n',
                      'description: item 2\n',
                      'market_price: 20.0\n',
                      'rental_price: 20.00\n',
                      'brand: brand\n',
                      'voltage: 2.4\n')

        expected_3 = ('product_code: code 3\n',
                      'description: item 3\n',
                      'market_price: 30.0\n',
                      'rental_price: 30.00\n')

        # Ensure the expected item info input is correct
        with patch('builtins.input', side_effect=['code 1']):
            self.assertEqual(main.item_info(), print(expected_1))
        with patch('builtins.input', side_effect=['code 1']):
            self.assertEqual(main.item_info(), print(expected_1))
        with patch('builtins.input', side_effect=['code 1']):
            self.assertEqual(main.item_info(), print(expected_1))
