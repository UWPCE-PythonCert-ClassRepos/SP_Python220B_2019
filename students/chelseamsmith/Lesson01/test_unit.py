"""Inventory management unit tests"""
from unittest import TestCase
from unittest.mock import patch
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.main as main
import inventory_management.market_prices as market_prices
import io


class ElectricAppliancesTests(TestCase):
    """unit tests for Electric Appliances class"""

    def test_electric_appliances(self):
        """tests the electric appliances initialization
        and return as dictionary methods"""
        appliance = ElectricAppliances('1', 'tv', 100, 25, 'Samsung', '60')
        self.assertEqual(appliance.return_as_dictionary(), {'product_code': '1',
                         'description': 'tv',
                         'market_price': 100,
                         'rental_price': 25,
                         'brand': 'Samsung',
                         'voltage': '60'})


class FurnitureTests(TestCase):
    """unit tests for Furniture class"""

    def test_furniture(self):
        """tests the furniture initialization
        and return as dictionary methods"""
        furnishing = Furniture('2', 'table', 200, 50, 'wood', 'L')
        self.assertEqual(furnishing.return_as_dictionary(), {'product_code': '2',
                         'description': 'table',
                         'market_price': 200,
                         'rental_price': 50,
                         'material': 'wood',
                         'size': 'L'})


class InventoryTests(TestCase):
    """unit tests for Furniture class"""

    def test_inventory(self):
        """tests the inventory initialization
        and return as dictionary methods"""
        thingie = Inventory('3', 'vase', 50, 10,)
        self.assertEqual(thingie.return_as_dictionary(), {'product_code': '3',
                         'description': 'vase',
                         'market_price': 50,
                         'rental_price': 10,})


class MainTests(TestCase):
    """unit tests for main module"""

    def test_main_menu_1(self):
        """tests the main menu function option 1"""
        with patch('builtins.input', side_effect="1"):
            self.assertEqual(main.main_menu().__name__, "add_new_item")

    def test_main_menu_2(self):
        """tests the main menu function option 2"""
        with patch('builtins.input', side_effect="2"):
            self.assertEqual(main.main_menu().__name__, "item_info")

    def test_main_menu_q(self):
        """tests the main menu function option q"""
        with patch('builtins.input', side_effect="q"):
            self.assertEqual(main.main_menu().__name__, "exit_program")

    def test_get_prices(self):
        """tests the get prices function"""
        self.assertEqual(main.get_price("1"), 24)

    def test_add_new_item_furniture(self):
        """tests the add new item function for furniture"""
        main.FULL_INVENTORY={}
        input_furniture = ('2', 'table', 50, 'y', 'wood', 'L')
        test_inventory = {'2': {'product_code': '2',
                         'description': 'table',
                         'market_price': 24,
                         'rental_price': 50,
                         'material': 'wood',
                         'size': 'L'}}
        with patch('builtins.input', side_effect = input_furniture):
            main.add_new_item()
            self.assertEqual(test_inventory, main.return_inventory())

    def test_add_new_item_appliance(self):
        """test the add new item function for electric appliances"""
        main.FULL_INVENTORY={}
        input_appliance = ('1', 'tv', 25, 'n', 'y', 'Samsung', '60')
        test_inventory = {'1':{'product_code': '1',
                         'description': 'tv',
                         'market_price': 24,
                         'rental_price': 25,
                         'brand': 'Samsung',
                         'voltage': '60'}}
        with patch('builtins.input', side_effect = input_appliance):
            main.add_new_item()
            self.assertEqual(test_inventory, main.return_inventory())

    def test_add_new_item_generic(self):
        """test the add new item function for inventory class"""
        main.FULL_INVENTORY = {}
        input_inventory = ('3', 'vase', 10, 'n', 'n')
        test_inventory = {'3': {'product_code': '3',
                         'description': 'vase',
                         'market_price': 24,
                         'rental_price': 10,}}
        with patch('builtins.input', side_effect = input_inventory):
            main.add_new_item()
            self.assertEqual(test_inventory, main.return_inventory())

    def test_item_info_success(self):
        """test the item info function successful retrieval"""
        main.FULL_INVENTORY = {'2': {'product_code': '2',
                         'description': 'table',
                         'market_price': 24,
                         'rental_price': 50,
                         'material': 'wood',
                         'size': 'L'},
                         '3': {'product_code': '3',
                         'description': 'vase',
                         'market_price': 24,
                         'rental_price': 10,}}
        with patch('builtins.input', side_effect = '2'):
            with patch('sys.stdout', new=io.StringIO()) as actual_result:
                main.item_info()
        test_value = '''product_code:2
description:table
market_price:24
rental_price:50
material:wood
size:L
'''
        self.assertEqual(actual_result.getvalue(), test_value)

    def test_item_info_fail(self):
        """test the item info function when no item found"""
        main.FULL_INVENTORY = {'2': {'product_code': '2',
                         'description': 'table',
                         'market_price': 24,
                         'rental_price': 50,
                         'material': 'wood',
                         'size': 'L'},
                         '3': {'product_code': '3',
                         'description': 'vase',
                         'market_price': 24,
                         'rental_price': 10,}}
        with patch('builtins.input', side_effect = '4'):
            with patch('sys.stdout', new=io.StringIO()) as actual_result:
                main.item_info()
        test_value = "Item not found in inventory\n"
        self.assertEqual(actual_result.getvalue(), test_value)

    def test_exit_program(self):
        """tests the exit program function"""
        with self.assertRaises(SystemExit):
            main.exit_program()
