import unittest
from electricAppliancesClass import ElectricAppliances
from furnitureClass import Furniture
from inventoryClass import inventory
import market_prices
import main


class TestInventoryClass(unittest.TestCase):
    """Unit tests for inventory class, which contains one function to store product information."""

    def test_inventory(self):
        """"Test to confirm proper storage of product info."""


class TestFurnitureClass(unittest.Testcase):
    """Unit tests for Furniture Class, which includes additional "size" and "material" features."""

    def test_furniture(self):
        """Test to confirm proper storage of all usual product info and additional furniture info."""



class TestElectricAppliancesClass(unittest.Testcase):
    """Unit tests for Electric Appliances Class, which includes additional "brand" and "voltage" features."""

    def test_electric_apps(self):
        """Test to confirm proper storage of all usual product info and additional furniture info."""



class TestMarketPrices(unittest.Testcase):
    """Unit test for market prices call function."""

    def test_market_prices(self):
        """Tests proper return of market prices. Current functionality returns 24 for all calls."""




class TestMainControlFlow(unittest.Testcase):
    """Unit tests for control flow of the inventory system."""

    def test





