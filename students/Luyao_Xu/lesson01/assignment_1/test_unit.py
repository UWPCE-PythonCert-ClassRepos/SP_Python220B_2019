#!/usr/bin/env python3
from unittest import TestCase
from unittest.mock import MagicMock
from inventory_management.electric_appliances_class import *
from inventory_management.furniture_class import *
from inventory_management.inventory_class import *
from inventory_management.market_prices import *
from inventory_management.main import *


class ElectricAppliancesTests(TestCase):
    """Test electric appliances class"""

    def setUp(self):
        self.test_ea = ElectricAppliances('100', 'Mobile Phone', '10000',
                                     '100',
                                     'Apple',
                                     '110')

    def test_dict(self):
        actual = self.test_ea.return_as_dictionary()
        expected = {'product_code': '100',
                    'description': 'Mobile Phone',
                    'market_price': '10000',
                    'rental_price': '100',
                    'brand': 'Apple',
                    'voltage': '110'}

        self.assertDictEqual(actual, expected)

    def test_brand(self):
        expected = 'Apple'
        self.assertEqual(self.test_ea.brand, expected)

    def test_voltage(self):
        expected = '110'
        self.assertEqual(self.test_ea.voltage, expected)

    def test_fields(self):
        d = self.test_ea.return_as_dictionary()
        self.assertEqual(d['product_code'], '100')
        self.assertEqual(d['description'], 'Mobile Phone')
        self.assertEqual(d['market_price'], '10000')
        self.assertEqual(d['rental_price'], '100')
        self.assertEqual(d['brand'], 'Apple')
        self.assertEqual(d['voltage'], '110')


class FurnitureTest(TestCase):
    """Test furniture class"""
    def setUp(self):
        self.test_fur = Furniture(
            '100', 'Table', '10000', '100', 'Wood', 'S')

    def test_dict(self):
        actual = self.test_fur.return_as_dictionary()
        expected = {'product_code': '100',
                    'description': 'Table',
                    'market_price': '10000',
                    'rental_price': '100',
                    'material': 'Wood',
                    'size': 'S'}

        self.assertEqual(actual, expected)


class MarketPriceTest(TestCase):
    """Test market price Class"""

    def test_market_price(self):
        actual = 24
        expected = get_latest_price()
        self.assertEqual(actual, expected)

    def test_mock_price(self):
        self.mock = MagicMock(return_value=11)
        expected = 11
        actual = self.mock.return_value
        self.assertEqual(expected, actual)


class InventoryClassTest(TestCase):
    def setUp(self):
        self.test_inv = Inventory('1', 'lamp', '100', '10')

    def test_inventory(self):
        actual = self.test_inv.return_as_dictionary()
        expected = {'product_code': '1',
                    'description': 'lamp',
                    'market_price': '100',
                    'rental_price': '10'}
        self.assertDictEqual(actual, expected)


class MainTest(TestCase):
    def setUp(self):
        self.add_new_item = main_menu('1')
        self.item_info = main_menu('2')
        self.exit_program = main_menu('q')


    def test_add_new_item(self):
        self.add_new_item = MagicMock(return_value=Furniture(
            '100', 'Table', '10000', '100', 'Wood', 'S'))

        actual = self.add_new_item()
        expected = Furniture(
            '100', 'Table', '10000', '100', 'Wood', 'S')

        self.assertDictEqual(actual.return_as_dictionary(),
                             expected.return_as_dictionary())

        self.add_new_item = MagicMock(return_value=ElectricAppliances(
            '100', 'Mobile Phone','10000','100', 'Apple', '110'))

        actual = self.add_new_item()
        expected = ElectricAppliances('100', 'Mobile Phone','10000',
                                      '100', 'Apple', '110')
        self.assertDictEqual(actual.return_as_dictionary(),
                             expected.return_as_dictionary())


    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            exit_program()
