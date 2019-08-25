# test_unit.py
"""Create unit tests for inventory management classes."""
import unittest

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances


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
        """Test we can initialize a piece of Furniture properly."""
        # test chair with no material or size
        chair = Furniture(100, "this is a chair", 150.00, 5.00)
        self.assertEqual(chair.size, "N/A")
        self.assertEqual(chair.material, "N/A")

        # test chair with material and size defined
        chair2 = Furniture(120, "this is chair #2", 180.00, 0.00, material="Leather", size="small")
        self.assertEqual(chair2.size, "small")
        self.assertEqual(chair2.material, "Leather")

    def test_return_as_dict(self):
        """Test dictionary function for extended furniture needs."""
        chair2 = Furniture(120, "this is chair #2", 180.00, 0.00, material="Leather", size="small")
        chair2_dict = chair2.return_as_dictionary()

        self.assertIsInstance(chair2_dict, dict)
        self.assertEqual(chair2_dict["size"], "small")
        self.assertEqual(chair2_dict["material"], "Leather")


class ElectricAppliancesTest(unittest.TestCase):
    """ElectricAppliances class tests."""

    def test_init(self):
        toaster = ElectricAppliances(526, "toaster", 50.00, 23.26)
        self.assertEqual(toaster.brand, "N/A")
        self.assertEqual(toaster.voltage, "N/A")

        fridge = ElectricAppliances(9610, "fridge", 850.00, 150.00, voltage=120, brand="whirlpool")
        self.assertEqual(fridge.voltage, 120)
        self.assertEqual(fridge.brand, "whirlpool")

    def test_return_as_dict(self):
        fridge = ElectricAppliances(9610, "fridge", 850.00, 150.00, voltage=120, brand="whirlpool")
        fridge_dict = fridge.return_as_dictionary()

        self.assertEqual(fridge_dict["brand"], "whirlpool")
        self.assertEqual(fridge_dict["voltage"], 120)
