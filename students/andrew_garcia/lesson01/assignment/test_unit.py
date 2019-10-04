from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price
import inventory_management.main as main


class InventoryTest(TestCase):
    def test_unit(self):
        self.item = Inventory(17, 'Microwave', 150, 70)
        self.assertEqual(self.item.product_code, 17)
        self.assertEqual(self.item.description, 'Microwave')
        self.assertEqual(self.item.market_price, 150)
        self.assertEqual(self.item.rental_price, 70)

    def test_return(self):
        """Tests return """
        self.item = Inventory(17, 'Microwave', 150, 70)
        self.assertEqual(self.item.return_as_dictionary(), {'product_code': 17, 'description': 'Microwave',
                                                            'market_price': 150, 'rental_price': 70})


class ElectricAppliancesTest(TestCase):
    def test_init(self):
        self.appliance = ElectricAppliances(42, 'Lamp', 200, 75, 'LightsPlus', 550)
        self.assertEqual(self.appliance.product_code, 42)
        self.assertEqual(self.appliance.brand, 'LightsPlus')

    def test_return(self):
        self.appliance = ElectricAppliances(42, 'Lamp', 200, 75, 'LightsPlus', 550)
        self.assertEqual(self.appliance.return_as_dictionary(), {'product_code': 42, 'description': 'Lamp',
                                                                 'market_price': 200, 'rental_price': 75,
                                                                 'brand': 'LightsPlus', 'voltage': 550})


class FurnitureTest(TestCase):
    def test_init(self):
        self.furniture = Furniture(25, 'Black Couch', 750, 650, 'Leather', 'Small')
        self.assertEqual(self.furniture.size, 'Small')
        self.assertEqual(self.furniture.market_price, 750)

    def test_return(self):
        self.furniture = Furniture(25, 'Black Couch', 750, 650, 'Leather', 'Small')
        self.assertEqual(self.furniture.return_as_dictionary(), {'product_code': 25, 'description': 'Black Couch',
                                                                 'market_price': 750, 'rental_price': 650,
                                                                 'material': 'Leather', 'size': 'Small'})


class MarketPricesTest(TestCase):
    def test_price(self):
        self.price = get_latest_price(17)
        self.assertEqual(self.price, 24)
