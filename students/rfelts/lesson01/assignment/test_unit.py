""" Unit tests """

from unittest import TestCase

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory


class ElectricAppliancesTest(TestCase):
    """ Test class for the ElectricAppliances class"""
    def test_electronic_appliances(self):
        """ Test that an electronic appliance object can be created """
        appliance_dict = {"product_code": 25, "description": "Microwave",
                          "market_price": 300, "rental_price": 10,
                          "brand": "Kitchen-aid", "voltage": 110}
        appliance = ElectricAppliances(25, "Microwave", 300, 10, "Kitchen-aid", 110)
        self.assertEqual(appliance.return_as_dictionary(), appliance_dict)


class FurnitureTest(TestCase):
    """ Test class for the Furniture class """
    def test_furniture(self):
        """ Test that a furniture object can be created """
        furniture_dict = {"product_code": 2, "description": "Couch", "market_price": 1500,
                          "rental_price": 100, "material": "leather", "size": "8ft"}
        furniture = Furniture(2, "Couch", 1500, 100, "leather", "8ft")
        self.assertEqual(furniture.return_as_dictionary(), furniture_dict)


class InventoryTest(TestCase):
    """ Test class for the Inventory class """
    def test_inventory(self):
        """ Test that an inventory object can be created """
        inventory_dict = {"product_code": 450, "description": "item", "market_price": 235,
                          "rental_price": 5}
        inventory = Inventory(450, "item", 235, 5)
        self.assertEqual(inventory.return_as_dictionary(), inventory_dict)
