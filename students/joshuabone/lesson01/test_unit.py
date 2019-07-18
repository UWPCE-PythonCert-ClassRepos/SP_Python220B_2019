"""Unit Tests for Inventory Management"""
import unittest
from unittest.mock import patch
import sys
import io

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.main import MainMenu
import inventory_management.market_prices as market_price


class ElectricalApplianceTests(unittest.TestCase):
    """Unit Tests for Electrical Appliance"""

    def test_electric_appliance_todict(self):
        """Test that ElectricalAppliance returns as dictionary"""
        fields = ("productCode", "description", "marketPrice", "rentalPrice",
                  "brand", "voltage")
        app = ElectricAppliances(*fields)
        expected = {f: f for f in fields}
        self.assertEqual(app.return_as_dictionary(), expected)


class FurnitureTests(unittest.TestCase):
    """Unit Tests for Furniture"""

    def test_furniture_todict(self):
        """Test that Furniture returns as dictionary"""
        fields = ("productCode", "description", "marketPrice", "rentalPrice",
                  "material", "size")
        app = Furniture(*fields)
        expected = {f: f for f in fields}
        self.assertEqual(app.return_as_dictionary(), expected)


class InventoryTests(unittest.TestCase):
    """Unit Tests for Inventory"""

    def test_inventory_todict(self):
        """Test that Inventory returns as dictionary"""
        fields = ("productCode", "description", "marketPrice", "rentalPrice")
        app = Inventory(*fields)
        expected = {f: f for f in fields}
        self.assertEqual(app.return_as_dictionary(), expected)


class MarketPriceTests(unittest.TestCase):
    """Unit Tests for Market Price"""

    def test_get_latest_price_returns_magic_number(self):
        """Test that get_latest_price returns a magic number"""
        price = market_price.get_latest_price("any string")
        self.assertEqual(price, 24)


class MainTests(unittest.TestCase):
    """Unit Tests for Main class"""
    MOCK_PRICE = 25

    def test_get_price(self):
        """Test get_price()"""
        output, result = capture_output(MainMenu.get_price)
        self.assertEqual(output, "Get price\n")
        self.assertIsNone(result)

    @patch("sys.stdin", io.StringIO("item_1"))
    def test_item_info_found(self):
        """Test item_info() when input exists in inventory"""
        inventory = {"item_1": {"k1": "v1", "k2": "v2"}}
        menu = MainMenu(inventory)
        output, result = capture_output(menu.item_info)
        self.assertEqual(output, "Enter item code: k1:v1\nk2:v2\n")
        self.assertIsNone(result)

    @patch("sys.stdin", io.StringIO("item_2"))
    def test_item_info_not_found(self):
        """Test item_info() when input does not exist in inventory"""
        inventory = {"item_1": {"k1": "v1", "k2": "v2"}}
        menu = MainMenu(inventory)
        output, result = capture_output(menu.item_info)
        self.assertEqual(output,
                         "Enter item code: Item not found in inventory\n")
        self.assertIsNone(result)

    @patch("inventory_management.market_prices.get_latest_price",
           lambda c: MainTests.MOCK_PRICE)
    @patch("sys.stdin",
           io.StringIO("item-code\nitem-desc\nrental-price\ny\nmaterial\nL"))
    def test_add_new_item_furniture(self):
        """Test can add new Furniture"""
        menu = MainMenu()
        capture_output(menu.add_new_item)
        expected = Furniture("item-code", "item-desc", MainTests.MOCK_PRICE,
                             "rental-price", "material",
                             "L").return_as_dictionary()
        self.assertEqual(menu.inventory, {"item-code": expected})

    @patch("inventory_management.market_prices.get_latest_price",
           lambda c: MainTests.MOCK_PRICE)
    @patch("sys.stdin",
           io.StringIO("item-code\nitem-desc\n"
                       "rental-price\nn\ny\nbrand\nvolt"))
    def test_add_new_item_electrical(self):
        """Test can add new ElectricalAppliances"""
        menu = MainMenu()
        capture_output(menu.add_new_item)
        expected = ElectricAppliances("item-code", "item-desc",
                                      MainTests.MOCK_PRICE,
                                      "rental-price", "brand",
                                      "volt").return_as_dictionary()
        self.assertEqual(menu.inventory, {"item-code": expected})

    @patch("inventory_management.market_prices.get_latest_price",
           lambda c: MainTests.MOCK_PRICE)
    @patch("sys.stdin",
           io.StringIO("item-code\nitem-desc\nrental-price\nn\nn"))
    def test_add_new_item_inventory(self):
        """Test that we can add new Inventory"""
        menu = MainMenu()
        capture_output(menu.add_new_item)
        expected = Inventory("item-code", "item-desc", MainTests.MOCK_PRICE,
                             "rental-price").return_as_dictionary()
        self.assertEqual(menu.inventory, {"item-code": expected})

    @patch("sys.stdin", io.StringIO("q"))
    def test_main_menu(self):
        """Test that the main menu works as expected."""
        menu = MainMenu()
        output, result = capture_output(menu.main_menu)
        self.assertEqual(output, (
            "Please choose from the following options (1, 2, q):\n" +
            "1. Add a new item to the inventory\n" +
            "2. Get item information\n" +
            "q. Quit\n" +
            ">"))
        self.assertEqual(result, menu.exit_program)

    @patch("sys.stdin", io.StringIO("\n"))
    @patch("inventory_management.main.MainMenu.main_menu")
    def test_do_menu(self, mock_main_menu):
        """Test that the do_menu logic prints as expected."""
        menu = MainMenu()
        mock_main_menu.return_value = lambda: None
        output, result = capture_output(lambda: menu.do_menu(False))
        self.assertEqual(output, "{}\n"
                                 "Press Enter to continue...........")
        self.assertIsNone(result)


def capture_output(test_code):
    """Helper method to capture results of console output"""
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    return_value = test_code()
    captured_output = captured.getvalue()
    captured.close()
    sys.stdout = old_stdout
    return captured_output, return_value
