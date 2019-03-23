"""Test File for testing inventory management files"""
import sys
sys.path.append('/UW-Python-Advanced/SP_Python220B_2019/students/vvinodh/Lesson1/inventory_management')
from unittest import TestCase
from mock import patch
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price
from inventory_management.main import main_menu, get_price, add_new_item, item_info, exit_program

class InventoryTest(TestCase):
    """Tests Inventory Class"""
    def test_inventory(self):
        """Tests the creation of an instance for inventory object"""
        test_dict = {'product_code': 1011, 'description': 'SuperToy',
                     'market_price': 5, 'rental_price': 1}
        test_inv = Inventory(1011, 'SuperToy', 5, 1)
        self.assertEqual(test_dict, test_inv.return_as_dictionary())

class FurnitureTest(TestCase):
    """Tests Furniture Class"""
    def test_furniture(self):
        """Tests the creation of an instance for furniture object"""
        test_dict = {'product_code': 1012, 'description': 'Chair',
                     'market_price': 50, 'rental_price': 10,
                     'material': 'Leather', 'size': 'Large'}
        test_furn = Furniture(1012, 'Chair', 50, 10, 'Leather', 'Large')
        self.assertEqual(test_dict, test_furn.return_as_dictionary())

class ElectricAppliancesTest(TestCase):
    """Tests ElectricAppliancesTest Class"""
    def test_electric(self):
        """Tests the creation of an instance for electric object"""
        test_dict = {'product_code': 1013, 'description': 'Ipad',
                     'market_price': 500, 'rental_price': 100,
                     'brand': 'Apple', 'voltage': 120}
        test_elec = ElectricAppliances(1013, 'Ipad', 500, 100, 'Apple', 120)
        self.assertEqual(test_dict, test_elec.return_as_dictionary())

class MarketPriceTest(TestCase):
    """Tests get_latest_price function"""
    def test_price(self):
        """""Tests if correct market price gets returned"""
        test_price = 24
        self.assertEqual(test_price, get_latest_price(5000))

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
        self.assertEqual(24, get_price(24))

    def test_add_new_item(self):
        """Tests that each type of item (Furniture, Electric, Regular) gets
        added to inventory"""
        input1 = [1, 'SuperToy', 5, 'n', 'n']
        test_inventory = {1: {'product_code': 1011, 'description': 'SuperToy',
                              'market_price': 5, 'rental_price': 1}}
        with patch('builtins.input', side_effect=input1):
            add_new_item()
        self.assertEqual(test_inventory, return_inventory())

        #add electric appliance to inventory
        input2 = [2, 'Ipad', 500, 'n', 'y', 'Apple', 5]
        test_inventory = {1: {'product_code': 1011, 'description': 'SuperToy',
                              'market_price': 5, 'rental_price': 1},
                          2: {'product_code': 1012, 'description': 'Ipad',
                              'market_price': 500, 'rental_price': 100, 'brand': 'Apple',
                              'voltage': 5}}
        with patch('builtins.input', side_effect=input2):
            add_new_item()
        self.assertEqual(test_inventory, return_inventory())

        #add furniture to inventory
        input3 = [3, 'Chair', 3, 'y', 'leather', 'L']
        test_inventory = {1: {'product_code': 1011, 'description': 'SuperToy',
                              'market_price': 5, 'rental_price': 1},
                          2: {'product_code': 1012, 'description': 'Ipad',
                              'market_price': 500, 'rental_price': 100,
                              'brand': 'Apple', 'voltage': 120},
                          3: {'product_code': 1013, 'description': 'Chair',
                              'market_price': 50, 'rental_price': 3,
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
