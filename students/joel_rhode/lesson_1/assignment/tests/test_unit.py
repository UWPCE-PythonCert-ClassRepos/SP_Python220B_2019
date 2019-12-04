"""Unit tests for the inventory management system."""

import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import MagicMock, patch

sys.path.append('./inventory_management')

from inventory_class import Inventory
from furniture_class import Furniture
from electric_appliances_class import ElectricAppliances
from market_prices import get_latest_price
import main


class InventoryClassTests(TestCase):
    """Unit tests for the Inventory class."""
    def test_inventory_class(self):
        """Test for the Inventory class."""
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
        """Test for the Furniture class."""
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
        """Test of the ElectricAppliance class."""
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
    def setUp(self):
        """Set up starting classes for use in main tests."""
        main.FULL_INVENTORY = {
            'GI-5': {
                'rental_price': 8.0,
                'market_price': 24,
                'product_code': 'GI-5',
                'description': 'Round Sculpture'
            },
            'F-22': {
                'size': 'L',
                'rental_price': 45.0,
                'product_code': 'F-22',
                'material': 'Wood',
                'market_price': 24,
                'description': 'Dining Table'
            }
        }


    def test_get_item_info_present(self):
        """Tests the get_item_info function when the item is in inventory."""
        expected_print = ('description: Dining Table\nmarket_price: 24\nmaterial: Wood\n'
                          'product_code: F-22\nrental_price: 45.0\nsize: L')
        with patch('builtins.input', return_value='F-22'), \
             patch('sys.stdout', new=StringIO()) as captured_output:
            main.item_info()
            self.assertEqual(captured_output.getvalue().strip(), expected_print)


    def test_get_item_info_not_present(self):
        """Tests the get_item_info function when the item is not in inventory."""
        expected_print = ("Item not found in inventory.")
        with patch('builtins.input', return_value='F-20'), \
             patch('sys.stdout', new=StringIO()) as captured_output:
            main.item_info()
            self.assertEqual(captured_output.getvalue().strip(), expected_print)

    @patch('main.market_prices.get_latest_price', return_value=200.)
    @patch('builtins.input')
    def test_main_add_new_item_basic(self, mock_input, mock_latest_price):
        """Tests the add_new_item function in main.py for general inventory."""
        with patch('main.inventory_class.Inventory') as mock_inventory:
            mock_inventory.return_as_dictionary = MagicMock(return_value=0)
            mock_input.side_effect = ['GI-1', 'Fake Plant', 50., 'n', 'n']
            main.add_new_item()
            mock_inventory.assert_called_with('GI-1', 'Fake Plant', 200., 50.)

    @patch('main.market_prices.get_latest_price', return_value=150.)
    @patch('builtins.input')
    def test_main_add_new_item_furniture(self, mock_input, mock_latest_price):
        """Tests the add_new_item function in main.py for furniture."""
        with patch('main.furniture_class.Furniture') as mock_inventory:
            mock_inventory.return_as_dictionary = MagicMock(return_value=0)
            mock_input.side_effect = ['F-1', 'Table', 75., 'y', 'Wood', 'L']
            main.add_new_item()
            mock_inventory.assert_called_with('Wood', 'L', 'F-1', 'Table', 150., 75.)

    @patch('main.market_prices.get_latest_price', return_value=450.)
    @patch('builtins.input')
    def test_main_add_new_item_appliance(self, mock_input, mock_latest_price):
        """Tests the add_new_item function in main.py for an electric appliance."""
        with patch('main.electric_appliances_class.ElectricAppliances') as mock_inventory:
            mock_inventory.return_as_dictionary = MagicMock(return_value=0)
            mock_input.side_effect = ['EA-2', 'Dishwasher', 100., 'n', 'y', 'Maytag', '240']
            main.add_new_item()
            mock_inventory.assert_called_with('Maytag', '240', 'EA-2', 'Dishwasher', 450., 100.)


    def test_exit_program(self):
        """Tests the program quit function in main.py."""
        with self.assertRaises(SystemExit):
            main.exit_program()

    @patch('main.exit_program', return_value=2)
    @patch('main.item_info', return_value=1)
    @patch('main.add_new_item', return_value=0)
    @patch('builtins.input')
    def test_main_menu(self, mock_input, mock_add_new_item, mock_item_info, mock_exit_program):
        """Tests the main menu."""
        mock_input.side_effect = ['1', '2', 'q']
        for output in range(3):
            self.assertEqual(main.main_menu(), output)
