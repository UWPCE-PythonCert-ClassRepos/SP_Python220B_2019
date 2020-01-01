"""Module for unit tests for inventory management"""

# pylint: disable=wrong-import-position

import unittest
from unittest import TestCase
from unittest.mock import patch

# import sys
# sys.path.append('./inventory_management')
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price
import inventory_management.main as Main


class InventoryTest(TestCase):
    """Unit tests for Inventory module"""

    def setUp(self):
        """Sets up item"""
        self.item = Inventory(100, "Fridge", 2500, 650)

    def test_init(self):
        """Test initializes and attributes for Inventory"""
        self.assertEqual(self.item.product_code, 100)
        self.assertEqual(self.item.description, "Fridge")
        self.assertEqual(self.item.market_price, 2500)
        self.assertEqual(self.item.rental_price, 650)

    def test_dict(self):
        """Test dictionary for Inventory"""
        inv_dict = Inventory(100, "Fridge", 2500, 650).return_as_dictionary()
        self.assertEqual(inv_dict,
                         {"product_code": 100, "description": "Fridge",
                          "market_price": 2500, "rental_price": 650})


class FurnitureTest(TestCase):
    """Unit tests for Inventory module"""

    def setUp(self):
        """Sets up product"""
        self.product = Furniture(200, "Chair", 150, 50, "Wood", "Small")

    def test_init(self):
        """Test initializes and attributes for Furniture"""
        self.assertEqual(self.product.product_code, 200)
        self.assertEqual(self.product.description, "Chair")
        self.assertEqual(self.product.market_price, 150)
        self.assertEqual(self.product.rental_price, 50)
        self.assertEqual(self.product.material, "Wood")
        self.assertEqual(self.product.size, "Small")

    def test_return(self):
        """Test dictionary for Furniture"""
        pro_dict = Furniture(200, "Chair", 150, 50, "Wood",
                             "Small").return_as_dictionary()
        self.assertEqual(pro_dict,
                         {"product_code": 200, "description": "Chair",
                          "market_price": 150, "rental_price": 50,
                          "material": "Wood", "size": "Small"})


class ElectricAppliancesTest(TestCase):
    """Unit tests for Inventory module"""

    def setUp(self):
        """Sets up appliance"""
        self.appliance = ElectricAppliances(300, "TV", 4000, 250, "Sony", 450)

    def test_init(self):
        """Test initializes and attributes for Electric Appliances"""
        self.assertEqual(self.appliance.product_code, 300)
        self.assertEqual(self.appliance.description, "TV")
        self.assertEqual(self.appliance.market_price, 4000)
        self.assertEqual(self.appliance.rental_price, 250)
        self.assertEqual(self.appliance.brand, "Sony")
        self.assertEqual(self.appliance.voltage, 450)

    def test_return(self):
        """Test dictionary for Electric Appliances"""
        app_dict = ElectricAppliances(300, "TV", 4000, 250, "Sony",
                                      450).return_as_dictionary()
        self.assertEqual(app_dict,
                         {"product_code": 300, "description": "TV",
                          "market_price": 4000, "rental_price": 250,
                          "brand": "Sony", "voltage": 450})


class MarketPricesTest(TestCase):
    """Unit tests for Market Prices module"""

    def test_mark_price(self):
        """Test price"""
        self.assertEqual(get_latest_price(24), 24)


class MainTest(TestCase):
    """Unit tests for Main module"""

    def test_main(self):
        """Test main menu options"""
        with patch("builtins.input", side_effect="1"):
            self.assertEqual(Main.main_menu().__name__, "add_new_item")
        with patch("builtins.input", side_effect="2"):
            self.assertEqual(Main.main_menu().__name__, "item_info")
        with patch("builtins.input", side_effect="q"):
            self.assertEqual(Main.main_menu().__name__, "exit_program")

    def test_exit(self):
        """Test exit"""
        with self.assertRaises(SystemExit):
            Main.exit_program()

    def test_add_new_item(self):
        """Test add new item"""
        Main.FULL_INVENTORY = {}
        new_item = [400, "Couch", 25, "n", "n"]
        inventory = {400: {"product_code": 400, "description": "Couch",
                           "market_price": 24, "rental_price": 25}}
        with patch("builtins.input", side_effect=new_item):
            Main.add_new_item()
        self.assertEqual(Main.FULL_INVENTORY, inventory)

    def test_add_new_furniture(self):
        """Test add new furniture"""
        Main.FULL_INVENTORY = {}
        new_furniture = [500, "Table", 245, "y", "Metal", "Large"]
        inventory = {500: {"product_code": 500, "description": "Table",
                           "market_price": 24, "rental_price": 245,
                           "material": "Metal", "size": "Large"}}
        with patch("builtins.input", side_effect=new_furniture):
            Main.add_new_item()
        self.assertEqual(Main.FULL_INVENTORY, inventory)

    def test_add_new_electric_appliance(self):
        """Test add new electric appliance"""
        Main.FULL_INVENTORY = {}
        new_appliance = [600, "Washer", 50, "n", "y", "LG", 220]
        inventory = {600: {"product_code": 600, "description": "Washer",
                           "market_price": 24, "rental_price": 50,
                           "brand": "LG", "voltage": 220}}
        with patch("builtins.input", side_effect=new_appliance):
            Main.add_new_item()
        self.assertEqual(Main.FULL_INVENTORY, inventory)

    def test_item_info(self):
        """Test item information"""
        Main.FULL_INVENTORY = {3: {"product_code": 3, "description": "PS4",
                                   "market_price": 399, "rental_price": 98}}
        item_info = {3: {"product_code": 3, "description": "PS4",
                         "market_price": 399, "rental_price": 98}}
        with patch("builtins.input", side_effect="3"):
            self.assertEqual(Main.item_info(), print(item_info))


if __name__ == "__main__":
    unittest.main()
