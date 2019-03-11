# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:52:01 2019

@author: Laura.Fiorentino
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management.furniture import Furniture
from inventory_management.inventory import Inventory
from inventory_management.electricappliances import ElectricAppliances
from inventory_management.main import main_menu as main_menu
from inventory_management.main import get_price as get_price, \
    add_new_item as add_new_item, item_info as item_info, \
    exit_program as exit_program


class FurnitureTests(TestCase):

    def test_furniture(self):
        new_item = Furniture('code', 'description', 'm_price', 'r_price',
                             'material', 'size')
        self.assertEqual('description', new_item.description)
        self.assertEqual('code', new_item.product_code)
        self.assertEqual('m_price', new_item.market_price)
        self.assertEqual('r_price', new_item.rental_price)
        self.assertEqual('material', new_item.material)
        self.assertEqual('size', new_item.size)


class InventoryTests(TestCase):
    def test_inventory(self):
        new_item = Inventory('code', 'description', 'm_price', 'r_price')
        self.assertEqual('description', new_item.description)
        self.assertEqual('code', new_item.product_code)
        self.assertEqual('m_price', new_item.market_price)
        self.assertEqual('r_price', new_item.rental_price)


class ElectricApplicancesTests(TestCase):
    def test_electricappliances(self):
        new_item = ElectricAppliances('code', 'description', 'm_price',
                                      'r_price', 'brand', 'voltage')
        self.assertEqual('description', new_item.description)
        self.assertEqual('code', new_item.product_code)
        self.assertEqual('m_price', new_item.market_price)
        self.assertEqual('r_price', new_item.rental_price)
        self.assertEqual('brand', new_item.brand)
        self.assertEqual('voltage', new_item.voltage)


class PriceTests(TestCase):
    def test_getprice(self):
        self.get_price = MagicMock(return_value=24)
        self.get_price(1)
        self.get_price.assert_called_with(1)


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

    def test_get_price(self):
        self.assertEqual(24, get_price(1))

    def test_exit(self):
        self.assertRaises(SystemExit)

    def test_add_new_item(self):
        with patch('builtins.input', side_effect=['100', 'description',
                                                  'rentalprice', 'y',
                                                  'material', 'size']):
            add_new_item()
            test_return = {'1': {'product_code': '1', 'description': '2',
                                 'market_price': 24, 'rental_price': '3',
                                 'material': 'l', 'size': 'l'}}
