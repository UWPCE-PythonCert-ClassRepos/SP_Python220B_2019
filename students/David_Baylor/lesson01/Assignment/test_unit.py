"""
test_unit.py
by David Baylor

Unit tests the inventory_manegment module.
"""
import sys

from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
from io import StringIO

import inventory_management.__main__ as main
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.market_prices import get_latest_price

class InventoryTest(TestCase):
    """Unit tests the Inventory class"""

    def test_add_item(self):
        """creates an object of the inventory class"""
        item = Inventory("1234", "Book", "$100", "$75")

        self.assertEqual("1234", item.product_code)
        self.assertEqual("Book", item.description)
        self.assertEqual("$100", item.market_price)
        self.assertEqual("$75", item.rental_price)

    def test_return_dict(self):
        """calls the return_as_dictionary function on the inventory class"""
        item = Inventory("1234", "Book", "$100", "$75")

        item_info = item.return_as_dictionary()
        self.assertEqual(item_info, {'product_code': '1234', 'description': 'Book',
                                     'market_price': '$100', 'rental_price': '$75'})

class ElectricAppliancesTest(TestCase):
    """Unit tests the ElectricAppliances class"""

    def test_add_electronic(self):
        """creates an object of the ElectricAppliendes class"""
        appliance = ElectricAppliances("1111", "Computer", "$800", "$100", "Dell", "120")

        self.assertEqual("1111", appliance.product_code)
        self.assertEqual("Computer", appliance.description)
        self.assertEqual("$800", appliance.market_price)
        self.assertEqual("$100", appliance.rental_price)
        self.assertEqual("Dell", appliance.brand)
        self.assertEqual("120", appliance.voltage)

    def test_return_dict(self):
        """calls the return_as_dictionary function on the ElectricAppliendes class"""

        appliance = ElectricAppliances("1111", "Computer", "$800", "$100", "Dell", "120")

        appliance_info = appliance.return_as_dictionary()
        self.assertEqual(appliance_info, {'product_code': '1111', 'description': 'Computer',
                                          'market_price': '$800', 'rental_price': '$100',
                                          'brand' : 'Dell', 'voltage' : '120'})
class FurnitureTest(TestCase):
    """Unit tests the Furniture class"""

    def test_add_furniture(self):
        """creates an object of the Furniture class"""
        furniture = Furniture("2222", "Chair", "$200", "$150", "Wood", "Small")

        self.assertEqual("2222", furniture.product_code)
        self.assertEqual("Chair", furniture.description)
        self.assertEqual("$200", furniture.market_price)
        self.assertEqual("$150", furniture.rental_price)
        self.assertEqual("Wood", furniture.material)
        self.assertEqual("Small", furniture.size)

    def test_return_dict(self):
        """calls the return_as_dictionary function on the Furniture class"""
        furniture = Furniture("2222", "Chair", "$200", "$150", "Wood", "Small")

        furniture_info = furniture.return_as_dictionary()
        self.assertEqual(furniture_info, {'product_code': '2222', 'description': 'Chair',
                                          'market_price': '$200', 'rental_price': '$150',
                                          'material' : 'Wood', 'size' : 'Small'})

