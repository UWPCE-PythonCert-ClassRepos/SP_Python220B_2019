"""Module for unit tests for inventory management"""


import io
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

import inventory_management.main as Main
import inventory_management.market_prices as MarketPrices
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture

class MarketPriceTests(TestCase):
    """Unit tests for MarketPrices module"""
    
    
class InventoryTests(TestCase):
    """Unit tests for Inventory module"""
    
    
class Furniture(TestCase):
    """Unit tests for Furniture module"""
    
    def setUp(self):
        """Sets up"""
        self.furniture = Furniture(123, "Bed", 500, 20, "Cotton", "Small")

class ElectricAppliances(TestCase):
    """Unit tests for ElectricAppliances module"""
    
    
    
class MainTests(TestCase):
    """Unit tests for Main module"""
    