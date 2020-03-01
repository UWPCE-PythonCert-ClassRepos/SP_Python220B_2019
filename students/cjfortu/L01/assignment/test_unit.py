#!/usr/bin/env python
"""
Unit test module.

Tests classes and functions independent of other methods or functions.
"""

from unittest import TestCase
from unittest.mock import patch, Mock
from io import StringIO
import os
import sys

os.chdir('inventory_management/')
sys.path.append(os.getcwd())

from inventory_class import Inventory
from furniture_class import Furniture
from electric_appliances_class import ElectricAppliances
import market_prices as mkt_prc
from market_prices import get_latest_price as glp
from main import *

INV_CDE = '123456'
INV_DSC = 'thing'
INV_MKT_PRC = '300'
INV_RNT_PRC = '30'
FUR_CDE = '456789'
FUR_DSC = 'couch'
FUR_MKT_PRC = '200'
FUR_RNT_PRC = '20'
FUR_MAT = 'leather'
FUR_SZ = 'L'
EA_CDE = '789123'
EA_DSC = 'tv'
EA_MKT_PRC = '100'
EA_RNT_PRC = '10'
EA_BRD = 'Samsung'
EA_VLT = '110'


class InventoryTests(TestCase):

    def test_inventory(self):
        """Test that the inventory class returns the correct dict."""
        inv = Inventory(INV_CDE, INV_DSC, INV_MKT_PRC, INV_RNT_PRC)
        self.assertEqual({'product_code': INV_CDE, 'description': INV_DSC,
                         'market_price': INV_MKT_PRC, 'rental_price': INV_RNT_PRC},
                         inv.return_as_data_struct())


class FurnitureTests(TestCase):

    def test_furniture(self):
        """Test that the furniture class returns the correct dict."""
        fur = Furniture(FUR_CDE, FUR_DSC, FUR_MKT_PRC, FUR_RNT_PRC, FUR_MAT, FUR_SZ)
        self.assertEqual({'product_code': FUR_CDE, 'description': FUR_DSC,
                         'market_price': FUR_MKT_PRC, 'rental_price': FUR_RNT_PRC,
                         'material': FUR_MAT, 'size': FUR_SZ}, fur.return_as_data_struct())


class ElectricAppliancesTests(TestCase):

    def test_electtric_appliances(self):
        """Test that the electric appliances class returns the correct dict."""
        ea = ElectricAppliances(EA_CDE, EA_DSC, EA_MKT_PRC, EA_RNT_PRC, EA_BRD, EA_VLT)
        self.assertEqual({'product_code': EA_CDE, 'description': EA_DSC,
                         'market_price': EA_MKT_PRC, 'rental_price': EA_RNT_PRC,
                         'brand': EA_BRD, 'voltage': EA_VLT}, ea.return_as_data_struct())


class MainTests(TestCase):

    def setUp(self):
        self.get_latest_price = mkt_prc.get_latest_price
        self.FULL_INVENTORY = FULL_INVENTORY

    def tearDown(self):
        mkt_prc.get_latest_price = self.get_latest_price
        FULL_INVENTORY = self.FULL_INVENTORY

    def test_main_menu(self):
        """Test the main menu responses."""
        with patch('builtins.input', return_value='1'):
            self.assertEqual(add_new_item, main_menu())
        with patch('builtins.input', return_value='2'):
            self.assertEqual(item_info, main_menu())
        with patch('builtins.input', return_value='q'):
            self.assertEqual(exit_program, main_menu())

    def test_add_new_item(self):
        """Test that new items are properly categorized and constructed, ...
        ...with market prices and FULL_INVENTORY mocked."""
        mkt_prc.get_latest_price = Mock(return_value=543)
        FULL_INVENTORY = Mock(return_value='dummy')
        with patch('builtins.input', side_effect=[FUR_CDE, FUR_DSC, FUR_RNT_PRC, 'Y', FUR_MAT,
                   FUR_SZ]):
            self.assertEqual(Furniture(FUR_CDE, FUR_DSC, 543, FUR_RNT_PRC, FUR_MAT, FUR_SZ),
                             add_new_item())
        with patch('builtins.input', side_effect=[EA_CDE, EA_DSC, EA_RNT_PRC, 'N', 'Y', EA_BRD,
                   EA_VLT]):
            self.assertEqual(ElectricAppliances(EA_CDE, EA_DSC, 543, EA_RNT_PRC, EA_BRD, EA_VLT),
                             add_new_item())
        with patch('builtins.input', side_effect=[INV_CDE, INV_DSC, INV_RNT_PRC, 'N', 'N']):
            self.assertEqual(Inventory(INV_CDE, INV_DSC, 543, INV_RNT_PRC),
                             add_new_item())

    @patch('sys.stdout', new_callable=StringIO)
    def test_item_info_not_found(self, mock_stdout):
        """Test that nonexistent item codes give the proper response."""
        with patch('builtins.input', return_value='1234'):
            item_info()
            self.assertEqual(mock_stdout.getvalue(), 'Item not found in inventory\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_item_info_found(self, mock_stdout):
        """Test that existing item codes yield the correct data."""
        with patch('builtins.input', return_value=EA_CDE), patch('main.FULL_INVENTORY',
             {EA_CDE: {'product_code': EA_CDE, 'description': EA_DSC, 'market_price': EA_MKT_PRC,
             'rental_price': EA_RNT_PRC, 'brand': EA_BRD, 'voltage': EA_VLT}}):
            item_info()
            self.assertEqual(mock_stdout.getvalue(), """product_code:789123
description:tv
market_price:100
rental_price:10
brand:Samsung
voltage:110\n""")

    def test_market_prices(self):
        """Test that market prices work as written."""
        self.assertEqual(24, mkt_prc.get_latest_price(None))
