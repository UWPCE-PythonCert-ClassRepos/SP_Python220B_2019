# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 13:44:20 2019

@author: Laura.Fiorentino
"""
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from inventory_management.main import main_menu
import inventory_management


class FurnitureTests(TestCase):
    def test_furniture(self):
        furniture_test = inventory_management. \
            furniture.Furniture('100', 'description', 'marketprice',
                                'rentalprice', 'material', 'size')
        furniture_test_2 = furniture_test.return_as_dictionary()
        self.assertEqual(furniture_test_2, {'product_code': '100',
                                            'description': 'description',
                                            'market_price': 'marketprice',
                                            'rental_price': 'rentalprice',
                                            'material': 'material',
                                            'size': 'size'})


class ElectricTests(TestCase):
    def test_electric(self):
        electric_test = inventory_management.electricappliances. \
            ElectricAppliances('200', 'description', 'marketprice',
                               'rentalprice', 'brand', 'voltage')
        electric_test_2 = electric_test.return_as_dictionary()
        self.assertEqual(electric_test_2, {'product_code': '200',
                                           'description': 'description',
                                           'market_price': 'marketprice',
                                           'rental_price': 'rentalprice',
                                           'brand': 'brand',
                                           'voltage': 'voltage'})


class InventoryTests(TestCase):
    def test_inventory(self):
        inventory_test = inventory_management. \
            inventory.Inventory('300', 'description', 'marketprice',
                                'rentalprice')
        inventory_test_2 = inventory_test.return_as_dictionary()
        self.assertEqual(inventory_test_2, {'product_code': '300',
                                            'description': 'description',
                                            'market_price': 'marketprice',
                                            'rental_price': 'rentalprice'})


class PriceTests(TestCase):
    def test_getprice(self):
        price = inventory_management.market_prices.get_latest_price('1')
        self.assertEqual(price, 24)


class MainTests(TestCase):
    def test_main_menu_add(self):
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main_menu(),
                             inventory_management.main.add_new_item)

    def test_main_menu_info(self):
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main_menu(), inventory_management.main.item_info)

    def test_main_menu_quit(self):
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main_menu(),
                             inventory_management.main.exit_program)

    def test_getprice(self):
        self.get_price = MagicMock(return_value=24)
        self.assertEqual(24, inventory_management.main.get_price(1))

    def test_add_new_item(self):
        furniture_input = ['100', 'description', 'rentalprice', 'y',
                           'material', 'size']
        electric_input = ['200', 'description', 'rentalprice', 'n', 'y',
                          'brand', 'voltage']
        other_input = ['300', 'description', 'rentalprice', 'n', 'n']
        with patch('builtins.input', side_effect=furniture_input):
            test_inventory = inventory_management.main.add_new_item()
            test_return_furniture = {'100': {'product_code': '100',
                                             'description': 'description',
                                             'market_price': 24,
                                             'rental_price': 'rentalprice',
                                             'material': 'material',
                                             'size': 'size'}}
            self.assertEqual(test_return_furniture, test_inventory)
        with patch('builtins.input', side_effect=electric_input):
            test_inventory = inventory_management.main.add_new_item()
            test_return_electrics = {'100': {'product_code': '100',
                                             'description': 'description',
                                             'market_price': 24,
                                             'rental_price': 'rentalprice',
                                             'material': 'material',
                                             'size': 'size'},
                                     '200': {'product_code': '200',
                                             'description': 'description',
                                             'market_price': 24,
                                             'rental_price': 'rentalprice',
                                             'brand': 'brand',
                                             'voltage': 'voltage'}}
            self.assertEqual(test_return_electrics, test_inventory)
        with patch('builtins.input', side_effect=other_input):
            test_inventory = inventory_management.main.add_new_item()
            test_return_other = {'100': {'product_code': '100',
                                         'description': 'description',
                                         'market_price': 24,
                                         'rental_price': 'rentalprice',
                                         'material': 'material',
                                         'size': 'size'},
                                 '200': {'product_code': '200',
                                         'description': 'description',
                                         'market_price': 24,
                                         'rental_price': 'rentalprice',
                                         'brand': 'brand',
                                         'voltage': 'voltage'},
                                 '300': {'product_code': '300',
                                         'description': 'description',
                                         'market_price': 24,
                                         'rental_price': 'rentalprice'}}
            self.assertEqual(test_return_other, test_inventory)

    def test_item_info(self):
        FULL_INV = {'100': {'product_code': '100',
                            'description': 'description',
                            'market_price': 24,
                            'rental_price': 'rentalprice',
                            'material': 'material',
                            'size': 'size'}}
        with patch('builtins.input', return_value='100'):
            test_info = {'product_code': '100',
                         'description': 'description',
                         'market_price': 24,
                         'rental_price': 'rentalprice',
                         'material': 'material',
                         'size': 'size'}
            self.assertEqual(inventory_management.main.item_info(FULL_INV),
                             test_info)
        with patch('builtins.input', side_effect='500'):
            self.assertEqual(inventory_management.main.item_info(FULL_INV),
                             None)

    def test_exit(self):
        with self.assertRaises(SystemExit):
            inventory_management.main.exit_program()
