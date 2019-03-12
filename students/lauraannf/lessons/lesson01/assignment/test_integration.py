# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 12:49:08 2019

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


class ModuleTests(TestCase):

    def test_module(self):
        furniture_test = Furniture('100', 'description', 'marketprice',
                                   'rentalprice', 'material', 'size')
        electric_test = ElectricAppliances('200', 'description', 'marketprice',
                                           'rentalprice', 'brand', 'voltage')
        inventory_test = Inventory('300', 'description', 'marketprice',
                                   'rentalprice')
        furniture_test_2 = furniture_test.return_as_dictionary()
        electric_test_2 = electric_test.return_as_dictionary()
        inventory_test_2 = inventory_test.return_as_dictionary()
        self.assertEqual(furniture_test_2, {'product_code': '100',
                                            'description': 'description',
                                            'market_price': 'marketprice',
                                            'rental_price': 'rentalprice',
                                            'material': 'material',
                                            'size': 'size'})
        self.assertEqual(electric_test_2, {'product_code': '200',
                                           'description': 'description',
                                           'market_price': 'marketprice',
                                           'rental_price': 'rentalprice',
                                           'brand': 'brand',
                                           'voltage': 'voltage'})
        self.assertEqual(inventory_test_2, {'product_code': '300',
                                            'description': 'description',
                                            'market_price': 'marketprice',
                                            'rental_price': 'rentalprice'})
        main_test = main_menu('1')
        main_test()