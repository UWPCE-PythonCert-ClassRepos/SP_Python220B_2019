import sys
import os
# Got any better ideas?
#
# What I want to do:
#   use these comands from outside inventory_management folder:
#   ...\lesson01\assignment>python inventory_management\main.py
#   ...\lesson01\assignment>python -m pylint inventory_management
#   ...\lesson01\assignment>python -m coverage run --source=inventory_management -m unittest test_unit.py
#
# Challenges:
#   Causes all remaining imports to fail flake8
#   I don't want to hardcode a path to the inventory_management folder
#   I don't want to modify the path at all
sys.path.insert(1, f"{os.getcwd()}\\inventory_management")
# sys.path.insert(1, '\\Users\\erica\\Desktop\\Python220\\SP_Python220B_2019\\'
#                 'students\\erica_edwards\\lesson01\\assignment\\inventory_management')

from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price
from inventory_management import main


class TestInventoryClass(TestCase):

    def test_inventory_init(self):
        """Mock test that a inventory.__init__ is called with the correct parameters"""
        self.mockInit = MagicMock()

        expected = {'product_code': '23',
                    'description': 'toaster',
                    'market_price': 49.99,
                    'rental_price': 37.95}

        _ = self.mockInit(*expected.values())

        self.mockInit.assert_called_with(*expected.values())
        self.mockInit.assert_called_with('23', 'toaster', 49.99, 37.95)

    def test_inventory_return(self):
        """Test that a inventory object is created"""

        expected = {'product_code': '23',
                    'description': 'toaster',
                    'market_price': 49.99,
                    'rental_price': 37.95}

        actual = Inventory(*expected.values())

        self.assertEqual(expected, actual.return_as_dictionary())


class TestElectricAppliancesClass(TestCase):

    def test_electric_appliances_init(self):
        """Mock test that a electric_appliances.__init__ is called with the correct parameters"""
        self.mockInit = MagicMock()

        expected = {'product_code': '23',
                    'description': 'toaster',
                    'market_price': 49.99,
                    'rental_price': 37.95,
                    'brand': 'GE',
                    'voltage': 2.5}

        _ = self.mockInit(*expected.values())

        self.mockInit.assert_called_with(*expected.values())
        self.mockInit.assert_called_with('23', 'toaster', 49.99, 37.95, 'GE', 2.5)

    def test_electric_appliances_return(self):
        """Test that a inventory object is created"""

        expected = {'product_code': '23',
                    'description': 'toaster',
                    'market_price': 49.99,
                    'rental_price': 37.95,
                    'brand': 'GE',
                    'voltage': 2.5}

        actual = ElectricAppliances(*expected.values())

        self.assertEqual(expected, actual.return_as_dictionary())


class TestFurnitureClass(TestCase):

    def test_Furniture_init(self):
        """Mock test that a furniture.__init__ is called with the correct parameters"""
        self.mockInit = MagicMock()

        expected = {'product_code': '23',
                    'description': 'toaster',
                    'market_price': 49.99,
                    'rental_price': 37.95,
                    'material': 'Velvet',
                    'size': 'xl'}

        _ = self.mockInit(*expected.values())

        self.mockInit.assert_called_with(*expected.values())
        self.mockInit.assert_called_with('23', 'toaster', 49.99, 37.95, 'Velvet', 'xl')

    def test_Furniture_return(self):
        """Test that a inventory object is created"""

        expected = {'product_code': '23',
                    'description': 'toaster',
                    'market_price': 49.99,
                    'rental_price': 37.95,
                    'material': 'Velvet',
                    'size': 'xl'}

        actual = Furniture(*expected.values())

        self.assertEqual(expected, actual.return_as_dictionary())


class TestMarketPrices(TestCase):
    """Test Market Price Returns set number and mocked number"""
    def test_market_prices(self):
        "Mock test market_prices"

        self.assertEqual(get_latest_price(624), 24)

        self.get_latest_price = MagicMock(return_value=38)
        assert self.get_latest_price(624) == 38


class TestMain(TestCase):
    """Test main menu"""
    def test_main_menu(self):
        """Test menu options use correct methods"""
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)

        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_add_new_mock_furniture(self):
        """Test furniture is added correctly"""
        item_1 = {"item_code": 624,
                  "item_description": "couch",
                  "item_rental_price": "35",
                  "is_furniture": "y",
                  "item_material": "Velvet",
                  "item_size": "XL"}
        print(item_1)
        expected = {'product_code': 624, 'description': 'couch', 'market_price': 82,
                    'rental_price': '35', 'material': 'Velvet', 'size': 'XL'}
        main.market_prices.get_latest_price = MagicMock(return_value=82)
        self.furniture_mock = MagicMock(return_value=expected)
        with patch("builtins.input", side_effect=item_1.values()):
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY[624], expected)

    def test_add_new_mock_electric_appliances(self):
        """Test electric appliance added correctly"""
        item_2 = {"item_code": 628,
                  "item_description": "toaster",
                  "item_rental_price": "35",
                  "is_furniture": "n",
                  "is_electic_appliance": "y",
                  "item_brand": "GE",
                  "item_voltage": 2.5}

        print(item_2)
        expected = {'product_code': 628, 'description': 'toaster', 'market_price': 82,
                    'rental_price': '35', 'brand': 'GE', 'voltage': 2.5}
        main.market_prices.get_latest_price = MagicMock(return_value=82)
        self.electric_appliances_mock = MagicMock(return_value=expected)
        with patch("builtins.input", side_effect=item_2.values()):
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY[628], expected)

    def test_add_new_mock_inventory(self):
        """Test new item added when not a piece of furniture or an electric appliance"""
        item_3 = {"item_code": 620,
                  "item_description": "wagon",
                  "item_rental_price": "35",
                  "is_furniture": "n",
                  "is_electic_appliance": "n"}

        print(item_3)
        expected = {'product_code': 620, 'description': 'wagon', 'market_price': 82,
                    'rental_price': '35'}
        main.market_prices.get_latest_price = MagicMock(return_value=82)
        self.inventory_mock = MagicMock(return_value=expected)
        with patch("builtins.input", side_effect=item_3.values()):
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY[620], expected)

    def test_item_info(self):
        """Test item info is printed based on item code entered"""
        test = {'product_code': 628, 'description': 'toaster', 'market_price': 82,
                'rental_price': '35', 'brand': 'GE', 'voltage': 2.5}
        expected = ('product_code: 628\n' 'description: toaster\n' 'market_price: 82\n'
                    'rental_price: 35\n' 'brand: GE\n' 'voltage: 2.5\n')
        with patch('builtins.input', side_effect=[628]):
            main.FULL_INVENTORY[628] = test
            self.assertEqual(main.item_info(), print(expected))

    def test_item_info_not_found(self):
        """Test expected output when item is not found"""
        expected = "Item not found in inventory"
        with patch('builtins.input', side_effect=[620]):
            main.FULL_INVENTORY[620] = {}
            self.assertEqual(main.item_info(), print(expected))

    def test_exit_program(self):
        """Test exiting program works"""
        with self.assertRaises(SystemExit):
            main.exit_program()
