from unittest import TestCase
from unittest.mock import patch

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.main as main
from inventory_management.market_prices import get_latest_price


class MainTests(TestCase):

    def test_main_menu(self):
        with patch ('builtins.input', side_effect ='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)
        with patch ('builtins.input', side_effect ='2'):
            self.assertEqual(main.main_menu(), main.item_info)
        with patch ('builtins.input', side_effect ='q'):
            self.assertEqual(main.main_menu(), main.exit_program)


    def test_get_price(self):
        self.assertEqual(24, main.get_price())


    def test_add_new_item(self):
        electric_appliance = [1, "item", 5, "n", "y", "brand", 5.5]
        furniture = [1, "item", 5, "y", "material", "XL"]
        inventory = [1, "item", 5, "n", "n"]

        with patch('builtins.input', side_effect=electric_appliance):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            test_dict = {1: {'product_code': 1, 'description': "item", 'market_price': 24,
                'rental_price': 5, 'brand': "brand", 'voltage': 5.5}}
            self.assertEqual(main.FULL_INVENTORY, test_dict)

        with patch('builtins.input', side_effect=furniture):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            test_dict = {1: {'product_code': 1, 'description': "item", 'market_price': 24,
                'rental_price': 5, 'material': "material", 'size': "XL"}}
            self.assertEqual(main.FULL_INVENTORY, test_dict)

        with patch('builtins.input', side_effect=inventory):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            test_dict = {1: {'product_code': 1, 'description': "item", 'market_price': 24,
                'rental_price': 5}}
            self.assertEqual(main.FULL_INVENTORY, test_dict)


    def test_item_info(self):
        expected = "Item not found in inventory"
        with patch('builtins.input', side_effect = '1'):
            main.FULL_INVENTORY = {}
            self.assertEqual(print(expected), main.item_info())

        test_dict = {'product_code': 1, 'description': "item", 'market_price': 5,
            'rental_price': 5, 'brand': "brand", 'voltage': 5.5}
        expected = "product_code: 1\ndescription: item\nmarket_price: 5\nrental_price: 5\nbrand: brand\nvoltage: 5.5\n"
        with patch('builtins.input', side_effect = '1'):
            main.FULL_INVENTORY['1'] = test_dict
            self.assertEqual(print(expected), main.item_info())


    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            main.exit_program()


class ElectricAppliancesTests(TestCase):

    def test_return_as_dict(self):
        electric_appliance = ElectricAppliances(1, "item", 5, 5, "brand", 5.5)
        test_dict = {'product_code': 1, 'description': "item", 'market_price': 5,
            'rental_price': 5, 'brand': "brand", 'voltage': 5.5}

        self.assertEqual(test_dict, electric_appliance.return_as_dictionary())


class FurnitureTests(TestCase):

    def test_return_as_dict(self):
        furniture = Furniture(1, "item", 5, 5, "material", "XL")
        test_dict = {'product_code': 1, 'description': "item", 'market_price': 5,
            'rental_price': 5, 'material': "material", 'size': "XL"}

        self.assertEqual(test_dict, furniture.return_as_dictionary())


class InventoryTests(TestCase):

    def test_return_as_dict(self):
        inventory = Inventory(1, "item", 5, 5)
        test_dict = {'product_code': 1, 'description': "item", 'market_price': 5, 'rental_price': 5}

        self.assertEqual(test_dict, inventory.return_as_dictionary())


class MarketPriceTests(TestCase):

    def test_get_latest_price(self):
        self.assertEqual(24, get_latest_price())


