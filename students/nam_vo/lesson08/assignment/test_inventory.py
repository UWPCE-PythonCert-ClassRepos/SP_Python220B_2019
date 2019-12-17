"""Unit tests for closure/curry capability"""

# pylint: disable=line-too-long

from unittest import TestCase
from inventory import add_furniture, single_customer

class InventoryTest(TestCase):
    """Test inventory.py module"""

    def test_add_furniture(self):
        """Test add_furniture()"""
        self.assertEqual('done', add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25))
        self.assertEqual('done', add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10))
        self.assertEqual('done', add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17))

    def test_single_customer(self):
        """Test single_customer()"""
        create_invoice = single_customer("Susan Wong", "rented_items.csv")
        self.assertEqual('done', create_invoice("test_items.csv"))
