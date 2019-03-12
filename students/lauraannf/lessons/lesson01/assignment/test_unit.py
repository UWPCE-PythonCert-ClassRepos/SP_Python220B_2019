# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:53:15 2019

@author: Laura.Fiorentino
"""

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

from inventory_management.market_prices import get_latest_price
from inventory_management.furniture import Furniture
from inventory_management.inventory import Inventory
from inventory_management.electricappliances import ElectricAppliances
from inventory_management.main import main_menu as main_menu
from inventory_management.main import get_price as get_price, \
    add_new_item as add_new_item, item_info as item_info, \
    exit_program as exit_program


class FurnitureTests(TestCase):
    def test_furniture(self):
        furniture_test = Furniture('100', 'description', 'marketprice',
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
        electric_test = ElectricAppliances('200', 'description', 'marketprice',
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
        inventory_test = Inventory('300', 'description', 'marketprice',
                                   'rentalprice')
        inventory_test_2 = inventory_test.return_as_dictionary()
        self.assertEqual(inventory_test_2, {'product_code': '300',
                                            'description': 'description',
                                            'market_price': 'marketprice',
                                            'rental_price': 'rentalprice'})


class PriceTests(TestCase):
    def test_getprice(self):
        price = get_latest_price('1')
        self.assertEqual(price, 24)


class MainTests(TestCase):
    def test_main_menu_add(self):
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main_menu(), add_new_item)

    def test_main_menu_info(self):
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main_menu(), item_info)

    def test_main_menu_quit(self):
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main_menu(), exit_program)

    def test_getprice(self):
        self.get_price = MagicMock(return_value=24)
        self.assertEqual(24, get_price(1))

    def test_add_new_item(self):
        furniture_input = ['100', 'description', 'rentalprice', 'y',
                           'material', 'size']
        electronic_input = ['200', 'description', 'rentalprice', 'n', 'y',
                            'brand', 'voltage']
        other_input = ['300', 'description', 'rentalprice', 'n', 'n']
        with patch('builtins.input', side_effect=furniture_input):
            test_inventory = add_new_item()
            test_return_furniture = {'100': {'product_code': '100',
                                             'description': 'description',
                                             'market_price': 24,
                                             'rental_price': 'rentalprice',
                                             'material': 'material',
                                             'size': 'size'}}
            self.assertEqual(test_return_furniture, test_inventory)
        with patch('builtins.input', side_effect=electronic_input):
            test_inventory = add_new_item()
            test_return_electronics = {'100': {'product_code': '100',
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
            self.assertEqual(test_return_electronics, test_inventory)
        with patch('builtins.input', side_effect=other_input):
            test_inventory = add_new_item()
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
        furniture_input = ['100', 'description', 'rentalprice', 'y',
                           'material', 'size']
        with patch('builtins.input', side_effect=furniture_input):
            add_new_item()
        with patch('builtins.input', side_effect='100'):
            item_test1 = item_info()
        self.assertEqual(item_test1, None)
        with patch('builtins.input', side_effect='500'):
            item_test2 = item_info()
            self.assertEqual(item_test2, None)

    def test_exit(self):
        with self.assertRaises(SystemExit):
            exit_program()
