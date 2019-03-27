"""Unit Tests for Inventory Management"""
import unittest

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
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
