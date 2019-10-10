from unittest.mock import MagicMock
from unittest import TestCase

from inventory_management.inventoryClass import inventory
from inventory_management.electricAppliancesClass import electricAppliances
from inventory_management.furnitureClass import furniture
from inventory_management import market_prices
from inventory_management import main

class InventoryTests(TestCase):

    def test_inventory(self):
        obj = inventory('abc', 'this is a test inventory', 1000, 1200)
        output = {
            'productCode': 'abc',
            'description': 'this is a test inventory',
            'marketPrice': 1000,
            'rentalPrice': 1200,
        }
        self.assertEqual(output, obj.returnAsDictionary())

class ElectricAppliancesTests(TestCase):

    def test_electric_appliances(self):
        obj = electricAppliances('abc', 'this is a test inventory', 1000, 1200, 'python', 110)
        output = {
            'productCode': 'abc',
            'description': 'this is a test inventory',
            'marketPrice': 1000,
            'rentalPrice': 1200,
            'brand': 'python',
            'voltage': 110,
        }
        self.assertEqual(output, obj.returnAsDictionary())

class FurnitureTests(TestCase):

    def test_furniture(self):
        obj = furniture('abc', 'this is a test inventory', 1000, 1200, 'plastic', '12x12')
        output = {
            'productCode': 'abc',
            'description': 'this is a test inventory',
            'marketPrice': 1000,
            'rentalPrice': 1200,
            'material': 'plastic',
            'size': '12x12',
        }
        self.assertEqual(output, obj.returnAsDictionary())

class MainTests(TestCase):

    def test_get_latest_price(self):
        market_prices.get_latest_price = MagicMock(return_value=market_prices.get_latest_price(''))
        market_prices.get_latest_price('abc')
        market_prices.get_latest_price.assert_called_with('abc')

    def test_mainMenu(self):
        main.mainMenu = MagicMock(return_value=0)
        main.mainMenu()
        main.mainMenu.assert_called_with()

    def test_getPrice(self):
        main.getPrice = MagicMock(return_value=main.getPrice(''))
        main.getPrice('abc')
        main.getPrice.assert_called_with('abc')

    def test_addNewItem(self):
        main.addNewItem = MagicMock(return_value=0)
        main.addNewItem()
        main.addNewItem.assert_called_with()

    def test_itemInfo(self):
        main.itemInfo = MagicMock(return_value=0)
        main.itemInfo()
        main.itemInfo.assert_called_with()

    def test_exitProgram(self):
        main.exitProgram = MagicMock(return_value=0)
        main.exitProgram()
        main.exitProgram.assert_called_with()
