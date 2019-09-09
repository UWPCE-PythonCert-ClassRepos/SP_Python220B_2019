#!/usr/bin/python
from unittest.mock import patch
from unittest import TestCase
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.main import *

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

class MainModuleTest(TestCase):
    """This class includes methods to test main.py module"""

    def test_main_menu(self):
        print("\n")
        with patch('builtins.input', return_value = '1' ):
            print ("Calling main_menu() with 1")
            self.assertEqual(main_menu(), addnew_item)
        with patch('builtins.input', return_value = '2'):
            self.assertEqual(main_menu(), item_info)
        with patch('builtins.input', return_value = 'q'):
            self.assertEqual(main_menu(), exit_program)


class TestItemInfo(TestCase):
    """This class test item_info function in main.py module"""

    def setUp(self):
        self.inventory_1 = Inventory('1234', 'lamp', '45', '10')
        self.electric_appliances = ElectricAppliances('4455', 'TV', '2200', '140', 'Samsung', '120')
        self.furniture_1 = Furniture('2020', 'sofa', '1200', '100', 'leather', '22x33x44')
        FULL_INVENTORY[item_code] = self.inventory_1.return_as_dictionary()
        FULL_INVENTORY[item_code] = self.electric_appliances.return_as_dictionary()
        FULL_INVENTORY[item_code] = self.furniture_1.return_as_dictionary()

    # def test_item_info(self):
    #     with path('builtins', return_value = '1234')
    #         self.assertDictEqual()


        # def item_info():
        #     """Item Info"""
        #     item_code = input("Enter item code: ")
        #     if item_code in FULL_INVENTORY:
        #         print_dict = FULL_INVENTORY[item_code]
        #         for key, value in print_dict.items():
        #             print("{}:{}".format(key, value))
