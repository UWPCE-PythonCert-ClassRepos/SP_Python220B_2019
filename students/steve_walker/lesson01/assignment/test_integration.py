"""Integration tests for inventory_management files"""

from unittest import TestCase
from unittest.mock import patch

import inventory_management.main as main


class IntegrationTests(TestCase):
    """
    Test adding one of each item to full_inventory, ensuring full_inventory
    grows with each addition as expected.
    """

    def test_add_new_items(self):

        # Test adding furniture item to the full_inventory
        furniture_inputs = (123, "sample description", "sample rental price",
                            "y", "sample material", "sample size")

        sample_inventory = {123: {'product_code': 123,
                          'description': "sample description",
                          'market_price': 24,
                          'rental_price': "sample rental price",
                          'material': "sample material",
                          'size': "sample size"}}

        with patch('builtins.input', side_effect=furniture_inputs):
            main.add_new_item()
        self.assertEqual(main.full_inventory, sample_inventory)

        # Test adding electronic appliance item to the full_inventory
        electronic_app_inputs = (122, "sample description",
                                 "sample rental price", "n", "y",
                                 "sample brand", "sample voltage")

        sample_inventory[122] = {'product_code': 122,
                          'description': "sample description",
                          'market_price': 24,
                          'rental_price': "sample rental price",
                          'brand': "sample brand",
                          'voltage': "sample voltage"}

        with patch('builtins.input', side_effect=electronic_app_inputs):
            main.add_new_item()
        self.assertEqual(main.full_inventory, sample_inventory)

        # Test adding general inventory item to the full_inventory
        inventory_inputs = (121, "sample description", "sample rental price",
                            "n", "n")

        sample_inventory[121] = {'product_code': 121,
                          'description': "sample description",
                          'market_price': 24,
                          'rental_price': "sample rental price"}

        with patch('builtins.input', side_effect=inventory_inputs):
            main.add_new_item()
        self.assertEqual(main.full_inventory, sample_inventory)
