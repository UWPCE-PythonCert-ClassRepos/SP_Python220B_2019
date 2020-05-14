#!/usr/bin/env python3


import sys
from unittest import TestCase
from unittest.mock import patch
sys.path.append('./inventory_management')
import market_prices as mp
import inventory_class as inv
import electric_appliances_class as ea
import furniture_class as fc
import main

# cd C:\Users\v-ollock\github\SP_Python220B_2019\students\ScotchWSplenda\lesson01\assignment
'''
python -m pylint ./inventory_management
python -m coverage run --source=inventory_management -m unittest test_unit.py
python -m coverage report
'''


class market_prices_test(TestCase):
    """for market_prices module."""
    def setUp(self):
        """set up instance for Market Price tests."""
        print('setUp')
        self.item_code = 12345

    def test_get_latest_price(self):
        """Test get_latest_price module"""
        print('test_get_latest_price')
        actual_price = mp.get_latest_price(12345)
        assert actual_price == 24


class inventory_class_test(TestCase):
    """FOR inventory_class module."""
    def test_inventory(self):
        test_inv = inv.Inventory(12345,
                                 "First Product",
                                 420,
                                 69)
        test_inv_dict = test_inv.return_as_dictionary()
        self.assertDictEqual(test_inv_dict, {'item_code': 12345,
                                             'description': "First Product",
                                             'market_price': 420,
                                             'rental_price': 69})


class electric_appliances_class_test(TestCase):
    """for electric_appliances_class module."""
    def setUp(self):
        item_code = 69420
        description = "foot masseuse"
        market_price = 69
        rental_price = 420
        brand = "Costco"
        voltage = 220
        self.test_app_item = ea.ElectricAppliances(item_code,
                                                   description,
                                                   market_price,
                                                   rental_price,
                                                   brand,
                                                   voltage)
        self.test_app_dict = self.test_app_item.return_as_dictionary()

    def test_app_creation(self):
        """Test creation of electrical appliance item."""
        comp_dict = {'item_code': 69420,
                     'description': "foot masseuse",
                     'market_price': 69,
                     'rental_price': 420,
                     'brand': "Costco",
                     'voltage': 220}
        self.assertDictEqual(self.test_app_dict, comp_dict)


class furniture_class_test(TestCase):
    """for furniture_class module."""
    def setUp(self):
        item_code = 69420
        description = "bench"
        market_price = 69
        rental_price = 420
        material = "wood"
        size = 220
        self.test_app_item = fc.Furniture(item_code,
                                          description,
                                          market_price,
                                          rental_price,
                                          material,
                                          size)
        self.test_app_dict = self.test_app_item.return_as_dictionary()

    def test_furn_creation(self):
        """Test creation of electrical appliance item."""
        comp_dict = {'item_code': 69420,
                     'description': "bench",
                     'market_price': 69,
                     'rental_price': 420,
                     'material': "wood",
                     'size': 220}
        self.assertDictEqual(self.test_app_dict, comp_dict)


class main_test(TestCase):
    '''testing adding different types of items'''
    def test_addfurn(self):
        input_furniture = ('123', 'bench', 150, 'y', 'wood', 'L')
        expected_item_dic = {'123': {'description': 'bench',
                                     'market_price': 24,
                                     'item_code': '123',
                                     'rental_price': 150,
                                     'material': 'wood',
                                     'size': 'L'}}
        with patch('builtins.input', side_effect=input_furniture):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            self.assertDictEqual(main.FULL_INVENTORY['123'], expected_item_dic['123'])

    def test_addapp(self):
        input_app = ('456', 'foot masseuse', 50, 'n', 'y', 'Costco', 120)
        expected_item_dic = {'456': {'description': 'foot masseuse',
                                     'market_price': 24,
                                     'item_code': '456',
                                     'rental_price': 50,
                                     'brand': 'Costco',
                                     'voltage': 120}}
        with patch('builtins.input', side_effect=input_app):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            self.assertDictEqual(main.FULL_INVENTORY['456'], expected_item_dic['456'])

    def test_addinv(self):
        input_inventory = ('789', 'test', 5, 'n', 'n')
        expected_item_dic = {'789': {'description': 'test',
                                     'market_price': 24,
                                     'item_code': '789',
                                     'rental_price': 5}}
        with patch('builtins.input', side_effect=input_inventory):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            self.assertDictEqual(main.FULL_INVENTORY['789'], expected_item_dic['789'])

    def test_is_no_record(self):
        with patch('builtins.input', side_effect=['69']):
            main.FULL_INVENTORY = {}
            self.assertEqual(main.item_info(), print("Item not found in inventory"))

    def test_is_a_record(self):
        with patch('builtins.input', side_effect=['789']):
            main.FULL_INVENTORY = {'789': {'description':'test',
                                   'market_price':24,
                                   'item_code':'789',
                                   'rental_price':5}}
            self.assertEqual(main.item_info(),
            print('description:test\n'
                  'market_price:24\n'
                  'item_code:789\n'
                  'rental_price:5'))


    def test_exit(self):
        with self.assertRaises(SystemExit):
            main.exit_program()

    def test_main_menu(self):
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)
