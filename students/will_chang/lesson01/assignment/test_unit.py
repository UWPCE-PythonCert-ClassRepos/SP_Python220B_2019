import sys
import io

from unittest import TestCase
from unittest.mock import patch

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.main as main
import inventory_management.market_prices as market_prices

# Excluded __name__ == '__main__' in .coveragerc config file

class ElectricAppliancesTests(TestCase):
    def test_electric_appliances(self):
        electric_appliance = ElectricAppliances(1, 'Toaster', 10,
                                                5, 'Frys', 220)
        electric_dict_test = electric_appliance.return_as_dictionary()
        
        self.assertEqual(electric_dict_test, {'product_code': 1,
                                              'description': 'Toaster',
                                              'market_price': 10,
                                              'rental_price': 5,
                                              'brand': 'Frys',
                                              'voltage': 220})
                            
class FurnitureTests(TestCase):
    def test_furniture(self):
        furniture = Furniture(2, 'Chair', 25, 10, 'Leather', 'S')
        furniture_dict_test = furniture.return_as_dictionary()
        self.assertEqual(furniture_dict_test, {'product_code': 2,
                                               'description': 'Chair',
                                               'market_price': 25,
                                               'rental_price': 10,
                                               'material': 'Leather',
                                               'size': 'S'})

class InventoryTests(TestCase):
    def test_inventory(self):
        inventory = Inventory(3, 'Desk', 30, 20)
        inventory_dict_test = inventory.return_as_dictionary()
        self.assertEqual(inventory_dict_test, {'product_code': 3,
                                               'description': 'Desk',
                                               'market_price': 30,
                                               'rental_price': 20})
                                               
class MarketPricesTests(TestCase):
    def test_market(self):
        self.assertEqual(24, market_prices.get_latest_price(20))
        
class MainTests(TestCase):
    def test_main_menu_options(self):
        with patch('builtins.input', side_effect = '1'):
            self.assertEqual(main.main_menu().__name__, 'add_new_item')
        with patch('builtins.input', side_effect = '2'):
            self.assertEqual(main.main_menu().__name__, 'item_info')
        with patch('builtins.input', side_effect = 'q'):
            self.assertEqual(main.main_menu().__name__, 'exit_program')
            
    def test_get_price(self):
        self.assertEqual(24, main.get_price(1))
        
    def test_add_item(self):
        isfurniture_input = (15, 'Futon', 5, 'y', 'cardboard', 'L')
        current_inventory = {15: {'product_code': 15, 'description': 'Futon',
                                  'market_price': 24, 'rental_price': 5,
                                  'material': 'cardboard', 'size': 'L'}}
        with patch('builtins.input', side_effect = isfurniture_input):
            main.add_new_item()
            self.assertEqual(current_inventory, main.FULL_INVENTORY)
        
        iselectric_appliance_input = (2507, 'Oven', 17, 'n', 'y', 'GE', 10)
        current_inventory = {15: {'product_code': 15, 'description': 'Futon',
                                  'market_price': 24, 'rental_price': 5,
                                  'material': 'cardboard', 'size': 'L'},
                             2507: {'product_code': 2507, 'description': 'Oven',
                                    'market_price': 24, 'rental_price': 17,
                                    'brand': 'GE', 'voltage': 10}}
        with patch('builtins.input', side_effect = iselectric_appliance_input):
            main.add_new_item()
            self.assertEqual(current_inventory, main.FULL_INVENTORY)                         
            
        is_other_item_input = (177, 'mittens', 2, 'n', 'n')
        current_inventory = {15: {'product_code': 15, 'description': 'Futon',
                                  'market_price': 24, 'rental_price': 5,
                                  'material': 'cardboard', 'size': 'L'},
                             2507: {'product_code': 2507, 'description': 'Oven',
                                    'market_price': 24, 'rental_price': 17,
                                    'brand': 'GE', 'voltage': 10},
                             177: {'product_code': 177, 'description': 'mittens',
                                   'market_price': 24, 'rental_price': 2,}}
        with patch('builtins.input', side_effect = is_other_item_input):
            main.add_new_item()
            self.assertEqual(current_inventory, main.FULL_INVENTORY)    
    
    def test_item_info_none(self):
        with patch('builtins.input', side_effect = '25'):
            main.item_info()
            self.assertEqual(main.item_info(), None)

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            main.exit_program()
            
if __name__ == '__main__':
    unittest.main()