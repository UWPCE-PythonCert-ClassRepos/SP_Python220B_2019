# test_unit.py
"""Create unit tests for inventory management classes."""
import unittest

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture


class InventoryTest(unittest.TestCase):
    """Inventory class tests."""

    def test_init(self):
        # test inventory item initializes and correct sets initial attributes/properties
        inven = Inventory(1025, "test item", 80.00, 10.00)
        self.assertEqual(inven.product_code, 1025)
        self.assertEqual(inven.description, "test item")
        self.assertEqual(inven.market_price, 80.00)
        self.assertEqual(inven._rental_price, 10.00)

    def test_dict_return(self):
        # test that a dictionary of the item is returned and the fields are correct
        inven = Inventory(1025, "test item", 80.00, 10.00)
        inven_dict = inven.return_as_dictionary()

        self.assertIsInstance(inven_dict, dict, "testing output is of type dictionary")
        self.assertEqual(inven_dict["product_code"], 1025)
        self.assertEqual(inven_dict["description"], "test item")
        self.assertEqual(inven_dict["market_price"], 80.00)
        self.assertEqual(inven_dict["rental_price"], 10.00)


class FurnitureTest(unittest.TestCase):
    """Contains all the tests for the Furniture Class."""

    def test_init(self):
        self.assert_(False)

    def test_return_as_dict(self):
        self.assert_(False)