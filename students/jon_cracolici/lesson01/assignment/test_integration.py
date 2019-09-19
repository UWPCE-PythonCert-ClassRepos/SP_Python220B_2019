"""This is an integration test of the inventory management system."""

from unittest import TestCase
from unittest.mock import patch
import unittest
import sys
import io
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
import inventory_management
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.main import main_menu, get_price, add_new_item, item_info, exit_program, FULL_INVENTORY
from inventory_management.market_prices import get_latest_price

class TestIntegrationClass(TestCase):
    """Tests integrated control flow, simulating user experience."""
    
    def test_user_run(self):
        """This emulates a hypothetical users behavior."""
        
        #Inputs and expected values
        user_in_1 = ['qws', '1']
        user_in_2 = ['2222', 'new generic product', '60.00', 'n', 'n']
        user_in_3 = ['3333', 'new electric product', '100.00', 'n', 'y', 'Atari', '120 volts']
        user_in_4 = ['4444', 'new furniture product', '40.00', 'y', 'cedar', 'L']
        expected_dict_2 = {'product_code': '2222', 'description': 'new generic product',
                           'market_price': 24, 'rental_price': '60.00'}
        expected_dict_3 = {'product_code': '3333', 'description': 'new electric product',
                           'market_price':24, 'rental_price': '100.00', 'brand': 'Atari',
                           'voltage': '120 volts'}
        expected_dict_4 = {'product_code': '4444', 'description': 'new furniture product',
                           'market_price': 24, 'rental_price': '40.00', 'material': 'cedar',
                           'size': 'L'}
        target_1 = 'product_code:3333\ndescription:new electric product\n'
        target_2 = 'market_price:24\nrental_price:100.00\nbrand:Atari\n'
        target_3 = 'voltage:120 volts\n'
        info_target = target_1+target_2+target_3
        
        #try out the program 
        with patch('builtins.input', side_effect=user_in_1):
            main_menu()

            #adding items
            with patch('builtins.input', side_effect=user_in_2):
                add_new_item()
                self.assertEqual(expected_dict_2, FULL_INVENTORY['2222'])      
            with patch('builtins.input', side_effect=user_in_3):
                add_new_item()
                self.assertEqual(expected_dict_3, FULL_INVENTORY['3333']) 
            with patch('builtins.input', side_effect=user_in_4):
                add_new_item()
                self.assertEqual(expected_dict_4, FULL_INVENTORY['4444']) 
                            
            #print(FULL_INVENTORY) 
            
        #getting an item's info
        with patch('builtins.input', side_effect='2'):
            main_menu()
            with patch('builtins.input', side_effect=user_in_3):
                with patch('sys.stdout', new=io.StringIO()) as print_result:
                    item_info()
        self.assertEqual(info_target, print_result.getvalue())
        
        #quitting the program
        with patch('builtins.input', side_effect='q'):
            main_menu()
            with self.assertRaises(SystemExit):
                exit_program()
                    
                
            
#        with patch('builtins.input', side_effect=user_in_0):
#            main_menu() 
#            print(FULL_INVENTORY)
