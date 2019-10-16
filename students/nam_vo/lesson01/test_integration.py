from unittest.mock import MagicMock
from unittest import TestCase

from inventory_management.inventoryClass import inventory
from inventory_management.electricAppliancesClass import electricAppliances
from inventory_management.furnitureClass import furniture
from inventory_management import market_prices
from inventory_management import main

class ModuleTests(TestCase):
    
    def test_module(self):
        full_inventory = {}
        # full_inventory = {
        #     'e': electricAppliances('e', 'this is a test inventory', 1000, 1200, 'python', 110),
        #     'f': furniture('f', 'this is a test inventory', 1000, 1200, 'plastic', '12x12'),
        # }

        # Get price
        self.assertEqual(24, market_prices.get_latest_price('e'))
        self.assertEqual(24, market_prices.get_latest_price('f'))

        # Add new electric appliance and new furniture
        full_inventory['e'] = electricAppliances('e', 'this is a test inventory', 1000, 1200, 'python', 110).returnAsDictionary()
        full_inventory['f'] = furniture('f', 'this is a test inventory', 1000, 1200, 'plastic', '12x12').returnAsDictionary()
