# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/11
# Code Poet: Anthony McKeever
# Start Date: 10/16/2019
# End Date: 10/18/2019

"""
Integration Tests for inventory_management.main and its modules
"""

import io
import sys

from unittest import TestCase
from unittest.mock import patch

import inventory_management.main as Main
import inventory_management.market_prices as Prices
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture


class TestIntegration(TestCase):
    """
    A collection of tests to validate the integration of main application and
    its modules.
    """

    def setUp(self):
        # Intercept the standard out to validate certain outputs are written
        # to the console.
        self.hold_stdout = sys.stdout
        self.stdout_intercept = io.StringIO()
        sys.stdout = self.stdout_intercept

        self.inventory = Inventory("Bird House",
                                   "Its a bird home",
                                   Prices.get_latest_price("Bird House"),
                                   2000)

        self.furniture = Furniture("Therapist Couch",
                                   "Tell me about your mother",
                                   Prices.get_latest_price("Therapist Couch"),
                                   3000,
                                   "existential crises",
                                   "L")

        self.appliance = ElectricAppliances("edp_001",
                                            "Electric Dog Polisher",
                                            Prices.get_latest_price("edp_001"),
                                            4000,
                                            "Purina",
                                            5)

    def tearDown(self):
        sys.stdout = self.hold_stdout

    def test_add_new_item_inventory(self):
        """
        Validates end to end flow of adding an Inventory item, getting its
        info and exiting the application
        """
        self.validate_add_new_item(self.inventory)

    def test_add_new_item_furniture(self):
        """
        Validates end to end flow of adding a Furniture item, getting its
        info and exiting the application
        """
        self.validate_add_new_item(self.furniture)

    def test_add_new_item_appliance(self):
        """
        Validates end to end flow of adding an ElectricAppliances item,
        getting its info and exiting the application
        """
        self.validate_add_new_item(self.appliance)

    def validate_add_new_item(self, inv):
        """
        Performs the test steps and assersions for end to end
        integration tests.
        """
        with patch("builtins.input") as handle_input:
            handle_input.side_effect = self.get_inputs(inv)

            with self.assertRaises(SystemExit):
                Main.main()

            std_out = self.stdout_intercept.getvalue()

            new_item_msg = "New inventory item added"
            self.assertTrue(std_out.count(new_item_msg) == 1)

            # The number of times the inventory's dictionary item should
            # appear is 3 based on the steps the application takes.
            # Once from the main.item_info method.
            # Twice from the main.main() method loop which prints it with each
            # iteration of the loop.
            inv_dict = inv.return_as_dictionary()
            self.assertTrue(std_out.count(str(inv_dict)) == 3)

    def get_inputs(self, inv):
        """
        Return the inputs for navigating menus and inputing inventory items.
        """
        inputs = ["1",               # main.add_new_item()
                  inv.product_code,  # Input product code.
                  inv.description,   # Input description
                  inv.rental_price]  # Input rental price

        if inv == self.inventory:
            inputs.extend(["n",      # Not Furniture
                           "n"])     # Not Electric Appliance

        elif inv == self.furniture:
            inputs.extend(["y",           # Is Furniture
                           inv.material,  # Input Material
                           inv.size])     # Input Size

        elif inv == self.appliance:
            inputs.extend(["n",           # Not Furniture
                           "y",           # Is Electric Appliance
                           inv.brand,     # Input Brand
                           inv.voltage])  # Input Voltage

        inputs.extend(["",                # Press Enter to return to menu
                       "2",               # main.item_info()
                       inv.product_code,  # Valid item product code
                       "",                # Press Enter to return to menu
                       "2",               # main.item_info()
                       "asd",             # Invalid product code
                       "",                # Press Enter to return to menu
                       "z",               # Invalid menu option
                       "q"])              # Quit Application

        return inputs
