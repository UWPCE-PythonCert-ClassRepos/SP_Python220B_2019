from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
import io

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price
from inventory_management.main import main_menu, get_price, add_new_item
from inventory_management.main import item_info, exit_program, FULL_INVENTORY

class ElectricApplianceTests(TestCase):

    def test_electric_appliance(self):
        # Set up test appliance
        attributes = ['product_code', 'description', 'market_price',
                      'rental_price', 'brand', 'voltage']
        values = ['123', 'Blender', 200.0, 50.0, 'Maytag', 110]

        # Initialize (order of values must match inputs)
        electric_appliance = ElectricAppliances(*values)

        # Ensure that attributes match input values
        for attr, val in zip(attributes, values):
            self.assertEqual(getattr(electric_appliance,attr),val)

        # Ensure that conversion to dict works properly
        output_dict = electric_appliance.return_as_dictionary()

        # Ensure that each attribute is in dictionary and that dict value
        # matches attribute value
        for attr, val in zip(attributes, values):
            self.assertIn(attr, output_dict)
            self.assertEqual(output_dict[attr], val)

class FurnitureTests(TestCase):

    def test_furniture(self):
        # Set up test furniture
        attributes = ['product_code', 'description', 'market_price',
                      'rental_price', 'material', 'size']
        values = ['123', 'Chair', 100.0, 80.0, 'fabric', 'L']

        # Initialize (order of values must match inputs)
        furniture = Furniture(*values)

        # Ensure that attributes match input values
        for attr, val in zip(attributes, values):
            self.assertEqual(getattr(furniture,attr),val)

        # Ensure that conversion to dict works properly
        output_dict = furniture.return_as_dictionary()

        # Ensure that each attribute is in dictionary and that dict value
        # matches attribute value
        for attr, val in zip(attributes, values):
            self.assertIn(attr, output_dict)
            self.assertEqual(output_dict[attr], val)

class MarketPricesTests(TestCase):

    def test_mp(self):
        # As of now, market_prices is set to return 24, regardless of input
        # Should still test this to ensure coverage
        self.assertEqual(get_latest_price('test'),24)

class MainTests(TestCase):

    pass
