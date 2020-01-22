import unittest

from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.market_prices import get_latest_price

class InventoryTest(unittest.TestCase):
    """Test cases for inventory_class module"""
    def test_inventory_class(self):
        """Test the Inventory instantiation and return_as_dictionary() method"""
        expected = {'productCode': 'DRYWALL',
                    'description': 'Just an ordinary drywall board.  Pretty boring.',
                    'marketPrice': '100.00',
                    'rentalPrice': '8.00'}

        self.item = Inventory('DRYWALL', 'Just an ordinary drywall board.  Pretty boring.',
                              '100.00', '8.00')

        self.assertIsInstance(self.item, Inventory)

        self.assertEqual(expected, self.item.return_as_dictionary())

class ElectricApplianceTest(unittest.TestCase):
    """Test cases for electric_appliances_class module"""
    def test_electric_appliances_class(self):
        """Test the ElectricAppliances instantiation and return_as_directory() method"""
        expected = {'productCode': 'OVEN',
                    'description': 'A great double oven',
                    'marketPrice': '599.99',
                    'rentalPrice': '40.00',
                    'brand': 'GT',
                    'voltage': '240V'}


        item_attributes = {'productCode': 'OVEN',
                           'description': 'A great double oven',
                           'market_price': '599.99',
                           'rental_price': '40.00',
                           'brand': 'GT',
                           'voltage': '240V'}

        self.item = ElectricAppliances(**item_attributes)

        self.assertIsInstance(self.item, Inventory, ElectricAppliances)

        self.assertEqual(expected, self.item.return_as_dictionary())

class FurnitureTest(unittest.TestCase):
    """Test cases for furniture_class module"""
    def test_electric_appliances_class(self):
        """Test the ElectricAppliances instantiation and return_as_directory() method"""
        expected = {'productCode': 'SECTIONAL',
                    'description': 'A pleather sectional sofa',
                    'marketPrice': '1045.87',
                    'rentalPrice': '102.77',
                    'material': 'Pleather',
                    'size': 'XL'}


        item_attributes = {'productCode': 'SECTIONAL',
                           'description': 'A pleather sectional sofa',
                           'market_price': '1045.87',
                           'rental_price': '102.77',
                           'material': 'Pleather',
                           'size': 'XL'}

        self.item = Furniture(**item_attributes)

        self.assertIsInstance(self.item, Inventory, Furniture)

        self.assertEqual(expected, self.item.return_as_dictionary())

class MarketPricesTest(unittest.TestCase):
    """Test cases for market_prices module"""
    def test_market_prices(self):
        """Test the get_latest_price() method"""
        self.assertEqual(24, get_latest_price('SECTIONAL'))
