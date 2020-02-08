from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

from inventory_management.inventory import Inventory
from inventory_management.electric_appliances import ElectricAppliances
from inventory_management.furniture import Furniture
from inventory_management.market_prices import get_latest_price

import inventory_management.main as main
import io


class InventoryTest(TestCase):
    def test_inventory_init(self):
        # Given
        args = {
            "product_code": 42,
            "description": "The test item",
            "market_price": 12.34,
            "rental_price": 5.67,
        }

        # When
        self.inventory = Inventory(**args)

        # Then
        self.assertEqual(42, self.inventory.product_code)
        self.assertEqual("The test item", self.inventory.description)
        self.assertEqual(12.34, self.inventory.market_price)
        self.assertEqual(5.67, self.inventory.rental_price)

    def test_inventory_return_as_dictionary(self):
        # Given
        args = {
            "product_code": 42,
            "description": "The test item",
            "market_price": 12.34,
            "rental_price": 5.67,
        }

        # When
        self.inventory = Inventory(**args)

        # Then
        self.assertEqual(args, self.inventory.return_as_dictionary())


class ElectricAppliancesTest(TestCase):
    def test_electric_appliance_init(self):
        # Given
        args = {
            "product_code": "Test1234",
            "description": "Test Toaster",
            "market_price": 123.45,
            "rental_price": 10.20,
            "brand": "Testola",
            "voltage": 220,
        }
        # When
        self.ea = ElectricAppliances(**args)

        # Then
        self.assertEqual("Testola", self.ea.brand)
        self.assertEqual(220, self.ea.voltage)

    def test_electric_appliance_return_as_dictionary(self):
        # Given
        args = {
            "product_code": "Test1234",
            "description": "Test Toaster",
            "market_price": 123.45,
            "rental_price": 10.20,
            "brand": "Testola",
            "voltage": 220,
        }

        # When
        self.ea = ElectricAppliances(**args)

        # Then
        self.assertEqual(args, self.ea.return_as_dictionary())


class FurnitureTest(TestCase):
    def test_furniture_init(self):
        # Given
        args = {
            "product_code": "Test5678",
            "description": "Test Sofa",
            "market_price": 123.45,
            "rental_price": 10.20,
            "material": "Flubber",
            "size": "Triple Single",
        }

        # When
        self.furniture = Furniture(**args)

        # Then
        self.assertEqual(123.45, self.furniture.market_price)
        self.assertEqual("Flubber", self.furniture.material)
        self.assertEqual("Triple Single", self.furniture.size)

    def test_furniture_return_as_dictionary(self):
        # Given
        args = {
            "product_code": "Test1234",
            "description": "Test Toaster",
            "market_price": 123.45,
            "rental_price": 10.20,
            "brand": "Testola",
            "voltage": 220,
        }

        # When
        self.ea = ElectricAppliances(**args)

        # Then
        self.assertEqual(args, self.ea.return_as_dictionary())


class FurnitureTest(TestCase):
    def test_furniture_init(self):
        # Given
        args = {
            "product_code": "Test5678",
            "description": "Test Sofa",
            "market_price": 123.45,
            "rental_price": 10.20,
            "material": "Flubber",
            "size": "Triple Single",
        }

        # When
        self.furniture = Furniture(**args)

        # Then
        self.assertEqual(args, self.furniture.return_as_dictionary())


class MarketPricesTest(TestCase):
    def test_get_latest_price(self):
        # Given
        item_code = 1234

        # When
        result = get_latest_price(item_code)

        # Then
        self.assertEqual(24, get_latest_price(item_code))


class MainTest(TestCase):
    def test_main_menu_case_1(self):
        # Given
        # When
        # Then
        with patch("builtins.input", side_effect="1"):
            self.assertEqual(main.add_new_item, main.main_menu())

    def test_main_menu_case_2(self):
        # Given
        # When
        # Then
        with patch("builtins.input", side_effect="2"):
            self.assertEqual(main.item_info, main.main_menu())

    def test_main_menu_case_q(self):
        # Given
        # When
        # Then
        with patch("builtins.input", side_effect="q"):
            self.assertEqual(main.exit_program, main.main_menu())

    def test_get_price(self):
        # Given
        expected_value = 24
        item_code = 32

        # When
        result = main.get_price(item_code)

        # Then
        self.assertEqual(expected_value, result)

    def test_add_new_item(self):
        print("add new item")
        # Given
        main.FULL_INVENTORY = {}
        input_inventory_1 = ["209", "vase", 2.99, "y", "ceramic", "S"]
        test_inventory = {
            "209": {
                "product_code": "209",
                "description": "vase",
                "market_price": 24,
                "rental_price": 2.99,
                "material": "ceramic",
                "size": "S",
            }
        }

        # When
        with patch("builtins.input", side_effect=input_inventory_1):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            self.assertEqual(test_inventory["209"], main.FULL_INVENTORY["209"])

        input_inventory_2 = [
            "210",
            "Washing Machine",
            50.00,
            "n",
            "y",
            "Samsung",
            "220",
        ]
        test_inventory["210"] = {
            "product_code": "210",
            "description": "Washing Machine",
            "market_price": 24,
            "rental_price": 50.00,
            "brand": "Samsung",
            "voltage": "220",
        }
        with patch("builtins.input", side_effect=input_inventory_2):
            main.add_new_item()
            self.assertEqual(test_inventory["210"], main.FULL_INVENTORY["210"])

        input_inventory_3 = ["211", "Kazoo", 1.00, "n", "n"]
        test_inventory["211"] = {
            "product_code": "211",
            "description": "Kazoo",
            "market_price": 24,
            "rental_price": 1.00,
        }
        with patch("builtins.input", side_effect=input_inventory_3):
            main.add_new_item()
            self.assertEqual(test_inventory["211"], main.FULL_INVENTORY["211"])

    def test_item_info(self):
        # Given
        main.FULL_INVENTORY = {
            "1": {
                "product_code": "222",
                "description": "waffle iron",
                "market_price": 129.99,
                "rental_price": 19.99,
                "brand": "Waffle-O-Matic",
                "voltage": "110",
            }
        }

        expected_result = """product_code:222
description:waffle iron
market_price:129.99
rental_price:19.99
brand:Waffle-O-Matic
voltage:110
"""

        # When
        with patch("builtins.input", side_effect="1"):
            with patch("sys.stdout", new=io.StringIO()) as actual_result:
                main.item_info()

        # Then
        self.assertEqual(expected_result, actual_result.getvalue())

    def test_item_info_no_item(self):
        # Given
        main.FULL_INVENTORY = {
            "1": {
                "product_code": "222",
                "description": "waffle iron",
                "market_price": 129.99,
                "rental_price": 19.99,
                "brand": "Waffle-O-Matic",
                "voltage": "110",
            }
        }
        # When
        with patch("builtins.input", side_effect="3"):
            with patch("sys.stdout", new=io.StringIO()) as actual_result:
                main.item_info()
        # Then
        self.assertEqual("Item not found in inventory\n", actual_result.getvalue())

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            main.exit_program()
