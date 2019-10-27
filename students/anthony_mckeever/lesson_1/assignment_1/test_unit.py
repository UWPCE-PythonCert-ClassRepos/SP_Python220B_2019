# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# RedMine Issue - SchoolOps-11
# Code Poet: Anthony McKeever
# Start Date: 10/16/2019
# End Date: 10/18/2019

"""
Unit Tests for Inventory Management and its Modules
"""

import io
import sys

from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

import inventory_management.main as Main
import inventory_management.market_prices as MarketPrices
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture


class MarketPriceTests(TestCase):
    """ Unit Tests for MarketPrices Module. """

    def test_get_market_price(self):
        """
        MarketPrices.get_latest_price will always return 24 for now.
        TODO: Fix this test upon build out of MarketPrices.get_latest_price
        """
        for i in range(10):
            self.assertEqual(24, MarketPrices.get_latest_price(i))


class InventoryTests(TestCase):
    """ Unit Tests for Inventory Module. """

    def setUp(self):
        self.inventory = Inventory("123", "xyz", 23, 200)

    def test_inventroy_variables(self):
        """
        Validates setting the variables of an Inventory object.
        """
        self.assertEqual("123", self.inventory.product_code)
        self.assertEqual("xyz", self.inventory.description)
        self.assertEqual(23, self.inventory.market_price)
        self.assertEqual(200, self.inventory.rental_price)

    def test_inventory_as_dictionary(self):
        """
        Validates Return As Dictionary method of an Inventory object.
        """
        inventory_dict = self.inventory.return_as_dictionary()
        self.assertEqual("123", inventory_dict.get("product_code"))
        self.assertEqual("xyz", inventory_dict.get("description"))
        self.assertEqual(23, inventory_dict.get("market_price"))
        self.assertEqual(200, inventory_dict.get("rental_price"))


class FurnitureTests(TestCase):
    """ Unit Tests for Furniture Module. """

    def setUp(self):
        self.furniture = Furniture("sophie", "loaphie", -34, 2000, "stuff", 2)

    def test_furniture_variables(self):
        """
        Validates setting the variables of a Furniture object.
        """
        self.assertEqual("sophie", self.furniture.product_code)
        self.assertEqual("loaphie", self.furniture.description)
        self.assertEqual(-34, self.furniture.market_price)
        self.assertEqual(2000, self.furniture.rental_price)
        self.assertEqual("stuff", self.furniture.material)
        self.assertEqual(2, self.furniture.size)

    def test_furniture_as_dictionary(self):
        """
        Validates Return As Dictionary method of an Furniture object.
        """
        furniture_dict = self.furniture.return_as_dictionary()
        self.assertEqual("sophie", furniture_dict.get("product_code"))
        self.assertEqual("loaphie", furniture_dict.get("description"))
        self.assertEqual(-34, furniture_dict.get("market_price"))
        self.assertEqual(2000, furniture_dict.get("rental_price"))
        self.assertEqual("stuff", furniture_dict.get("material"))
        self.assertEqual(2, furniture_dict.get("size"))


class ElectricAppliancesTests(TestCase):
    """ Unit Tests for ElectricAppliances Module """

    def setUp(self):
        self.appliance = ElectricAppliances("fc_001",
                                            "Flux Capacitor",
                                            20000,
                                            2000,
                                            "Doc Brown Labs",
                                            "2.21 Jiggawatts")

    def test_electric_appliance_variables(self):
        """
        Validates setting the variables of a ElectricAppliances object.
        """
        self.assertEqual("fc_001", self.appliance.product_code)
        self.assertEqual("Flux Capacitor", self.appliance.description)
        self.assertEqual(20000, self.appliance.market_price)
        self.assertEqual(2000, self.appliance.rental_price)
        self.assertEqual("Doc Brown Labs", self.appliance.brand)
        self.assertEqual("2.21 Jiggawatts", self.appliance.voltage)

    def test_electric_appliance_as_dictionary(self):
        """
        Validates Return As Dictionary method of an ElectricAppliances object.
        """
        appliance_dict = self.appliance.return_as_dictionary()
        self.assertEqual("fc_001", appliance_dict.get("product_code"))
        self.assertEqual("Flux Capacitor", appliance_dict.get("description"))
        self.assertEqual(20000, appliance_dict.get("market_price"))
        self.assertEqual(2000, appliance_dict.get("rental_price"))
        self.assertEqual("Doc Brown Labs", appliance_dict.get("brand"))
        self.assertEqual("2.21 Jiggawatts", appliance_dict.get("voltage"))


