# test_unit.py
# All unit tests for all classes in this file

'''Unit tests for the HP Norton Project Assignment'''

import sys
sys.path.append('inventory_management')

from unittest import TestCase
from unittest.mock import patch, MagicMock
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.inventory_class import Inventory
import inventory_management.market_prices as market_prices
import inventory_management.main as main

class TestInventoryClass(TestCase):
    '''Testing the Inventory Class'''

    def test_inventory(self):
        expected = {'product_code': '4509',
                    'description': 'Fire-resistant Water',
                    'market_price': 1.00,
                    'rental_price': 0.05}
        inv_details = Inventory('4509', 'Fire-resistant Water', 1.00, 0.05)

        self.assertEqual(inv_details.return_as_dictionary(), expected)
        self.assertEqual(inv_details.product_code, '4509')
        self.assertEqual(inv_details.description, 'Fire-resistant Water')

class TestEletricAppliancesClass(TestCase):
    '''Testing the Electric Appliances Class'''

    def test_electric_appliances(self):
        expected = {'product_code': '4508',
                    'description': 'Drill',
                    'market_price': 340,
                    'rental_price': 10.00,
                    'brand': 'LG',
                    'voltage': 50000}
        ea_details = ElectricAppliances('4508', 'Drill', 340, 10.00, 'LG', 50000)

        self.assertEqual(ea_details.return_as_dictionary(), expected)
        self.assertEqual(ea_details.brand, 'LG')
        self.assertEqual(ea_details.voltage, 50000)

class TestFurnitureClass(TestCase):
    '''Test the Furniture Class'''

    def test_furniture(self):
        expected = {'product_code': '4510',
                    'description': 'Vase',
                    'market_price': 340,
                    'rental_price': 0,
                    'material': 'Glass',
                    'size': '50 x 50'}
        furn_details = Furniture('4510', 'Vase', 340, 0, 'Glass', '50 x 50')

        self.assertEqual(furn_details.return_as_dictionary(), expected)
        self.assertEqual(furn_details.material, 'Glass')
        self.assertEqual(furn_details.size, '50 x 50')

class TestMarketPrices(TestCase):
    '''Test market_prices'''
    def test_get_latest_price(self):
        self.assertEqual(24, market_prices.get_latest_price(24))

class TestMain(TestCase):
    def test_main_menu(self):
        '''Test that each input results in the corresponding function'''

        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)

        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_get_price(self):
        self.get_price = MagicMock(return_value=24)

    def test_add_new_item(self):
        '''Test that new items are added'''

        furn_details = ['code 1', 'item 1', 10.0, 'y', 'material', 'size']
        ea_details = ['code 2', 'item 2', 20.00, 'N', 'Y', 'brand', 2.4]
        inv_details = ['code 3', 'item 3', 30.00, 'n', 'n']

        expected = {
        'code 1': {'product_code': 'code 1',
                   'description': 'item 1',
                   'market_price': 10.0,
                   'rental_price': 10.0,
                   'material': 'material',
                   'size': 'size'},
        'code 2': {'product_code': 'code 2',
                   'description': 'item 2',
                   'market_price': 20.0,
                   'rental_price': 20.00,
                   'brand': 'brand',
                   'voltage': 2.4},
        'code 3': {'product_code': 'code 3',
                   'description': 'item 3',
                   'market_price': 30.0,
                   'rental_price': 30.00},
        }

        # Test if furniture item is added to the inventory list
        with patch('market_prices.get_latest_price', return_value=10.0):
            with patch('builtins.input', side_effect=furn_details):
                main.FULL_INVENTORY = {}
                main.add_new_item()
                test_furn = {}
                test_furn.setdefault('code 1', expected.get('code 1'))
                self.assertEqual(main.FULL_INVENTORY, test_furn)

        # Test if electric appliance item is added to the inventory list
        with patch('market_prices.get_latest_price', return_value=20.0):
            with patch('builtins.input', side_effect=ea_details):
                main.FULL_INVENTORY = {}
                main.add_new_item()
                test_ea = {}
                test_ea.setdefault('code 2', expected.get('code 2'))
                self.assertEqual(main.FULL_INVENTORY, test_ea)

        # Test that inventory item is added to the inventory list
        with patch('market_prices.get_latest_price', return_value=30.0):
            with patch('builtins.input', side_effect=inv_details):
                main.FULL_INVENTORY = {}
                main.add_new_item()
                test_inv = {}
                test_inv.setdefault('code 3', expected.get('code 3'))
                self.assertEqual(main.FULL_INVENTORY, test_inv)

    def test_item_info(self):
        '''Check if item is in the inventory list when item code is inputted'''

        details = {'product_code': '001',
                   'description': 'clouds',
                   'market_price': 100000.00,
                   'rental_price': 25}
        expected = ('product_code: 1234\n'
                    'description: clouds\n'
                    'market_price: 100000.00\n'
                    'rental_price: 25\n')

        with patch('builtins.input', side_effect=['001']):
            main.FULL_INVENTORY['1234'] = details
            self.assertEqual(main.item_info(), print(expected))

        with patch('builtins.input', side_effect=['999']):
            main.FULL_INVENTORY = []
            expected_message = 'Item not found in inventory'
            self.assertEqual(main.item_info(), print(expected_message))

    def test_exit_program(self):
        '''Test the ability of the program to exit'''

        with self.assertRaises(SystemExit):
            main.exit_program()
