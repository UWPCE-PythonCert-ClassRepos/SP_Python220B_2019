"""Unit tests for the inventory management system."""


from unittest import TestCase
from unittest.mock import MagicMock, patch

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price
from inventory_management.main import main_menu, add_new_item, item_info, exit_program


class InventoryClassTests(TestCase):
    """Unit tests for the Inventory class."""

    def test_inventory_class(self):
        inventory_test = Inventory("GI-2", "Table", 500, 60)

        inventory_test_dict = {
            "product_code": "GI-2",
            "description": "Table",
            "market_price": 500,
            "rental_price": 60
        }

        self.assertDictEqual(vars(inventory_test), inventory_test_dict)
        self.assertDictEqual(inventory_test.return_as_dictionary(), inventory_test_dict)


class FurnitureClassTests(TestCase):
    """Unit tests for the Furniture class."""


    def test_furniture_class(self):
        furniture_test = Furniture("Wood", "L", "F-12", "Table", 500, 60)

        furniture_test_dict = {
            "material": "Wood",
            "size": "L",
            "product_code": "F-12",
            "description": "Table",
            "market_price": 500,
            "rental_price": 60
        }

        self.assertDictEqual(vars(furniture_test), furniture_test_dict)
        self.assertDictEqual(furniture_test.return_as_dictionary(), furniture_test_dict)


class ElectricApplianceClassTests(TestCase):
    """Unit tests for the ElectricAppliance class."""

    def test_electic_appliance_class(self):
        appliance_test = ElectricAppliances("Maytag", 240, "EA-1", "Washing Machine", 650, 75)

        appliance_test_dict = {
            "brand": "Maytag",
            "voltage": 240,
            "product_code": "EA-1",
            "description": "Washing Machine",
            "market_price": 650,
            "rental_price": 75
        }

        self.assertDictEqual(vars(appliance_test), appliance_test_dict)
        self.assertDictEqual(appliance_test.return_as_dictionary(), appliance_test_dict)


class MarketPricesTests(TestCase):
    """Test of the market price retrieval items."""

    def test_market_prices(self):
        """Test the get_latest_price function."""
        self.assertEqual(24, get_latest_price("F-12"))


class MainTests(TestCase):
    """Unit tests for the main inventory management system."""

    @patch('main.input', create=True)
    def setUp(self):
        """Set up starting classes for use in main tests."""
        FULL_INVENTORY = {
            'GI-5': {
                'rental_price': '8',
                'market_price': 24,
                'product_code': 'GI-5',
                'description': 'Fake Plant'
            },
            'EA-2': {
                'rental_price': '25',
                'product_code': 'EA-2',
                'voltage': '110',
                'market_price': 24,
                'description': 'Washing Machine',
                'brand': 'Maytag'
            },
            'F-22': {
                'size': 'L',
                'rental_price': '45',
                'product_code': 'F-22',
                'material': 'Wood',
                'market_price': 24,
                'description': 'Dining Table'
            }
        }


    def test_get_item_info_present(self, mocked_input):
        """Tests the get_item_info function when the item is in inventory."""
        mocked_input.side_effect = ['F-22']
        expected_print = ("size: L\nrental_price: 45\nproduct_code: F-22\nmaterial: Wood\n"
                          "market_price: 24\ndescription: Dining Table")

        self.assertEqual(item_info(), expected_print)


    def test_get_item_info_not_present(self, mocked_input):
        """Tests the get_item_info function when the item is in inventory."""
        mocked_input.side_effect = ['F-20']
        self.assertEqual(item_info(), expected_print)

    def test_main_get_price(self):
        """Tests the get_price function."""

#        self.assertEqual()
