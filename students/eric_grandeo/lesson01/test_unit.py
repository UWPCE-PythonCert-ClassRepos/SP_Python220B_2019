from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

import sys
sys.path.append('./inventory_management')
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.market_prices import get_latest_price
#from inventory_management.main import main_menu, get_price, add_new_item, item_info, exit_program
import inventory_management.main as main

class InventoryTests(TestCase):

    def test_inventory(self):
        test_inv = Inventory(1234, "test product", 567, 246)    
        self.assertIsInstance(test_inv, Inventory)
        test_dict = {"product_code": 1234, "description": "test product",
                     "market_price": 567, "rental_price": 246}
        self.assertDictEqual(test_dict, test_inv.return_as_dictionary())
        
class ElectricAppliancesTest(TestCase):
    
    def test_electric_inventory(self):
        test_elect_inv = ElectricAppliances(1234, "test product", 567, 246, "My Brand", 440)    
        self.assertIsInstance(test_elect_inv, ElectricAppliances)
        test_elect_dict = {"product_code": 1234, "description": "test product",
                     "market_price": 567, "rental_price": 246, "brand": "My Brand",
                     "voltage": 440}
        self.assertDictEqual(test_elect_dict, test_elect_inv.return_as_dictionary())
        
class FurnitureTest(TestCase):
    
    def test_furniture(self):
        test_furn = Furniture(1234, "test product", 567, 246, "wood", "L")    
        self.assertIsInstance(test_furn, Furniture)
        test_furn_dict = {"product_code": 1234, "description": "test product",
                     "market_price": 567, "rental_price": 246, "material": "wood",
                     "size": "L"}
        self.assertDictEqual(test_furn_dict, test_furn.return_as_dictionary())

class MarketPriceTest(TestCase):
    
    def test_market_price(self):
        self.assertEqual(get_latest_price('test'),24)

class MainTest(TestCase):
    
    def test_main_menu(self):
        test_input = {"1": "add_new_item", "2": "item_info", "q": "exit_program"}
        for key, value in test_input.items():
            with patch('builtins.input', side_effect=key): 
                main_resp = main.main_menu()
                self.assertEqual(main_resp.__name__, value)
                
    def test_add_new_item_furn(self):
        furn_inputs = ['123', 'table', '456', 'y', 'wood', 'm']
        furn_output = {'product_code': '123',
                      'description': 'table',
                      'market_price': 24,
                      'rental_price': '456',
                      'material': 'wood',
                      'size': 'm'}
        
        with patch('builtins.input', side_effect=furn_inputs):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY['123'], furn_output)
            
    def test_add_new_item_elec(self):
        elec_inputs = ['321', 'blender', '456', 'n', 'y', 'samsung', '120']
        elec_output = {'product_code': '321',
                      'description': 'blender',
                      'market_price': 24,
                      'rental_price': '456',
                      'brand': 'samsung',
                      'voltage': '120'}
        
        with patch('builtins.input', side_effect=elec_inputs):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY['321'], elec_output)