class MainTests(TestCase):
    """ Unit Tests for the Main application. """

    def setUp(self):
        # Intercept the standard out to validate certain outputs are written
        # to the console.
        self.hold_stdout = sys.stdout
        self.stdout_intercept = io.StringIO()
        sys.stdout = self.stdout_intercept

    def tearDown(self):
        # Restore standard out after test complete.
        sys.stdout = self.hold_stdout

    def test_main_menu(self):
        """
        Validates the Main Menu.
        """
        with patch("builtins.input") as handle_input:
            handle_input.return_value = "1"
            self.assertIs(Main.add_new_item, Main.main_menu())

            handle_input.return_value = "2"
            self.assertIs(Main.item_info, Main.main_menu())

            handle_input.return_value = "q"
            self.assertIs(Main.exit_program, Main.main_menu())

    def test_add_new_item_inventory(self):
        """
        Validates the Main.add_new_item's Inventory object flow.
        """
        with patch("builtins.input") as handle_input:
            handle_input.side_effect = ["inventory",       # product code
                                        "stuff in a box",  # description
                                        2000,              # rental price
                                        "n",               # not furniture
                                        "n"]               # not appliance

            self.validate_add_new_item("inventory", Inventory)

    def test_add_new_item_furniture(self):
        """
        Validates the Main.add_new_item's Furniture object flow.
        """
        with patch("builtins.input") as handle_input:
            handle_input.side_effect = ["furniture",       # product code
                                        "sophie loaphie",  # description
                                        3000,              # rental price
                                        "y",               # is furniture
                                        "loaphie sophie",  # material
                                        "smallish"]        # size

            self.validate_add_new_item("furniture", Furniture)

    def test_add_new_item_appliance(self):
        """
        Validates the Main.add_new_item's ElectricAppliances object flow.
        """
        with patch("builtins.input") as handle_input:
            handle_input.side_effect = ["appliance",  # product code
                                        "Poké Ball",  # description
                                        200,          # rental price
                                        "n",          # not furniture
                                        "y",          # is appliance
                                        "Silph Co.",  # brand
                                        "1.5"]        # voltage

            self.validate_add_new_item("appliance", ElectricAppliances)

    def validate_add_new_item(self, inv, inv_type):
        """
        Performs the assertions for the Main.add_new_item function.
        """
        # Hold the MarketPrices.get_latest_price to restore after mock is
        # no longer needed so MarketPrices unit tests won't inadvertently fail
        # if execution order is randomized by coverage.py or python unittest
        hold_prices = MarketPrices.get_latest_price

        inv_type.return_as_dictionary = MagicMock(return_value="stuff")
        MarketPrices.get_latest_price = MagicMock(return_value=5)

        Main.add_new_item()
        main_inv = Main.FULL_INVENTORY.get(inv)
        self.assertEqual("stuff", main_inv)

        std_out = self.stdout_intercept.getvalue()
        new_item_msg = "New inventory item added"
        self.assertTrue(std_out.count(new_item_msg) == 1)

        # Restore original MarketPrices.get_latest_price
        MarketPrices.get_latest_price = hold_prices

    def test_item_info_existing_item(self):
        """
        Validates Main.item_info for an item in Main.FULL_INVENTORY.
        """
        Main.FULL_INVENTORY["123"] = {"sophie": "loaphie"}
        self.validate_item_info_print("123", "sophie:loaphie")

    def test_item_info_nonexistent_item(self):
        """
        Validates Main.item_info for an item not in Main.FULL_INVENTORY.
        """
        msg = "Item not found in inventory"
        self.validate_item_info_print("456", msg)

    def validate_item_info_print(self, input_val, expected):
        """
        Performs the call and assertion for Main.item_info.

        :self:          The Class
        :input_val:     The user's input value to mock.
        :expected:      The expected output in the console.
        """
        with patch("builtins.input") as handle_input:
            handle_input.return_value = input_val
            Main.item_info()

            std_out = self.stdout_intercept.getvalue()
            self.assertTrue(std_out.count(expected) == 1)

    def test_exit_program(self):
        """
        Validates Main.exit_program calls sys.exit.
        """
        with self.assertRaises(SystemExit):
            Main.exit_program()

    def test_main(self):
        """
        Validates Main.main's while loop.
        """
        Main.add_new_item = MagicMock()
        with patch("builtins.input") as handle_input:
            handle_input.side_effect = ["1",  # Enter Mocked method
                                        "",   # Emulate "Enter" key press
                                        "q"]  # Quit application to break loop

            with self.assertRaises(SystemExit):
                Main.main()
