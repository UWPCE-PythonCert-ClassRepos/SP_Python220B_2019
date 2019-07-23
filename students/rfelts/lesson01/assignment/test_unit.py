""" Unit tests for: electric_appliances_class, furniture_class, inventory_class, market_prices,
and main """

from unittest import TestCase
from unittest.mock import patch

from io import StringIO

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.market_prices as price
import inventory_management.main as main


class ElectricAppliancesTest(TestCase):
    """ Test class for the ElectricAppliances class"""

    def test_electronic_appliances(self):
        """ Test that an electronic appliance object can be created """

        appliance_dict = {"product_code": 25, "description": "Microwave",
                          "market_price": 300, "rental_price": 10,
                          "brand": "Kitchen-aid", "voltage": 110}

        appliance = ElectricAppliances(25, "Microwave", 300, 10, "Kitchen-aid", 110)
        self.assertEqual(appliance_dict, appliance.return_as_dictionary())


class FurnitureTest(TestCase):
    """ Test class for the Furniture class """

    def test_furniture(self):
        """ Test that a furniture object can be created """

        furniture_dict = {"product_code": 2, "description": "Couch", "market_price": 1500,
                          "rental_price": 100, "material": "leather", "size": "8ft"}

        furniture = Furniture(2, "Couch", 1500, 100, "leather", "8ft")
        self.assertEqual(furniture_dict, furniture.return_as_dictionary())


class InventoryTest(TestCase):
    """ Test class for the Inventory class """

    def test_inventory(self):
        """ Test that an inventory object can be created """

        inventory_dict = {"product_code": 450, "description": "item", "market_price": 235,
                          "rental_price": 5}

        inventory = Inventory(450, "item", 235, 5)
        self.assertEqual(inventory_dict, inventory.return_as_dictionary())


class MarketPricesTest(TestCase):
    """ Test class for Market Prices """

    def test_market_prices(self):
        """ Test getting the price of the requested item """
        self.assertEqual(24, price.get_latest_price(12))


class TestMain(TestCase):
    """ Test class for main """

    def test_main_menu(self):
        """Test for the main menu selections  """

        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.add_new_item, main.main_menu())

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.item_info, main.main_menu())

        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.exit_program, main.main_menu())

    def test_get_price(self):
        """ Test getting the price of the requested item """
        self.assertEqual(24, main.get_price(35))

    def test_add_new_item(self):
        """ Test the various items types cab be added to the inventory object """

        # Different inventory object lists used for testing. Remember to include the yes and
        # no answers for the item type.
        furniture_list = ["2", "Couch", "100", "Y", "leather", "8ft"]
        appliance_list = ["25", "Microwave", "10", "N", "Y", "Kitchen-aid", "110"]
        inventory_list = ["450", "item", "5", "N", "N"]

        inventory_dict = {"2": {"product_code": "2", "description": "Couch", "market_price": 1500,
                                "rental_price": "100", "material": "leather", "size": "8ft"},
                          "25": {"product_code": "25", "description": "Microwave",
                                 "market_price": 300, "rental_price": "10", "brand": "Kitchen-aid",
                                 "voltage": "110"},
                          "450": {"product_code": "450", "description": "item", "market_price": 235,
                                  "rental_price": "5"}}

        # Test adding a furniture object
        # First mock getting a value from market prices then mock the user input
        with patch('inventory_management.market_prices.get_latest_price', return_value=1500):
            with patch('builtins.input', side_effect=furniture_list):
                main.add_new_item()
                # Test for the furniture item in the full inventory dict
                self.assertEqual(inventory_dict.get("2"), main.FULL_INVENTORY.get("2"))

        # Test adding an appliance object
        with patch('inventory_management.market_prices.get_latest_price', return_value=300):
            with patch('builtins.input', side_effect=appliance_list):
                main.add_new_item()
                # Test for the appliance item in the full inventory dict
                self.assertEqual(inventory_dict.get("25"), main.FULL_INVENTORY.get("25"))

        # Test adding a generic inventory object
        with patch('inventory_management.market_prices.get_latest_price', return_value=235):
            with patch('builtins.input', side_effect=inventory_list):
                main.add_new_item()
                # Test for all the items (furniture, appliance, and inventory) are in the
                # full inventory dict
                self.assertEqual(inventory_dict, main.FULL_INVENTORY)

    def test_item_info(self):
        """Test getting item info  """

        # Reset the full inventory dict
        main.FULL_INVENTORY = {"2": {"product_code": "2", "description": "Couch",
                                     "market_price": 1500, "rental_price": "100",
                                     "material": "leather", "size": "8ft"}}
        expected_result = "product_code:2\ndescription:Couch\nmarket_price:1500" \
                          "\nrental_price:100\nmaterial:leather\nsize:8ft"

        # Need to capture stdout to be able to compare it with the expected output
        with patch('sys.stdout', new=StringIO()) as test_output:
            with patch('builtins.input', side_effect=["2"]):
                main.item_info()
                self.assertEqual(expected_result, test_output.getvalue().strip())

    def test_item_info_not_found(self):
        """ Test getting item info when the item is not in the inventory """

        # Reset the FULL_INVENTORY dict
        main.FULL_INVENTORY = {}
        expected_result = "Item not found in inventory"

        # Need to capture stdout to beable to compare it with the expected output
        with patch('sys.stdout', new=StringIO()) as test_output:
            with patch('builtins.input', side_effect=["15"]):
                main.item_info()
                self.assertEqual(expected_result, test_output.getvalue().strip())

    def test_exit_program(self):
        """ Test the exit program menu option """
        with self.assertRaises(SystemExit):
            main.exit_program()
