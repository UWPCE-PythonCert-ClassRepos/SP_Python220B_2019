from unittest import TestCase
from unittest.mock import patch

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.main as main
import inventory_management.market_prices as market_prices

class ModuleTests(TestCase):

    def test_module(self):
        add_furniture = (256979, 'Comfy Sofa', 5, 'y', 'cobblestone', 'L')
        current_inventory = {256979: {'product_code': 256979, 'description': 'Comfy Sofa',
                                  'market_price': 24, 'rental_price': 5,
                                  'material': 'cobblestone', 'size': 'L'}}
        with patch('builtins.input', side_effect = add_furniture):
            main.add_new_item()
            self.assertEqual(current_inventory, main.FULL_INVENTORY)
        
        add_appliance = (707, 'Microwave', 17, 'n', 'y', 'SOS', 10)
        current_inventory = {256979: {'product_code': 256979, 'description': 'Comfy Sofa',
                                  'market_price': 24, 'rental_price': 5,
                                  'material': 'cobblestone', 'size': 'L'},
                             707: {'product_code': 707, 'description': 'Microwave',
                                    'market_price': 24, 'rental_price': 17,
                                    'brand': 'SOS', 'voltage': 10}}
        with patch('builtins.input', side_effect = add_appliance):
            main.add_new_item()
            self.assertEqual(current_inventory, main.FULL_INVENTORY)                         
            
        add_other = (177, 'shoes', 2, 'n', 'n')
        current_inventory = {256979: {'product_code': 256979, 'description': 'Comfy Sofa',
                                  'market_price': 24, 'rental_price': 5,
                                  'material': 'cobblestone', 'size': 'L'},
                             707: {'product_code': 707, 'description': 'Microwave',
                                    'market_price': 24, 'rental_price': 17,
                                    'brand': 'SOS', 'voltage': 10},
                             177: {'product_code': 177, 'description': 'shoes',
                                   'market_price': 24, 'rental_price': 2,}}
        with patch('builtins.input', side_effect = add_other):
            main.add_new_item()
            self.assertEqual(current_inventory, main.FULL_INVENTORY)
            
        self.assertEqual(24, market_prices.get_latest_price(20))    
            
        with self.assertRaises(SystemExit):
            main.exit_program()