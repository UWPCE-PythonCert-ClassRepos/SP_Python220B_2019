# Advanced Programming in Python -- Lesson 1 Assignment One
# Jason Virtue
# Start Date 2/1/2020


"""
Inventory Management and its Modules Unit Test
"""

import io
import sys

from unittest import TestCase
from unittest.mock import patch, MagicMock

import inventory_management.main as Main
import inventory_management.market_prices as MarketPrices
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture

class MarketPriceTests(TestCase):
    """Unit test for market price module"""

    def test_get_market_price(self):

        """Get market price which returns hard-coded 24 value"""

        for i in range(10):
            self.assertEqual(24, MarketPrices.get_latest_price(i))

class InventoryTests(TestCase):
    """Unit test for inventory module"""

    def setUp(self):
        self.inventory = Inventory("123", "abc", 55, 100)

    def test_inventory_variables(self):
        """
        Test cases to validate
        """
        self.assertEqual("123", self.inventory.product_code)
        self.assertEqual("abc", self.inventory.description)
        self.assertEqual(55, self.inventory.market_price)
        self.assertEqual(100, self.inventory.rental_price)
    
    def test_inventory_as_dictionary(self):
        """Validate return as dictionary method"""
        inventory_dict = self.inventory.return_as_dictionary()
        self.assertEqual("123", inventory_dict.get("product_code"))
        self.assertEqual("abc", inventory_dict.get("description"))
        self.assertEqual(55, inventory_dict.get("market_price"))
        self.assertEqual(100, inventory_dict.get("rental_price"))


class FurnitureTests(TestCase):
    """Unit tests for Furniture module"""

    def setUp(self):
        self.furniture = Furniture("RTG01", "Bed", 100, 50, "cotton", 10)

    def test_furniture_variables(self):
        """Compares actuals to variables"""
        self.assertEqual("RTG01", self.furniture.product_code)
        self.assertEqual("Bed", self.furniture.description)
        self.assertEqual(100, self.furniture.market_price)
        self.assertEqual(50, self.furniture.rental_price)
        self.assertEqual("cotton", self.furniture.material)
        self.assertEqual(10, self.furniture.size)

    def test_furniture_as_dictionary(self):
        """Validate return as dictionary method"""
        furniture_dict = self.furniture.return_as_dictionary()
        self.assertEqual("RTG01", furniture_dict.get("product_code"))
        self.assertEqual("Bed", furniture_dict.get("description"))
        self.assertEqual(100, furniture_dict.get("market_price"))
        self.assertEqual(50, furniture_dict.get("rental_price"))
        self.assertEqual("cotton", furniture_dict.get("material"))
        self.assertEqual(10, furniture_dict.get("size"))

class ElectricAppliancesTestCases(TestCase):
    """Unit Test for Electric Appliances Module"""

    def setUp(self):
        self.appliance = ElectricAppliances("Surface01", "Book", 2000, 20, "Microsoft", "120")
    
    def test_electric_appliance_variables(self):
        """Compare actuals to variables"""
        self.assertEqual("Surface01", self.appliance.product_code)
        self.assertEqual("Book", self.appliance.description)
        self.assertEqual(2000, self.appliance.market_price)
        self.assertEqual(20, self.appliance.rental_price)
        self.assertEqual("Microsoft", self.appliance.brand)
        self.assertEqual("120", self.appliance.voltage)

    def test_electric_appliance_as_dictionary(self):
        """Compares actuals to dictionary"""
        appliance_dict = self.appliance.return_as_dictionary()
        self.assertEqual("Surface01", appliance_dict.get("product_code"))
        self.assertEqual("Book", appliance_dict.get("description"))
        self.assertEqual(2000, appliance_dict.get("market_price"))
        self.assertEqual(20, appliance_dict.get("rental_price"))
        self.assertEqual("Microsoft", appliance_dict.get("brand"))
        self.assertEqual("120", appliance_dict.get("voltage"))

class MainTests(TestCase):
    """ Tests for Main menu application """
    def setUp(self):
        self.hold_stdout = sys.stdout
        self.stdout_intercept = io.StringIO()
        sys.stdout = self.stdout_intercept

    def tearDown(self):
        sys.stdout = self.hold_stdout

    def test_main_menu(self):
        """Tests navigation of main menu"""
        with patch("builtins.input") as handle_input:
            handle_input.return_value = "1"
            self.assertIs(Main.add_new_item, Main.main_menu())

            handle_input.return_value = "2"
            self.assertIs(Main.item_info, Main.main_menu())

            handle_input.return_value = "q"
            self.assertIs(Main.exit_program, Main.main_menu())

    def test_add_new_item_inventory(self):
        """Tests generic inventory items"""
        with patch("builtins.input") as handle_input:
            handle_input.side_effect = ["inventory",       # product code
                                        "Cool Stuff",  # description
                                        2000,              # rental price
                                        "n",               # not furniture
                                        "n"]               # not appliance

            self.validate_add_new_item("inventory", Inventory)

    def test_add_new_item_furniture(self):
        """Test Furniture items work flow"""
        with patch("builtins.input") as handle_input:
            handle_input.side_effect = ["furniture",       # product code
                                        "RTG",  # description
                                        3000,              # rental price
                                        "y",               # is furniture
                                        "Canvas",  # material
                                        "smallish"]        # size

            self.validate_add_new_item("furniture", Furniture)

    def test_add_new_item_appliance(self):
        """Tests ElectricAppliances work flow"""
        with patch("builtins.input") as handle_input:
            handle_input.side_effect = ["appliance",  # product code
                                        "Surface",  # description
                                        200,          # rental price
                                        "n",          # not furniture
                                        "y",          # is appliance
                                        "Microsoft",  # brand
                                        "120"]        # voltage

            self.validate_add_new_item("appliance", ElectricAppliances)

    def validate_add_new_item(self, inv, inv_type):
        """Performs the assertions for the Main.add_new_item function."""

        hold_prices = MarketPrices.get_latest_price

        inv_type.return_as_dictionary = MagicMock(return_value="stuff")
        MarketPrices.get_latest_price = MagicMock(return_value=24)

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
        """Test main while loop"""
        Main.add_new_item = MagicMock()
        with patch("builtins.input") as handle_input:
            handle_input.side_effect = ["1",  # Enter Mocked method
                                        "",   # Emulate "Enter" key press
                                        "q"]  # Quit application to break loop

