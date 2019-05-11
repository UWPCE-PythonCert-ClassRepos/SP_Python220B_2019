import sys
import unittest
sys.path.append('/Users/guntur/PycharmProjects/uw/p220/SP_Python220B_2019/students/g_rama'
                '/lesson01/inventory_management')
from unittest import TestCase, mock
import pytest
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory


class TestInventory(unittest.TestCase):
    def testInventory(self):
        test_inventory = Inventory(1, "dining_table_description", 400, 50)
        assert test_inventory.product_code == 1
        assert test_inventory.description == "dining_table_description"
        assert test_inventory.market_price == 400
        assert test_inventory.rental_price == 50
        test_actualoutput = test_inventory.return_as_dictionary()
        test_expectedoutput = {'product_code': 1, 'description': "dining_table_description", 'market_price': 400,
                              'rental_price': 50}
        assert test_actualoutput == test_expectedoutput
        self.assertDictEqual(test_actualoutput, test_expectedoutput)


class TestElectricAppliances(unittest.TestCase):
    def testElectricAppliances(self):
        test_electric_app = ElectricAppliances(1, "refregirator_description", 400, 50,
                                               "samsung", "110v")
        assert test_electric_app.product_code == 1
        assert test_electric_app.description == "refregirator_description"
        assert test_electric_app.market_price == 400
        assert test_electric_app.rental_price == 50
        assert test_electric_app.brand == "samsung"
        assert test_electric_app.voltage == "110v"
        test_actualoutput = test_electric_app.return_as_dictionary()
        test_expectedoutput = {'product_code': 1, 'description': "refregirator_description", 'market_price': 400,
                               'rental_price': 50, 'brand': "samsung", 'voltage': "110v"}
        assert test_actualoutput == test_expectedoutput
        self.assertDictEqual(test_actualoutput, test_expectedoutput)


class TestFurniture(unittest.TestCase):
    def testFurniture(self):
        test_furniture = Furniture(1, "dining_table_description", 400, 50, "glass", "L")
        assert test_furniture.product_code == 1
        assert test_furniture.description == "dining_table_description"
        assert test_furniture.market_price == 400
        assert test_furniture.rental_price == 50
        assert test_furniture.material == "glass"
        assert test_furniture.size == "L"
        test_actualoutput = test_furniture.return_as_dictionary()
        test_expectedoutput = {'product_code': 1, 'description': "dining_table_description", 'market_price': 400,
                               'rental_price': 50, 'material': "glass", 'size': "L"}
        assert test_actualoutput == test_expectedoutput
        self.assertDictEqual(test_actualoutput, test_expectedoutput)









