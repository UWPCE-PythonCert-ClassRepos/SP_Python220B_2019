"""Unit Test Module for Inventory Management Software."""

import io
import os
import sys
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(DIR_PATH)

import unittest
from unittest import TestCase
from unittest.mock import patch
import inventory_management
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.main import main_menu, get_price, add_new_item
from inventory_management.main import item_info, exit_program, FULL_INVENTORY
from inventory_management.market_prices import get_latest_price
import inventory_management.main
#from electric_appliances_class import ElectricAppliances
#from furniture_class import Furniture
#from inventory_class import Inventory
#from main import main_menu, get_price, add_new_item
#from main import item_info, exit_program, FULL_INVENTORY
#from market_prices import get_latest_price


class TestInventoryClass(unittest.TestCase):
    """Unit tests for inventory class, which contains one function to store product information."""

    def test_inventory_props(self):
        """"Test to confirm proper storage of product info."""
        trial_instance = Inventory('1111', 'product description', 200.00, 50.00)
        self.assertEqual(trial_instance.product_code, '1111')
        self.assertEqual(trial_instance.description, 'product description')
        self.assertEqual(trial_instance.market_price, 200.00)
        self.assertEqual(trial_instance.rental_price, 50.00)

    def test_inventory_dict(self):
        """Test to confirm proper info translation to a dict."""
        trial_instance = Inventory('1111', 'product description', 200.00, 50.00)
        trial_instance_dict = trial_instance.return_as_dictionary()
        self.assertEqual(trial_instance_dict, {'product_code': '1111',
                                               'description': 'product description',
                                               'market_price': 200.00, 'rental_price': 50.00})


class TestFurnitureClass(unittest.TestCase):
    """Unit tests for Furniture Class, which includes additional "size" and "material" features."""

    def test_furniture_props(self):
        """Test to confirm proper storage of all usual product info,
        and additional furniture info."""
        trial_instance = Furniture('1111', 'product description', 200.00,
                                   50.00, 'leather', 'queen')
        self.assertEqual(trial_instance.material, 'leather')
        self.assertEqual(trial_instance.size, 'queen')

    def test_furniture_dict(self):
        """Test to confirm proper info translation to a dict."""
        trial_instance = Furniture('1111', 'product description', 200.00, 50.00,
                                   'leather', 'queen')
        trial_instance_dict = trial_instance.return_as_dictionary()
        self.assertEqual(trial_instance_dict, {'product_code': '1111',
                                               'description': 'product description',
                                               'market_price': 200.00, 'rental_price': 50.00,
                                               'material': 'leather', 'size': 'queen'})


class TestElectricAppliancesClass(unittest.TestCase):
    """Unit tests for Electric Appliances Class,
    which includes additional "brand" and "voltage" features."""

    def test_electric_apps_props(self):
        """Test to confirm proper storage of all usual product info,
        and additional furniture info."""
        trial_instance = ElectricAppliances('1111', 'product description', 200.00, 50.00,
                                            'Dell', '120 Volts')
        self.assertEqual(trial_instance.brand, 'Dell')
        self.assertEqual(trial_instance.voltage, '120 Volts')

    def test_electric_apps_dict(self):
        """Test to confirm proper info translation to a dict."""
        trial_instance = ElectricAppliances('1111', 'product description', 200.00, 50.00,
                                            'Dell', '120 Volts')
        trial_instance_dict = trial_instance.return_as_dictionary()
        self.assertEqual(trial_instance_dict, {'product_code': '1111',
                                               'description': 'product description',
                                               'market_price': 200.00, 'rental_price': 50.00,
                                               'brand': 'Dell', 'voltage': '120 Volts'})


class TestMarketPrices(unittest.TestCase):
    """Unit test for market prices call function."""

    def test_market_prices(self):
        """Tests proper return of market prices.
        Current functionality returns 24 for all calls."""

        dummy_price = get_latest_price('1111')
        self.assertEqual(dummy_price, 24)