class MainTest(TestCase):
    """Unit tests the main file"""

    def test_item_info_in_inventory(self):
        """unit tests the intem_info functon when the item is in the inventory"""
        main.input = MagicMock(return_value='1234')

        main.FULL_INVENTORY = {'1234': {'product_code': '1234', 'description': 'Pen',
                                        'market_price': 24, 'rental_price': '$0.50'}}

        with StringIO() as captured_output:
            sys.stdout = captured_output
            try:
                main.item_info()
            finally:
                sys.stdout = sys.__stdout__

            self.assertEqual(captured_output.getvalue(), "product_code:1234\ndescription:Pen\n"\
                                                         "market_price:24\nrental_price:$0.50\n")

    def test_item_info_not_in_inventory(self):
        """unit tests the intem_info functon when the item is not in the inventory"""

        main.input = MagicMock(return_value='1234')

        main.FULL_INVENTORY = {'1111': {'product_code': '1111', 'description': 'Pen',
                                        'market_price': 24, 'rental_price': '$0.50'}}

        with StringIO() as captured_output:
            sys.stdout = captured_output
            try:
                main.item_info()
            finally:
                sys.stdout = sys.__stdout__

            self.assertEqual(captured_output.getvalue(), "Item not found in inventory\n")

    def test_main_menue(self):
        """unit tests the main menue function"""

        main.input = MagicMock(return_value='1')
        main.add_new_item = MagicMock(return_value=1)

        with StringIO() as captured_output:
            sys.stdout = captured_output
            try:
                out_put = main.main_menu()
            finally:
                sys.stdout = sys.__stdout__

            self.assertEqual(captured_output.getvalue(),
                             """Please choose from the following options (1, 2, q):
1. Add a new item to the inventory
2. Get item information
q. Quit\n""")
            self.assertEqual(out_put(), 1)
    def test_add_new_item_else(self):
        """unit tests the add new item function in main when not adding furniture or electronics"""

        main.input = MagicMock()
        main.input.side_effect = ["1234", "Book", "$10", "N", "N"]
        main.get_latest_price = MagicMock(return_value="$15")

        with patch('inventory_management.__main__.Inventory') as mock_inventory:
            instance = mock_inventory.return_value
            instance.return_as_dictionary.return_value = {"product_code": "1234",
                                                          "description": "Book",
                                                          "market_price": "$15",
                                                          "rental_price": "$10"}

            main.add_new_item()

            mock_inventory.assert_called_with("1234", "Book", "$15", "$10")

        self.assertEqual(main.FULL_INVENTORY, {'1234': {'product_code': '1234',
                                                        'description': 'Book',
                                                        'market_price': "$15",
                                                        'rental_price': '$10'}})

    def test_add_new_item_furniture(self):
        """unit tests the add new item function in main when not adding furniture or electronics"""

        main.input = MagicMock()
        main.input.side_effect = ["1234", "Chair", "$25", "Y", "Wood", "S"]
        main.get_latest_price = MagicMock(return_value="$50")

        with patch('inventory_management.__main__.Furniture') as mock_furniture:
            instance = mock_furniture.return_value
            instance.return_as_dictionary.return_value = {"product_code": "1234",
                                                          "description": "Chair",
                                                          "market_price": "$50",
                                                          "rental_price": "$25",
                                                          "material": "Wood",
                                                          "size": "S"}

            main.add_new_item()

            mock_furniture.assert_called_with("1234", "Chair", "$50", "$25", "Wood", "S")

        self.assertEqual(main.FULL_INVENTORY, {'1234': {'product_code': '1234',
                                                        'description': 'Chair',
                                                        'market_price': "$50",
                                                        'rental_price': '$25',
                                                        'material': "Wood", "size": "S"}})

    def test_add_new_item_electronics(self):
        """unit tests the add new item function in main when not adding furniture or electronics"""

        main.input = MagicMock()
        main.input.side_effect = ["1234", "Computer", "$100", "N", "Y", "Dell", "120"]
        main.get_latest_price = MagicMock(return_value="$500")

        with patch('inventory_management.__main__.ElectricAppliances') as mock_electric_appliances:
            instance = mock_electric_appliances.return_value
            instance.return_as_dictionary.return_value = {"product_code": "1234",
                                                          "description": "Computer",
                                                          "market_price": "$500",
                                                          "rental_price": "$100",
                                                          "brand": "Dell",
                                                          "voltage": "120"}

            main.add_new_item()

            mock_electric_appliances.assert_called_with("1234", "Computer", "$500", "$100", "Dell",
                                                        "120")

        self.assertEqual(main.FULL_INVENTORY, {'1234': {'product_code': '1234',
                                                        'description': 'Computer',
                                                        'market_price': "$500",
                                                        'rental_price': '$100',
                                                        'brand': "Dell", "voltage": "120"}})

class MarketPricesTest(TestCase):
    """tests the market_prices file"""
    def test_market_prices(self):
        """runns output and asserts the return value"""
        out_put = get_latest_price("1234")
        self.assertEqual(out_put, 24)
