# -*- coding: utf-8 -*-
"""
Created on Sun Jun 9 11:11:14 2019
@author: Florentin Popescu
"""

#""" use unit test to test the scripts in inventory management file """
#======================================
# imports
import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch
from IPython.utils.capture import capture_output

from inventory_management.inventory import Inventory
from inventory_management.furniture import Furniture
from inventory_management.electric_appliances import Electric
from inventory_management.market_prices import get_latest_price

from inventory_management.main import main_menu
from inventory_management.main import get_price
from inventory_management.main import add_new_item
from inventory_management.main import item_info
from inventory_management.main import exit_program

#======================================
class InventoryTests(TestCase):
    """ test inventory class """
    def test_inventory(self):
        """ assert equal """
        inventory_test = Inventory('111',
                                   'description',
                                   'marketprice',
                                   'rentalprice').return_as_dictionary()
        self.assertEqual(inventory_test,
                         {'product_code': '111',
                          'description': 'description',
                          'market_price': 'marketprice',
                          'rental_price': 'rentalprice'})

#======================================
class FurnitureTests(TestCase):
    """ test furniture class """
    def test_furniture(self):
        """ assert equal """
        furniture_test = Furniture('222', 'description',
                                   'marketprice', 'rentalprice',
                                   'material', 'size').return_as_dictionary()
        self.assertEqual(furniture_test, {'product_code': '222',
                                          'description': 'description',
                                          'market_price': 'marketprice',
                                          'rental_price': 'rentalprice',
                                          'material': 'material',
                                          'size': 'size'})

#======================================
class ElectricTest(TestCase):
    """ test electric appliances class """
    def test_electric(self):
        """ assert equal """
        electric_test = Electric('333', 'description',
                                 'marketprice', 'rentalprice',
                                 'brand', 'voltage').return_as_dictionary()
        self.assertEqual(electric_test, {'product_code': '333',
                                         'description': 'description',
                                         'market_price': 'marketprice',
                                         'rental_price': 'rentalprice',
                                         'brand': 'brand',
                                         'voltage': 'voltage'})

#======================================
class PriceTests(TestCase):
    """ test market prices method """
    def test_get_price(self):
        """ assert equal """
        self.assertEqual(24, get_latest_price('44'))

##======================================
class MainTests(TestCase):
    """ main tests """
    def test_add_new_furniture(self):
        """ assert equal """
        furniture_record = list(Furniture('300',
                                          'chair', '40', 'Y', 'wood',
                                          'L').return_as_dictionary().values())
        with patch('builtins.input', side_effect=furniture_record):
            test_furniture = add_new_item()
        self.assertEqual(test_furniture['300'],
                         {'product_code': '300',
                          'description': 'chair',
                          'market_price': 24,
                          'rental_price': '40',
                          'material': 'wood',
                          'size': 'L'})

    #----------------------------------
    def test_add_new_electric(self):
        """ assert equal """
        electric_record = ['400', 'fridge', '50', 'n', 'y', 'GE', '5']
        with patch('builtins.input', side_effect=electric_record):
            test_electric = add_new_item()
        self.assertEqual(test_electric['400'],
                         {'product_code': '400',
                          'description': 'fridge',
                          'market_price': 24,
                          'rental_price': '50',
                          'brand': 'GE',
                          'voltage': '5'})

    #----------------------------------
    def test_add_new_other_item(self):
        """assert equal """
        other_item_record = ['10', 'book', '5', 'n', 'n']
        with patch('builtins.input', side_effect=other_item_record):
            test_other_item = add_new_item()
        self.assertEqual(test_other_item['10'],
                         {'product_code': '10',
                          'description': 'book',
                          'market_price': 24,
                          'rental_price': '5'})

    #----------------------------------
    def test_main_menu_1(self):
        """ assert equal """
        with patch('builtins.input', side_effect=['1']):
            output = main_menu()
        self.assertEqual(output.__name__, 'add_new_item')

    #----------------------------------
    def test_main_menu_2(self):
        """ assert equal """
        with patch('builtins.input', side_effect=['2']):
            output = main_menu()
        self.assertEqual(output.__name__, 'item_info')

    #----------------------------------
    def test_main_menu_q(self):
        """ assert equal """
        with patch('builtins.input', side_effect=['q']):
            output = main_menu()
        self.assertEqual(output.__name__, 'exit_program')

    #----------------------------------
    def test_get_price(self):
        """ assert equal """
        magic = MagicMock(side_effect=get_price)
        self.assertEqual(magic(7), 24)

    #----------------------------------
    def test_exit(self):
        """ assert raises """
        with self.assertRaises(SystemExit):
            exit_program()

    #----------------------------------
    def test_item_info(self):
        """ asert equal """
        new_furniture = ['1000', 'sofa', '200', 'y', 'wood', 'XL']
        with patch('builtins.input', side_effect=new_furniture):
            add_new_item()
        with patch('builtins.input', side_effect=['1000']):
            with capture_output() as capture:
                item_info()
        self.assertEqual(capture.stdout.splitlines(),
                         ['product_code:1000',
                          'description:sofa',
                          'market_price:24',
                          'rental_price:200',
                          'material:wood',
                          'size:XL'])

        with patch('builtins.input', side_effect=['0']):
            self.assertEqual(None, item_info())

#======================================
if __name__ == "__main__":
    unittest.main()

#============= END ====================
#======================================
