#/usr/bin/python3

from unittest import TestCase
from unittest.mock import Mock, patch
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management import main
from inventory_management.market_prices import get_latest_price
class InventoryTest(TestCase):

    def setUp(self):
        self.inventory_1 = Inventory('1234', 'lamp', '45', '10')
        self.inventory_1_dic = self.inventory_1.return_as_dictionary()
        self.electric_appliances_1 =ElectricAppliances('4455', 'TV', '2200', '140','Samsung', '120')
        self.electric_appliances_1_dic = self.electric_appliances_1.return_as_dictionary()
        self.furniture_1 = Furniture('2020', 'sofa', '1200', '100', 'leather', '22x33x44')
        self.furniture_1_dic = self.furniture_1.return_as_dictionary()

    def test_inventory(self):
        self.assertEqual(self.inventory_1_dic['product_code'],'1234')
        self.assertEqual(self.inventory_1_dic['description'], 'lamp')
        self.assertEqual(self.inventory_1_dic['market_price'], '45')
        self.assertEqual(self.inventory_1_dic['rental_price'], '10')

    def test_electric_appliances(self):
        self.assertEqual(self.electric_appliances_1_dic['product_code'],'4455')
        self.assertEqual(self.electric_appliances_1_dic['description'], 'TV')
        self.assertEqual(self.electric_appliances_1_dic['market_price'], '2200')
        self.assertEqual(self.electric_appliances_1_dic['rental_price'], '140')
        self.assertEqual(self.electric_appliances_1_dic['brand'], 'Samsung')
        self.assertEqual(self.electric_appliances_1_dic['voltage'], '120')

    def test_furniture(self):
        self.assertEqual(self.furniture_1_dic['product_code'],'2020')
        self.assertEqual(self.furniture_1_dic['description'], 'sofa')
        self.assertEqual(self.furniture_1_dic['market_price'], '1200')
        self.assertEqual(self.furniture_1_dic['rental_price'], '100')
        self.assertEqual(self.furniture_1_dic['material'], 'leather')
        self.assertEqual(self.furniture_1_dic['size'], '22x33x44')



class MainModuleTest_addnew_item(TestCase):

    def test_addnew_furniture(self):
        input_furniture = ('444', 'bed', 150, 'y', 'wood', 'L')
        input_app = ('555', 'laptop', 50, 'n', 'y', 'samsung', 120)
        input_inventory = ('666', 'test', 5, 'n', 'n')
        expected_item_dic = {'444': {'description': 'bed',
                                     'market_price': 180.0,
                                     'product_code': '444',
                                     'rental_price': 150,
                                     'material': 'wood',
                                     'size': 'L'},
                             '555': {'description': 'laptop',
                                     'market_price': 120.0,
                                     'product_code': '555',
                                     'rental_price': 50,
                                     'brand': 'samsung',
                                     'voltage': 120},
                             '666': {'description': 'test',
                                     'market_price': 10.0,
                                     'product_code': '666',
                                     'rental_price': 5
                                                    }}


        with patch('builtins.input', side_effect=input_furniture):
            main.FULL_INVENTORY = {}
            with patch('inventory_management.market_prices.get_latest_price', return_value=180.0):

                main.addnew_item()
                self.assertDictEqual(main.FULL_INVENTORY['444'], expected_item_dic['444'] )

        with patch('builtins.input', side_effect=input_app):
            main.FULL_INVENTORY = {}
            with patch('inventory_management.market_prices.get_latest_price', return_value=120.0):

                main.addnew_item()
                self.assertDictEqual(main.FULL_INVENTORY['555'], expected_item_dic['555'] )

        with patch('builtins.input', side_effect = input_inventory):
            with patch('inventory_management.market_prices.get_latest_price', return_value=10.0):

                main.addnew_item()
                self.assertEqual(main.FULL_INVENTORY['666'], expected_item_dic['666'])


    def test_exit(self):
        with self.assertRaises(SystemExit):
            main.exit_program()

    def test_item_info(self):

        with patch ('builtins.input', side_effect = '444'):
            main.FULL_INVENTORY={}
            self.assertEqual(main.item_info(),  print("Item not found in inventory"))

        with patch ('builtins.input', side_effect = '444'):
            main.FULL_INVENTORY = {'444': {'description': 'bed',
                                     'market_price': 180.0,
                                     'product_code': '444',
                                     'rental_price': 150,
                                     'material': 'wood',
                                     'size': 'L'}}

            expected = {'description': 'bed',
                                     'market_price': 180.0,
                                     'product_code': '444',
                                     'rental_price': 150,
                                     'material': 'wood',
                                     'size': 'L'}

            self.assertEqual(main.item_info(), print(expected))
            self.assertEqual(main.FULL_INVENTORY['444'], expected)



        with patch('builtins.input', side_effect='111'):
            self.assertEqual(main.item_info(), print("Item not found in inventory"))

class MarketPrice(TestCase):

    def test_market_price(self):
        self.assertEqual(get_latest_price('444'), 24)


class GetPrice(TestCase):

    def test_main_get_price(self):
        self.assertEqual(main.get_price('444'), print("Get price") )

class MainMenu(TestCase):

    def test_main_menu(self):
        with patch('builtins.input', side_effect = '1'):
            self.assertEqual(main.main_menu().__name__, 'addnew_item')

    def test_main_menu(self):
        with patch('builtins.input', side_effect = '2'):
            self.assertEqual(main.main_menu().__name__, 'item_info')

    def test_main_menu(self):
        with patch('builtins.input', side_effect = 'q'):
            self.assertEqual(main.main_menu().__name__, 'exit_program')