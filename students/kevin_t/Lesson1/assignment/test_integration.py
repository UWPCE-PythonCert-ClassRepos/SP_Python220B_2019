""" Integration testing for the HP Norton Project """

from unittest import TestCase
from unittest.mock import patch
import sys
sys.path.append('inventory_management')
from inventory_class import Inventory
from electric_appliance_class import ElectricAppliances
from furniture_class import Furniture
from main import main_menu, get_price, add_new_item, item_info, exit_program, FULL_INVENTORY

class ModuleTest(TestCase):
    """ Verify that the entire module operates as expected"""
    def test_module(self):
        """ Verify that furniture is correctly added to the FULL_INVENTORY dictionary """
        example_furniture = ('1', '50', 'desk', 100, 'y', 'wood', 'M')
        correct_furniture_dict = {'50': {'product_code': '50', 'description': 'desk',
                               'market_price': 24, 'rental_price': 100,
                               'material': 'wood', 'size': 'M'}}

        with patch('builtins.input', side_effect=example_furniture):
            main_menu()()
        self.assertEqual(FULL_INVENTORY, correct_furniture_dict)

        """ Verify that electrical appliances are correctly added to the FULL_INVENTORY dictionary """
        example_electrical = ('\n', '1', '200', 'vacuum', 250, 'n', 'y', 'dyson', '220')
        correct_electrical_dict = {'50': {'product_code': '50', 'description': 'desk',
                                          'market_price': 24, 'rental_price': 100,
                                          'material': 'wood', 'size': 'M'},
                                   '200': {'product_code': '200', 'description': 'vacuum',
                                           'market_price': 24, 'rental_price': 250,
                                           'brand': 'dyson', 'voltage': '220'}}

        with patch('builtins.input', side_effect=example_electrical):
            main_menu()()
        self.assertEqual(FULL_INVENTORY, correct_electrical_dict)

        """ Verify that miscellaneous items are correctly added to the FULL_INVENTORY dictionary """
        example_item = ('\n', '1', '45', 'lamp', 10, 'n', 'n', 'n')
        correct_item_dict = {'50': {'product_code': '50', 'description': 'desk',
                                    'market_price': 24, 'rental_price': 100,
                                    'material': 'wood', 'size': 'M'},
                             '200': {'product_code': '200', 'description': 'vacuum',
                                     'market_price': 24, 'rental_price': 250,
                                     'brand': 'dyson', 'voltage': '220'},
                             '45': {'product_code': '45', 'description': 'lamp',
                                    'market_price': 24, 'rental_price': 10}}

        with patch('builtins.input', side_effect=example_item):
            main_menu()()
        self.assertEqual(FULL_INVENTORY, correct_item_dict)

        """ Verify that items can correctly be recalled from FULL_INVENTORY dictionary """
        example_item_query = ('\n', '2', 200)

        with patch('builtins.input', side_effect=example_item_query):
            self.assertEqual(main_menu(), item_info)

        """ Verify that non-existing items are correctly identified from FULL_INVENTORY dictionary """
        example_quit = ('\n', 'q')

        with patch('builtins.input', side_effect=example_quit):
            self.assertEqual(main_menu(), exit_program)