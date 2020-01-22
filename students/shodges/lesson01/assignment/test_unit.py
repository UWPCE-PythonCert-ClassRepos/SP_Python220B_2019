import unittest

from inventory_management.inventory_class import Inventory
#from inventory_management.electric_appliances_class import ElectricAppliances
#from inventory_management.furniture_class import Furniture
#from inventory_management.market_prices import get_latest_price

class InventoryTest(unittest.TestCase):
    """Test cases for Inventory class"""
    def test_inventory_init(self):
        """Test the inventory instantiation and return_as_dictionary() method"""
        expected = {'productCode': 'DRYWALL',
                    'description': 'Just an ordinary drywall board.  Pretty boring.',
                    'marketPrice': '100.00',
                    'rentalPrice': '8.00'}

        self.item = Inventory('DRYWALL', 'Just an ordinary drywall board.  Pretty boring.',
                              '100.00', '8.00')

        self.assertIsInstance(self.item, Inventory)

        return_result = self.item.return_as_dictionary

        self.assertEqual(expected, self.item.return_as_dictionary())
