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

    def test_mainMenu(self):
        main.input = MagicMock(return_value='1')
        expected_response = main.addNewItem
        self.assertEqual(main.mainMenu(), expected_response)

    def test_getPrice(self):
        main.getPrice = MagicMock(return_value=main.getPrice(''))
        main.getPrice('abc')
        main.getPrice.assert_called_with('abc')

    def test_get_latest_price(self):
        expected_response = 24
        self.assertEqual(main.market_prices.get_latest_price('code'), expected_response)

    def test_add_furniture(self):
        user_inputs = ['code','description','rental price','y','material','size']
        main.input = MagicMock(side_effect=user_inputs)
        main.fullInventory = MagicMock(return_value='full')
        self.assertEqual(main.addNewItem(), None)

    def test_add_electric_appliance(self):
        user_inputs = ['code','description','rental price','n','y','brand','voltage']
        main.input = MagicMock(side_effect=user_inputs)
        main.fullInventory = MagicMock(return_value='full')
        self.assertEqual(main.addNewItem(), None)

    def test_add_inventory(self):
        user_inputs = ['code','description','rental price','n','n']
        main.input = MagicMock(side_effect=user_inputs)
        main.fullInventory = MagicMock(return_value='full')
        self.assertEqual(main.addNewItem(), None)

    def test_item_found(self):
        main.fullInventory = {1: {'productCode': 'abc'}}
        main.input = MagicMock(return_value=1)
        self.assertEqual(main.itemInfo(), None)

    def test_item_not_found(self):
        main.fullInventory = {1: {'productCode': 'abc'}}
        main.input = MagicMock(return_value=0)
        self.assertEqual(main.itemInfo(), None)

    def test_exitProgram(self):
        main.sys.exit = MagicMock(return_value=0)
        self.assertEqual(main.exitProgram(), None)
