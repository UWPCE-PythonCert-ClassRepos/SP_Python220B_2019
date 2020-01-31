#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import patch

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.market_prices as market_prices
import inventory_management.main as main


class ElectricTests(TestCase):
    def test_init(self):
        product = ElectricAppliances(product_code="ABC",
                                     description="Meh",
                                     market_price=9.99,
                                     rental_price=0.99,
                                     brand="VGood",
                                     voltage="220")
        self.assertEqual("ABC", product.product_code)
        self.assertEqual("Meh", product.description)
        self.assertEqual(9.99, product.market_price)
        self.assertEqual(0.99, product.rental_price)
        self.assertEqual("VGood", product.brand)
        self.assertEqual("220", product.voltage)

    def test_return_as_dictionary(self):
        product = ElectricAppliances(product_code="ABC",
                                     description="Meh",
                                     market_price=9.99,
                                     rental_price=0.99,
                                     brand="VGood",
                                     voltage="220")
        output_dict = dict()
        output_dict["productCode"] = "ABC"
        output_dict["description"] = "Meh"
        output_dict["marketPrice"] = 9.99
        output_dict["rentalPrice"] = 0.99
        output_dict["brand"] = "VGood"
        output_dict["voltage"] = "220"

        self.assertDictEqual(output_dict, product.return_as_dictionary())


class FurnitureTests(TestCase):
    def test_init(self):
        product = Furniture(product_code="BigOlCouch",
                            description="Big, old.",
                            market_price=999.99,
                            rental_price=99.99,
                            material="wood",
                            size="XXL")
        self.assertEqual("BigOlCouch", product.product_code)
        self.assertEqual("Big, old.", product.description)
        self.assertEqual(999.99, product.market_price)
        self.assertEqual(99.99, product.rental_price)
        self.assertEqual("wood", product.material)
        self.assertEqual("XXL", product.size)

    def test_return_as_dictionary(self):
        product = Furniture(product_code="BigOlCouch",
                            description="Big, old.",
                            market_price=999.99,
                            rental_price=99.99,
                            material="wood",
                            size="XXL")
        output_dict = dict()
        output_dict["productCode"] = "BigOlCouch"
        output_dict["description"] = "Big, old."
        output_dict["marketPrice"] = 999.99
        output_dict["rentalPrice"] = 99.99
        output_dict["material"] = "wood"
        output_dict["size"] = "XXL"

        self.assertDictEqual(output_dict, product.return_as_dictionary())


class InventoryTests(TestCase):
    def test_init(self):
        product = Inventory(product_code="BigOlCouch",
                            description="Big, old.",
                            market_price=999.99,
                            rental_price=99.99)

        self.assertEqual("BigOlCouch", product.product_code)
        self.assertEqual("Big, old.", product.description)
        self.assertEqual(999.99, product.market_price)
        self.assertEqual(99.99, product.rental_price)

    def test_return_as_dictionary(self):
        product = Inventory(product_code="BigOlCouch",
                            description="Big, old.",
                            market_price=999.99,
                            rental_price=99.99)

        output_dict = dict()
        output_dict["productCode"] = "BigOlCouch"
        output_dict["description"] = "Big, old."
        output_dict["marketPrice"] = 999.99
        output_dict["rentalPrice"] = 99.99

        self.assertDictEqual(output_dict, product.return_as_dictionary())


class MarketPricesTests(TestCase):
    def test_get_latest_price(self):
        for x in range(5):
            self.assertEqual(24, market_prices.get_latest_price())


class MainTests(TestCase):
    def test_main_menu1(self):
        with patch('builtins.input', side_effect="1"):
            self.assertEqual(main.main_menu().__name__, "add_new_item")
        with patch('builtins.input', side_effect="2"):
            self.assertEqual(main.main_menu().__name__, "item_info")
        with patch('builtins.input', side_effect="q"):
            self.assertEqual(main.main_menu().__name__, "exit_program")

    def test_get_price(self):
        self.assertEqual(24, main.get_price())

    def test_add_new_item(self):
        main.FULL_INVENTORY = {}
        furniture = ["BigOlCouch", "Big, old.", 99.99, "n", "n"]
        test = {"BigOlCouch": {"productCode": "BigOlCouch", "description": "Big, old.",
                "marketPrice": 24, "rentalPrice": 99.99}}
        with patch("builtins.input", side_effect=furniture):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, test)

    def test_add_new_furniture(self):
        main.FULL_INVENTORY = {}
        furniture = ["BigOlCouch", "Big, old.", 99.99, "y", "Wood", "XXL"]
        test = {"BigOlCouch": {"productCode": "BigOlCouch", "description": "Big, old.",
                               "marketPrice": 24, "rentalPrice": 99.99,
                               "material": "Wood", "size": "XXL"}}
        with patch("builtins.input", side_effect=furniture):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, test)

    def test_add_new_electric_appliance(self):
        main.FULL_INVENTORY = {}
        appliance = [666, "Toaster", 23, "n", "y", "Apple", 220]
        test = {666: {"productCode": 666, "description": "Toaster",
                      "marketPrice": 24, "rentalPrice": 23,
                      "brand": "Apple", "voltage": 220}}
        with patch("builtins.input", side_effect=appliance):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, test)

    def test_item_info(self):
        test_dict = {'productCode': "BigOlCouch", 'description': "Big, old.", 'marketPrice': 24,
                     'rentalPrice': 99.99}
        expected = "productCode: BigOlCouch\ndescription: Big, old.\nmarketPrice: 24\nrentalPrice: 99.99\n"
        with patch('builtins.input', side_effect='1'):
            main.FULL_INVENTORY['1'] = test_dict
            self.assertEqual(print(expected), main.item_info())

        test = "Item not found in inventory"
        with patch('builtins.input', side_effect='1'):
            main.FULL_INVENTORY = {}
            self.assertEqual(print(test), main.item_info())

    def test_exit(self):
        with self.assertRaises(SystemExit):
            main.exit_program()
