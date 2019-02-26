"""Test File for testing inventory management files"""
import sys
sys.path.append('/Users/njschafi/desktop/python220/SP_Python220B_2019/'
                'students/njschafi/lesson01/inventory_management')

from unittest import TestCase
from mock import patch
from inventory_class import Inventory
from electric_appliances_class import ElectricAppliances
from furniture_class import Furniture
from market_prices import get_latest_price
from main import add_new_item, return_inventory, item_info
from main import main_menu, get_price, exit_program


class InventoryTest(TestCase):
    """Tests Inventory Class"""
    def test_inventory(self):
        """Tests the creation of an instance for inventory object"""
        test_dict = {'product_code': 6789, 'description': 'Horse',
                     'market_price': 50, 'rental_price': 10}
        test_inv = Inventory(6789, 'Horse', 50, 10)
        self.assertEqual(test_dict, test_inv.return_as_dictionary())

class FurnitureTest(TestCase):
    """Tests Furniture Class"""
    def test_furniture(self):
        """Tests the creation of an instance for furniture object"""
        test_dict = {'product_code': 6789, 'description': 'Horse',
                     'market_price': 50, 'rental_price': 10,
                     'material': 'Leather', 'size': 'Large'}
        test_furn = Furniture(6789, 'Horse', 50, 10, 'Leather', 'Large')
        self.assertEqual(test_dict, test_furn.return_as_dictionary())

class ElectricAppliancesTest(TestCase):
    """Tests ElectricAppliancesTest Class"""
    def test_electric(self):
        """Tests the creation of an instance for electric object"""
        test_dict = {'product_code': 6789, 'description': 'Horse',
                     'market_price': 50, 'rental_price': 10,
                     'brand': 'Sony', 'voltage': 28}
        test_elec = ElectricAppliances(6789, 'Horse', 50, 10, 'Sony', 28)
        self.assertEqual(test_dict, test_elec.return_as_dictionary())

class MarketPriceTest(TestCase):
    """Tests get_latest_price function"""
    def test_price(self):
        """""Tests if correct market price gets returned"""
        test_price = 24
        self.assertEqual(test_price, get_latest_price(403))

class MainTest(TestCase):
    """Tests main module"""
    def test_main_menu(self):
        """Tests main menu"""
        user_input = ['1']
        with patch('builtins.input', side_effect=user_input):
            function = main_menu()
        self.assertEqual(function.__name__, 'add_new_item')

    def test_get_price(self):
        """Tests get_price method"""
        self.assertEqual(24, get_price(5))

    def test_add_new_item(self):
        """Tests that each type of item (Furniture, Electric, Regular) gets
        added to inventory"""
        input1 = [1, 'horse', 10, 'n', 'n']
        test_inventory = {1: {'product_code': 1, 'description': 'horse',
                              'market_price': 24, 'rental_price': 10}}
        with patch('builtins.input', side_effect=input1):
            add_new_item()
        self.assertEqual(test_inventory, return_inventory())

        #add electric appliance to inventory
        input2 = [2, 'mixer', 5, 'n', 'y', 'sony', 5]
        test_inventory = {1: {'product_code': 1, 'description': 'horse',
                              'market_price': 24, 'rental_price': 10},
                          2: {'product_code': 2, 'description': 'mixer',
                              'market_price': 24, 'rental_price': 5, 'brand': 'sony',
                              'voltage': 5}}
        with patch('builtins.input', side_effect=input2):
            add_new_item()
        self.assertEqual(test_inventory, return_inventory())

        #add furniture to inventory
        input3 = [3, 'couch', 3, 'y', 'leather', 'L']
        test_inventory = {1: {'product_code': 1, 'description': 'horse',
                              'market_price': 24, 'rental_price': 10},
                          2: {'product_code': 2, 'description': 'mixer',
                              'market_price': 24, 'rental_price': 5,
                              'brand': 'sony', 'voltage': 5},
                          3: {'product_code': 3, 'description': 'couch',
                              'market_price': 24, 'rental_price': 3,
                              'material': 'leather', 'size': 'L'}}
        with patch('builtins.input', side_effect=input3):
            add_new_item()
        self.assertEqual(test_inventory, return_inventory())

    def test_no_item_info(self):
        """Tests if item_info gets returned"""
        input4 = [22]
        with patch('builtins.input', side_effect=input4):
            item = item_info()
        self.assertEqual(item, None)

    def test_item_info(self):
        """Tests if item_info gets returned"""
        input4 = [1]
        with patch('builtins.input', side_effect=input4):
            item = item_info()
        self.assertEqual(item, None)

    def test_exit_program(self):
        """Tests if program exits properly"""
        with self.assertRaises(SystemExit):
            exit_program()
