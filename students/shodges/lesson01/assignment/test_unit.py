import unittest

from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
#from inventory_management.furniture_class import Furniture
#from inventory_management.market_prices import get_latest_price

class InventoryTest(unittest.TestCase):
    """Test cases for Inventory class"""
    def test_inventory_class(self):
        """Test the inventory instantiation and return_as_dictionary() method"""
        expected = {'productCode': 'DRYWALL',
                    'description': 'Just an ordinary drywall board.  Pretty boring.',
                    'marketPrice': '100.00',
                    'rentalPrice': '8.00'}

        self.item = Inventory('DRYWALL', 'Just an ordinary drywall board.  Pretty boring.',
                              '100.00', '8.00')

        self.assertIsInstance(self.item, Inventory)

        self.assertEqual(expected, self.item.return_as_dictionary())

class ElectricApplianceTest(unittest.TestCase):
    """Test cases for ElectricAppliances class"""
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
