"""Integration testing for inventory management system"""

from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from inventory_management.market_prices import get_latest_price
from inventory_management.product_classes import Inventory, Furniture, ElectricAppliances
import inventory_management.main as menu

class IntegrationTest(TestCase):
    """ This class tests integration for inventory management system"""

    def test_integration(self):

        market_price = get_latest_price(44)

        furn_item = (44, 'Test description', 50, 'y', 'leather', 'L')
        elec_item = (22, 'Test description', 50, 'n', 'y', 'John Deere', 200)
        other_item = (99, 'Test description', 50, 'n', 'n')

        menu.FULL_INVENTORY = {}
        with patch('builtins.input', side_effect = furn_item):
            menu.add_new_item()
        with patch('builtins.input', side_effect = elec_item):
            menu.add_new_item()
        with patch('builtins.input', side_effect = other_item):
            menu.add_new_item()

        test_dict = {44: {'product_code': 44, 'description': 'Test description', 
                    'market_price': 24, 'rental_price': 50, 'material': 'leather', 'size': 'L'}, 
                    22: {'product_code': 22, 'description': 'Test description', 'market_price': 24, 
                    'rental_price': 50, 'brand': 'John Deere', 'voltage': 200}, 
                    99: {'product_code': 99, 'description': 'Test description', 
                    'market_price': 24, 'rental_price': 50}}
                    
        self.assertEqual(menu.FULL_INVENTORY, test_dict)
        #menu.add_new_item()
        #menu.add_new_item()

