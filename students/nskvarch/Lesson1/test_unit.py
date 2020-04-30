#!usr/bin/env python3
# Unit test script for the HP Norton Furniture exercise created by Niels Skvarch

import unittest
from unittest.mock import MagicMock, patch
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price
from inventory_management import main


class TestCaseOne(unittest.TestCase):
    """Test the initialization of an Inventory object"""
    def test_inventory(self):
        inv_obj = Inventory("1234", "inventory item", "1", "2")
        inv_obj_dict = inv_obj.return_as_dictionary()
        self.assertEqual(inv_obj_dict, {"product_code": "1234", "description": "inventory item",
                                        "market_price": "1", "rental_price": "2"})


class TestCaseTwo(unittest.TestCase):
    """Test the initialization of a Furniture object"""
    def test_furniture(self):
        furn_obj = Furniture("5678", "furniture item", "3", "4", "furniture material", "M")
        furn_obj_dict = furn_obj.return_as_dictionary()
        self.assertEqual(furn_obj_dict, {"product_code": "5678", "description": "furniture item",
                                         "market_price": "3", "rental_price": "4",
                                         "material": "furniture material", "size": "M"})


class TestCaseThree(unittest.TestCase):
    """Test the initialization of a Furniture object"""
    def test_electronics(self):
        elect_obj = ElectricAppliances("9012", "electric appliance item", "5", "6",
                                       "appliance brand", "120")
        elect_obj_dict = elect_obj.return_as_dictionary()
        self.assertEqual(elect_obj_dict, {"product_code": "9012", "description": "electric appliance item",
                                          "market_price": "5", "rental_price": "6",
                                          "brand": "appliance brand", "voltage": "120"})


class TestCaseFour(unittest.TestCase):
    """Test the return of a mocked market value"""
    def test_market_prices(self):
        self.assertEqual(get_latest_price(3456), 24)
        self.get_latest_price = MagicMock(return_value=9)
        assert self.get_latest_price(3456) == 9


class TestCaseFive(unittest.TestCase):
    """Test the main program menu with mocked user input for menu navigation"""
    def test_main_menu(self):
        with patch("builtins.input", side_effect="1"):
            self.assertEqual(main.main_menu().__name__, "add_new_item")
        with patch("builtins.input", side_effect="2"):
            self.assertEqual(main.main_menu().__name__, "item_info")
        with patch("builtins.input", side_effect="q"):
            self.assertEqual(main.main_menu().__name__, "exit_program")


class TestCaseSix(unittest.TestCase):
    """Test the main program get price function"""
    def test_get_price(self):
        self.assertEqual(24, main.get_price("1234"))


class TestCaseSeven(unittest.TestCase):
    """Test the main program add item function and the get item information function"""
    def test_add_item(self):
        add_inv_item = ("1234", "inventory item", "2", "n", "n")
        test_inventory = {"1234": {"product_code": "1234", "description": "inventory item",
                                   "market_price": 24, "rental_price": "2"}}
        with patch("builtins.input", side_effect=add_inv_item):
            main.add_new_item()
            self.assertEqual(test_inventory, main.FULL_INVENTORY)
        add_furn_item = ("5678", "furniture item", "4", "y", "furniture material", "M")
        test_inventory = {"5678": {"product_code": "5678", "description": "furniture item",
                                   "market_price": 24, "rental_price": "4",
                                   "material": "furniture material", "size": "M"},
                          "1234": {"product_code": "1234", "description": "inventory item",
                                   "market_price": 24, "rental_price": "2"}}
        with patch("builtins.input", side_effect=add_furn_item):
            main.add_new_item()
            self.assertEqual(test_inventory, main.FULL_INVENTORY)
        add_elect_item = ("9012", "electric appliance item", "6", "n",
                          "y", "appliance brand", "120")
        test_inventory = {"9012": {"product_code": "9012", "description": "electric appliance item",
                                   "market_price": 24, "rental_price": "6",
                                   "brand": "appliance brand", "voltage": "120"},
                          "5678": {"product_code": "5678", "description": "furniture item",
                                   "market_price": 24, "rental_price": "4",
                                   "material": "furniture material", "size": "M"},
                          "1234": {"product_code": "1234", "description": "inventory item",
                                   "market_price": 24, "rental_price": "2"}}
        with patch("builtins.input", side_effect=add_elect_item):
            main.add_new_item()
            self.assertEqual(test_inventory, main.FULL_INVENTORY)

    def test_item_info(self):
        expected_item = {'description': 'inventory item', 'market_price': 24,
                         'product_code': '1234', 'rental_price': '2'}
        with patch("builtins.input", side_effect=["1234"]):
            self.assertEqual(expected_item, main.item_info())

    def test_item_not_found(self):
        expected_result = None
        with patch("builtins.input", side_effect=["123"]):
            self.assertEqual(expected_result, main.item_info())


class TestCaseEight(unittest.TestCase):
    """Test the clean exit of the main program"""
    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            main.exit_program()


# main program name-space
if __name__ == "__main__":
    unittest.main()
