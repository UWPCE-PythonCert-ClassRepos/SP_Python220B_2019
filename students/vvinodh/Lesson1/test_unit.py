"""Test File for testing inventory management files"""

from unittest import TestCase

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture


class InventoryTest(TestCase):
    """Tests Inventory Class"""
    def test_inventory(self):
        """Tests the creation of an instance for inventory object"""
        test_dict = {'product_code': 6789, 'description': 'Cars',
                     'market_price': 50, 'rental_price': 10}
        test_inv = Inventory(6789, 'Cars', 50, 10)
        self.assertEqual(test_dict, test_inv.return_as_dictionary())

class FurnitureTest(TestCase):
    """Tests Furniture Class"""
    def test_furniture(self):
        """Tests the creation of an instance for furniture object"""
        test_dict = {'product_code': 6789, 'description': 'Horse',
                     'market_price': 50, 'rental_price': 10,
                     'material': 'Leather', 'size': 'Large'}
        test_furn = Furniture(6789, 'Car', 50, 10, 'Leather', 'Large')
        self.assertEqual(test_dict, test_furn.return_as_dictionary())
