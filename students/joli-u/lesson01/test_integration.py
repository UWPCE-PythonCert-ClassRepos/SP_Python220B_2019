"""
test_integration.py
joli umetsu
py220
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
import sys

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.market_prices as market_prices
import inventory_management.main as main


class TestInventoryManagementIntegration(TestCase):
    """ tests inventory management integration """

    def test_integration(self):
        """ checks that items are added to full inventory dict correctly """
        check_dict = {}

        
        with patch('builtins.input') as mock_input:
        
            # adding a furniture item
            mock_input.side_effect = ['1', '199021', 'desk', '800', 'y', 'gold', 'm']
            main.main_menu()()
            
            check_dict['199021'] = {'product_code': '199021', 
                                    'description': 'desk',
                                    'market_price': 24,
                                    'rental_price': '800',
                                    'material': 'gold',
                                    'size': 'm'}

            self.assertEqual(main.FULL_INVENTORY, check_dict)
            self.assertIn('199021', main.FULL_INVENTORY)
            
            # adding an electrical item
            mock_input.side_effect = ['1', '532112', 'dryer', '600', 'n', 'y', 'ge', '120']
            main.main_menu()()
            
            check_dict['532112'] = {'product_code': '532112', 
                                    'description': 'dryer',
                                    'market_price': 24,
                                    'rental_price': '600',
                                    'brand': 'ge',
                                    'voltage': '120'}
            
            self.assertEqual(main.FULL_INVENTORY, check_dict)
            self.assertIn('532112', main.FULL_INVENTORY)
            
            # adding an inventory item
            mock_input.side_effect = ['1', '243354', 'stuff', '10', 'n', 'n']
            main.main_menu()()
            
            check_dict['243354'] = {'product_code': '243354', 
                                    'description': 'stuff',
                                    'market_price': 24,
                                    'rental_price': '10'}
                                    
            self.assertEqual(main.FULL_INVENTORY, check_dict)
            self.assertIn('243354', main.FULL_INVENTORY)
            self.assertIn('199021', main.FULL_INVENTORY)
            
            # getting item info
            mock_input.side_effect = ['2', '199021']
            check_output = "product_code:199021\ndescription:desk\nmarket_price:24,rental_price:800\nmaterial:gold\nsize:m"

            self.assertEqual(main.main_menu()(), print(check_output))
        
            # getting item info for item that doesn't exist
            mock_input.side_effect = ['2', '34']
            check_output = "Item not found in inventory"
            
            self.assertEqual(main.main_menu()(), print(check_output))
            
            # exiting
            main.exit_program = MagicMock()
            mock_input.side_effect = ['q']
            main.main_menu()()
            
            main.exit_program.assert_called()