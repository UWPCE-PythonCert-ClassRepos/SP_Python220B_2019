"""Creates an integration test that runs Inventroy Management as a whole"""

import sys
sys.path.append('/Users/allth/OneDrive/Desktop/Python/Python220/'
                'SP_Python220B_2019/students/dfspray/Lesson01/inventory_management')
import unittest
import unittest.mock
from unittest.mock import patch
import inventory_management.market_prices as market_prices
import inventory_management.main as main
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory

class IntegrationTest(unittest.TestCase):
    """Creates a class that tests inventory_management together"""
    def test_main_integration(self):
        """Test all functions with main as a starting point"""

        price = market_prices.get_latest_price(0)

        #Adding non categorized inventory item with main
        item1 = ['1', 'shoe', '1', 'n', 'n']
        with patch('builtins.input', side_effect=item1):
            main.add_new_item()

        unintegrated_item1 = Inventory(['1', 'shoe', price, '1'])

        #Adding furniture item with main
        item2 = ['2', 'chair', '2', 'y', 'wood', 'S']
        with patch('builtins.input', side_effect=item2):
            main.add_new_item()

        unintegrated_item2 = Furniture(['2', 'chair', price, '2'], 'wood', 'S')

        #Adding electric appliance with main
        item3 = ['3', 'stove', '3', 'n', 'y', 'LG', '100']
        with patch('builtins.input', side_effect=item3):
            main.add_new_item()

        unintegrated_item3 = ElectricAppliances(['3', 'stove', price, '3'], 'LG', '100')

        actual_inventory = main.return_full_inventory()
        expected_inventory = {
            '1': unintegrated_item1.return_as_dictionary(),
            '2': unintegrated_item2.return_as_dictionary(),
            '3': unintegrated_item3.return_as_dictionary()}

        self.assertEqual(actual_inventory, expected_inventory)
