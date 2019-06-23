#!/usr/bin/env python3
from unittest import TestCase
from unittest.mock import MagicMock, patch
from inventory_management.electric_appliances_class import *
from inventory_management.furniture_class import *
from inventory_management.inventory_class import *
from inventory_management.market_prices import *
from inventory_management.main import *


class ElectricAppliancesTests(TestCase):
    """Test electric appliances class"""

    def setUp(self):
        self.test_ea = ElectricAppliances('1', 'Mobile Phone', 10000, 100,
                                          'Apple', '110')

    def test_dict(self):
        actual = self.test_ea.return_as_dictionary()
        expected = {'product_code': '1',
                    'description': 'Mobile Phone',
                    'market_price': 10000,
                    'rental_price': 100,
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
        self.assertEqual(d['product_code'], '1')
        self.assertEqual(d['description'], 'Mobile Phone')
        self.assertEqual(d['market_price'], 10000)
        self.assertEqual(d['rental_price'], 100)
        self.assertEqual(d['brand'], 'Apple')
        self.assertEqual(d['voltage'], '110')


class FurnitureTest(TestCase):
    """Test furniture class"""
    def setUp(self):
        self.test_fur = Furniture('2', 'Table', 10000, 100, 'Wood', 'S')

    def test_dict(self):
        actual = self.test_fur.return_as_dictionary()
        expected = {'product_code': '2',
                    'description': 'Table',
                    'market_price': 10000,
                    'rental_price': 100,
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
        self.test_inv = Inventory('3', 'lamp', 100, 10)

    def test_inventory(self):
        actual = self.test_inv.return_as_dictionary()
        expected = {'product_code': '3',
                    'description': 'lamp',
                    'market_price': 100,
                    'rental_price': 10}
        self.assertDictEqual(actual, expected)


class MainTest(TestCase):

    def setUp(self):
        self.add_new_item = main_menu('1')
        self.item_info = main_menu('2')
        self.exit_program = main_menu('q')

    def test_valid_input(self):
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main_menu(), add_new_item)
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main_menu(), item_info)
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main_menu(), exit_program)

    def test_add_new_inventory_item(self):
        # Test Inventory
        FULL_INVENTORY.clear()
        mocked_input = '4', 'Book', 5, 'n', 'n'
        expected = {'4': {'product_code': '4',
                          'description': 'Book',
                          'market_price': 24,
                          'rental_price': 5}}
        with patch('builtins.input', side_effect=mocked_input):
            self.add_new_item()
        self.assertEqual(expected, FULL_INVENTORY)

    def test_add_new_furniture(self):
        # Test Furniture
        FULL_INVENTORY.clear()
        mocked_input = '2', 'Table', 100, 'y', 'wood', 'S'
        expected = {'2': {'product_code': '2',
                        'description': 'Table',
                        'market_price': 24,
                        'rental_price': 100,
                        'material': 'wood',
                        'size': 'S'}}
        with patch('builtins.input', side_effect=mocked_input):
            self.add_new_item()
        self.assertEqual(expected, FULL_INVENTORY)

    def test_add_new_electric_appliances(self):
        # Test ElectricAppliances
        FULL_INVENTORY.clear()
        mocked_input = '3', 'Mobile Phone', 100, 'n', 'y', 'Apple', '110'
        expected = {'3': {'product_code': '3',
                          'description': 'Mobile Phone',
                          'market_price': 24,
                          'rental_price': 100,
                          'brand': 'Apple',
                          'voltage': '110'}}
        with patch('builtins.input', side_effect=mocked_input):
            self.add_new_item()
        self.assertEqual(expected, FULL_INVENTORY)

    def test_get_price(self):
        self.get_price = MagicMock(return_value=24)
        self.assertEqual(24, get_price())

    def test_none_item_info(self):
        FULL_INVENTORY.clear()
        test_dict = {'product_code': '1', 'description': 'Table',
                     'market_price': 24, 'rental_price': 100, 'material':
                         'wood', 'size': 'S'}
        FULL_INVENTORY['1'] = test_dict
        with patch('builtins.input', side_effect='22'):
            actual = self.item_info()
            expected = None
            self.assertEqual(actual, expected)

    def test_item_info(self):
        FULL_INVENTORY.clear()
        test_dict = {'product_code': '1', 'description': 'Table',
                     'market_price': 24, 'rental_price': 100, 'material':
                     'wood', 'size': 'S'}
        FULL_INVENTORY['1'] = test_dict
        with patch('builtins.input', side_effect='1'):
            actual = self.item_info()
            expected = {'product_code': '1',
                        'description': 'Table',
                        'market_price': 24,
                        'rental_price': 100,
                        'material': 'wood',
                        'size': 'S'}

            self.assertEqual(actual, expected)

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            exit_program()

#