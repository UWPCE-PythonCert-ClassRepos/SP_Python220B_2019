"""use unit test to test the scripts in inventory management file"""

import unittest
import sys
from inventory_management.main import main_menu
import inventory_management
from unittest.mock import patch


class ElectricApplicancesClassTest(unittest.TestCase):
    def test_electric_appliances(self):
        electric_test = inventory_management.electric_appliances_class. \
            ElectricAppliances('6980', 'description', 'marketprice', 'rentalprice', 'brand', 'voltage')
        electric_test_2 = electric_test.return_as_dictionary()

        self.assertEqual(electric_test_2, {'productCode': '6980',
                                           'description': 'description',
                                           'marketPrice': 'marketprice',
                                           'rentalPrice': 'rentalprice',
                                           'brand': 'brand',
                                           'voltage': 'voltage'})


class FurnitureTests(unittest.TestCase):
    def test_furniture(self):
        furniture_test = inventory_management. \
            furniture_class.Furniture('999', 'description', 'marketprice',
                                      'rentalprice', 'material', 'size')
        furniture_test_2 = furniture_test.return_as_dictionary()
        self.assertEqual(furniture_test_2, {'productCode': '999',
                                            'description': 'description',
                                            'marketPrice': 'marketprice',
                                            'rentalPrice': 'rentalprice',
                                            'material': 'material',
                                            'size': 'size'})


class Invetory(unittest.TestCase):
    def test_inventory(self):
        inventory_class = inventory_management.inventory_class. \
            Inventory('156', 'description', 'marketprice',
                      'rentalprice')
        inventory_test = inventory_class.return_as_dictionary()
        self.assertEqual(inventory_test, {'productCode': '156',
                                          'description': 'description',
                                          'marketPrice': 'marketprice',
                                          'rentalPrice': 'rentalprice'})


class MarketPriceTests(unittest.TestCase):
    def test_get_latest_price(self):
        market_price = inventory_management.market_prices. \
            get_latest_price('200')
        self.assertEqual(24, market_price)


class MainTests(unittest.TestCase):

    def test_exit(self):
        with self.assertRaises(SystemExit):
            inventory_management.main.exit_program()

    def test_add_new_furniture(self):
        furniture = ['780', 'table', '300', 'y', 'wood', 'L']
        with patch('builtins.input', side_effect=furniture):
            output = inventory_management.main.add_new_item()
        self.assertEqual(inventory_management.main.inventory_specs()['780'], {'productCode': '780',
                                                                              'description': 'table',
                                                                              'marketPrice': 24,
                                                                              'rentalPrice': '300',
                                                                              'material': 'wood',
                                                                              'size': 'L'})

    def test_add_new_electric(self):
        electric_appliance = ['800', 'computer', '500', 'n', 'y', 'Dell', '50']
        with patch('builtins.input', side_effect=electric_appliance):
            inventory_management.main.add_new_item()
        print('hey')
        print(inventory_management.main.FULL_INVENTORY)
        print('hey')
        self.assertEqual(inventory_management.main.inventory_specs()['800'], {'productCode': '800',
                                                                              'description': 'computer',
                                                                              'marketPrice': 24,
                                                                              'rentalPrice': '500',
                                                                              'brand': 'Dell',
                                                                              'voltage': '50'})

    def test_add_new_item(self):
        item = ['1000', 'pencil', '500', 'n', 'n']
        with patch('builtins.input', side_effect=item):
            inventory_management.main.add_new_item()
        print('hey')
        print(inventory_management.main.FULL_INVENTORY)
        print('hey')
        self.assertEqual(inventory_management.main.inventory_specs()['1000'], {'productCode': '1000',
                                                                               'description': 'pencil',
                                                                               'marketPrice': 24,
                                                                               'rentalPrice': '500'})

    def test_main_menu_1(self):
        with patch('builtins.input', side_effect=['1']):
            output = inventory_management.main.main_menu()

        self.assertEqual(output.__name__, 'add_new_item')

    def test_main_menu_2(self):
        with patch('builtins.input', side_effect=['2']):
            output = inventory_management.main.main_menu()

        self.assertEqual(output.__name__, 'item_info')

    def test_get_price(self):
        self.assertEqual(inventory_management.main.get_price(6980), 24)

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            inventory_management.main.exit_program()

    def test_item_info(self):
        with patch('builtins.input', side_effect=['1']):
            output = inventory_management.main.item_info()
        self.assertEqual(None, output)

        furniture = ['780', 'table', '300', 'y', 'wood', 'L']
        with patch('builtins.input', side_effect=furniture):
            inventory_management.main.add_new_item()

        with patch('builtins.input', side_effect=['780']):
            output = inventory_management.main.item_info()
        print('hey')
        print(output)
        print('hey')
        # self.assertEqual(output,)

    def test_inventory_specs(self):
        furniture2 = ['999', 'table', '300', 'y', 'wood', 'L']
        with patch('builtins.input', side_effect=furniture2):
            inventory_management.main.add_new_item()
        self.assertEqual(inventory_management.main.inventory_specs()['999'], {'productCode': '999',
                                                                              'description': 'table',
                                                                              'marketPrice': 24,
                                                                              'rentalPrice': '300',
                                                                              'material': 'wood',
                                                                              'size': 'L'})
