import sys
sys.path.append('C:\\Users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\'
                'students\\chris_lombardi\\lesson01\\inventory_management')

from unittest import TestCase
from unittest.mock import MagicMock, patch
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
import inventory_management.market_prices as mp
import inventory_management.main as main

class TestInventoryManagement(TestCase):

    def test_integration(self):
        main.FULL_INVENTORY = {}
        inv_details = ['001', 'Painting', 6.0, 'n', 'n']
        app_details = ['002', 'Microwave', 5.0, 'n', 'y', 'GE', 3.2]
        furn_details = ['003', 'Desk', 15.0, 'y', 'Mahogany', 'L']

        expected_dict = {
        '001': {'product_code': '001', 'description': 'Painting',
                'market_price': 24, 'rental_price': 6.0},
        '002': {'product_code': '002', 'description': 'Microwave', 'market_price': 24,
                'rental_price': 5.0, 'brand': 'GE', 'voltage': 3.2},
        '003': {'product_code': '003', 'description': 'Desk', 'market_price': 24,
                'rental_price': 15.0, 'material': 'Mahogany', 'size': 'L'}
        }

        # Expected output for searching inventory.
        test_string = ('product_code: 002\n'
                       'description: Microwave\n'
                       'market_price: 24\n'
                       'rental_price: 5.0\n'
                       'brand: GE\n'
                       'voltage: 3.2\n')

        # Test that a blank full inventory is created.
        with patch('builtins.input', side_effect=inv_details):
            main.add_new_item()
        with patch('builtins.input', side_effect=app_details):
            main.add_new_item()
        with patch('builtins.input', side_effect=furn_details):
            main.add_new_item()

        # Test that all items were added to the full inventory.
        self.assertEqual(main.FULL_INVENTORY, expected_dict)

        # Test that an applicance item was added to the full inventory.
        with patch('builtins.input', side_effect=['002']):
            self.assertEqual(main.item_info(), print(test_string))
