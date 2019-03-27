"""Unit Tests for Inventory Management"""
import unittest
from unittest.mock import patch
import sys
import io

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.main as main
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
        price = market_price.get_latest_price("zzxyx")
        self.assertEqual(price, 24)


class MainTests(unittest.TestCase):
    """Unit Tests for Main class"""

    def test_get_price(self):
        """Test get_price()"""
        result = capture_output(main.get_price)
        self.assertEqual(result, "Get price\n")

    @patch("sys.stdin", io.StringIO("item_1"))
    def test_item_info_found(self):
        """Test item_info() when input exists in inventory"""
        inventory = {"item_1": {"k1": "v1", "k2": "v2"}}
        result = capture_output(lambda: main.item_info(inventory))
        self.assertEqual(result, "Enter item code: k1:v1\nk2:v2\n")

    @patch("sys.stdin", io.StringIO("item_2"))
    def test_item_info_not_found(self):
        """Test item_info() when input does not exist in inventory"""
        inventory = {"item_1": {"k1": "v1", "k2": "v2"}}
        result = capture_output(lambda: main.item_info(inventory))
        self.assertEqual(result,
                         "Enter item code: Item not found in inventory\n")


def capture_output(test_code):
    """Helper method to capture results of console output"""
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    test_code()
    return_val = captured.getvalue()
    captured.close()
    sys.stdout = old_stdout
    return return_val
