# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 17:56:48 2019

@author: Humberto
"""

from unittest import TestCase
from unittest.mock import patch
import inventory_management.main as main
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.inventory_class import Inventory
import inventory_management.market_prices as market_prices

class InventoryTests(TestCase):
    """Tests the functions within the inventory system"""
    def test_is_inventory(self):
        """tests to make sure inventory objects are created"""
        nintendo64 = Inventory('N64', 'Nintendo 64', 200, 75)
        self.assertIsInstance(nintendo64, Inventory)

    def test_inventory(self):
        """tests the adding inventory item functionality"""
        nintendo64 = Inventory('N64', 'Nintendo 64', 200, 75)
        compare = {'productCode':'N64',
                   'description':'Nintendo 64',
                   'marketPrice':200,
                   'rentalPrice':75}
        self.assertDictEqual(nintendo64.return_as_dictionary(), compare)

class ElectricAppliancesTests(TestCase):
    """Tests Electric Appliances functionality"""
    def test_is_electrical_appliance(self):
        """tests to make sure electric applaince objects are created"""
        blender = ElectricAppliances('B33', 'Nutri-Bullet Blender', 100,
                                     25, 'Nutri-Bullet', 12)
        self.assertIsInstance(blender, ElectricAppliances)

    def test_electrical_appliance(self):
        """tests the adding electric appliance item functionality"""
        blender = ElectricAppliances('B33', 'Nutri-Bullet Blender', 24, 25,
                                     'Nutri-Bullet', 12)
        compare = {'productCode':'B33',
                   'description':'Nutri-Bullet Blender',
                   'marketPrice':24,
                   'rentalPrice':25,
                   'brand':'Nutri-Bullet',
                   'voltage':12}
        self.assertDictEqual(blender.return_as_dictionary(), compare)

class FurnitureTests(TestCase):
    """Tests Furniture functionality"""
    def test_is_furniture(self):
        """tests to make sure furniture item objects are created"""
        couch = Furniture('C74', 'IKEA Malmer Couch', 24, 125,
                          'Leather', 'L')
        self.assertIsInstance(couch, Furniture)

    def test_furniture(self):
        """tests the furniture item functionality"""
        couch = Furniture('C74', 'IKEA Malmer Couch', 24, 125,
                          'Leather', 'L')
        compare = {'productCode':'C74',
                   'description':'IKEA Malmer Couch',
                   'marketPrice':24,
                   'rentalPrice':125,
                   'material':'Leather',
                   'size':'L'}
        self.assertDictEqual(couch.return_as_dictionary(), compare)

class MarketPriceTests(TestCase):
    """Tests the Market Prices functionality"""
    def test_get_latest_price(self):
        """tests the get latest price functionality"""
        true_price = market_prices.get_latest_price('N64')
        compare = 24
        self.assertEqual(true_price, compare)

class MainTests(TestCase):
    """Tests the Main function"""
    def test_main_menu(self):
        """tests the main menu functionality"""
        with patch('builtins.input', side_effect='1'):
            function = main.main_menu()
        self.assertEqual(function.__name__, 'add_new_item')
        with patch('builtins.input', side_effect='2'):
            function = main.main_menu()
        self.assertEqual(function.__name__, 'item_info') 
        with patch('builtins.input', side_effect='q'):
            function = main.main_menu()
        self.assertEqual(function.__name__, 'exit_program')

    def test_get_price(self):
        """tests the get price function"""
        true_price = main.get_price('N64')
        compare = 24
        self.assertEqual(true_price, compare)

    def test_add_new_item_furniture(self):
        """tests the add new furniture funtion"""
        main.FULL_INVENTORY = {}
        item_inputs = ['C74', 'IKEA Malmer Couch', 650, 'y', 'Leather', 'L']
        compare = {'productCode':'C74',
                   'description':'IKEA Malmer Couch',
                   'marketPrice':24,
                   'rentalPrice':650,
                   'material':'Leather',
                   'size':'L'}

        with patch('builtins.input', side_effect=item_inputs):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY['C74'], compare)

    def test_add_new_item_electronic_appliance(self):
        """tests the add new electric appliance function"""
        main.FULL_INVENTORY = {}
        item_inputs = ['B33', 'Nutri-Bullet Blender', 100, 'n', 'y',
                       'Nutri-Bullet', 12]
        compare = {'productCode':'B33',
                   'description':'Nutri-Bullet Blender',
                   'marketPrice':24,
                   'rentalPrice':100,
                   'brand':'Nutri-Bullet',
                   'voltage':12}

        with patch('builtins.input', side_effect=item_inputs):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY['B33'], compare)