class TestMainControlFlow(unittest.TestCase):
    """Unit tests for control flow of the inventory system."""

    def test_main_menu_1(self):
        """Control flow test for option 1."""

        with patch('builtins.input', side_effect=['1']):
            response = main_menu()
        self.assertEqual(response.__name__, 'add_new_item')

    def test_main_menu_2(self):
        """Control flow test for option 2."""

        with patch('builtins.input', side_effect=['2']):
            response = main_menu()
        self.assertEqual(response.__name__, 'item_info')

    def test_get_price(self):
        """Tests get price function. Note that this tests a placeholder file."""
        FULL_INVENTORY = {'1111': {'product_code': '1111', 'description': 'product description',
                                   'market_price': 24, 'rental_price': 50.00}}
        self.assertEqual(get_price('1111'), 24)

    def test_add_new_item_gen(self):
        """Tests adding new generic inventory item."""

        user_inputs = ['2222', 'new generic product', '60.00', 'n', 'n']
        expected_dict = {'product_code': '2222', 'description': 'new generic product',
                         'market_price': 24, 'rental_price': '60.00'}
        with patch('builtins.input', side_effect=user_inputs):
            add_new_item()
            self.assertEqual(expected_dict, FULL_INVENTORY['2222'])

    def test_add_new_item_electric(self):
        """Tests adding new electric inventory item."""

        user_inputs = ['3333', 'new electric product', '100.00', 'n', 'y', 'Atari', '120 volts']
        expected_dict = {'product_code': '3333', 'description': 'new electric product',
                         'market_price':24, 'rental_price': '100.00', 'brand': 'Atari',
                         'voltage': '120 volts'}
        with patch('builtins.input', side_effect=user_inputs):
            add_new_item()
            self.assertEqual(expected_dict, FULL_INVENTORY['3333'])

    def test_add_new_item_furniture(self):
        """Tests adding new furniture inventory item."""

        user_inputs = ['4444', 'new furniture product', '40.00', 'y', 'cedar', 'L']
        expected_dict = {'product_code': '4444', 'description': 'new furniture product',
                         'market_price': 24, 'rental_price': '40.00', 'material': 'cedar',
                         'size': 'L'}
        with patch('builtins.input', side_effect=user_inputs):
            add_new_item()
            self.assertDictEqual(expected_dict, FULL_INVENTORY['4444'])

    def test_item_info_gen(self):
        """Tests getting info on item in database."""

        target_1 = 'product_code:2222\ndescription:new generic product\n'
        target_2 = 'market_price:24\nrental_price:60.00\n'
        target = target_1 + target_2
        general_item = ['2222', 'new generic product', '60.00', 'n', 'n']

        with patch('builtins.input', side_effect=general_item):
            add_new_item()
            with patch('builtins.input', side_effect=general_item):
                with patch('sys.stdout', new=io.StringIO()) as print_result:
                    item_info()
        self.assertEqual(target, print_result.getvalue())


    def test_item_info_electric(self):
        """Tests getting info on an electric item in database."""

        target_1 = 'product_code:3333\ndescription:new electric product\n'
        target_2 = 'market_price:24\nrental_price:100.00\nbrand:Atari\n'
        target_3 = 'voltage:120 volts\n'
        target = target_1+target_2+target_3
        elect_item = ['3333', 'new electric product', '100.00', 'n', 'y', 'Atari', '120 volts']

        with patch('builtins.input', side_effect=elect_item):
            add_new_item()
            with patch('builtins.input', side_effect=elect_item):
                with patch('sys.stdout', new=io.StringIO()) as print_result:
                    item_info()
        self.assertEqual(target, print_result.getvalue())


    def test_item_info_furniture(self):
        """Tests getting info on a furniture item in database."""

        target_1 = 'product_code:4444\ndescription:new furniture product\n'
        target_2 = 'market_price:24\nrental_price:40.00\nmaterial:cedar\n'
        target_3 = 'size:L\n'
        target = target_1 + target_2 + target_3
        furn_item = ['4444', 'new furniture product', '40.00', 'y', 'cedar', 'L']

        with patch('builtins.input', side_effect=furn_item):
            add_new_item()
            with patch('builtins.input', side_effect=furn_item):
                with patch('sys.stdout', new=io.StringIO()) as print_result:
                    item_info()
        self.assertEqual(target, print_result.getvalue())

    def test_item_info_none(self):
        """Tests the program on returning None when given an invalid item code."""

        target = 'Item not found in inventory\n'
        with patch('builtins.input', side_effect=['turds']):
            with patch('sys.stdout', new=io.StringIO()) as print_result:
                item_info()
        self.assertEqual(target, print_result.getvalue())

    def test_exit_program(self):
        """Tests the ability of the program to quit."""

        with self.assertRaises(SystemExit):
            exit_program()