"""
Unit tests for Lesson 01 inventory management system.
"""

import unittest
from unittest import mock

import os, sys
_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_dir, "inventory_management"))

import electric_appliances_class
import furniture_class
import inventory_class
import main
import market_prices


class TestElectricAppliances(unittest.TestCase):
    """Test :py:class:`electric_appliances_class.ElectricAppliances`"""

    def setUp(self) -> None:
        self.product_code = 0
        self.description = 1
        self.market_price = 2
        self.rental_price = 3
        self.brand = 4
        self.voltage = 5

        self.electric_app = \
            electric_appliances_class.ElectricAppliances(self.product_code, self.description,
                                                         self.market_price, self.rental_price,
                                                         self.brand, self.voltage)

    def test_init(self):
        """Test that class was constructed properly."""

        self.assertEqual(self.product_code, self.electric_app.product_code)
        self.assertEqual(self.description, self.electric_app.description)
        self.assertEqual(self.market_price, self.electric_app.market_price)
        self.assertEqual(self.rental_price, self.electric_app.rental_price)
        self.assertEqual(self.brand, self.electric_app.brand)
        self.assertEqual(self.voltage, self.electric_app.voltage)

    def test_return_as_dict(self):
        output = self.electric_app.return_as_dict()

        self.assertEqual(self.product_code, output['productCode'])
        self.assertEqual(self.description, output['description'])
        self.assertEqual(self.market_price, output['marketPrice'])
        self.assertEqual(self.rental_price, output['rentalPrice'])
        self.assertEqual(self.brand, output['brand'])
        self.assertEqual(self.voltage, output['voltage'])


class TestFurniture(unittest.TestCase):
    """Test :py:class:`furniture_class.Furniture`"""

    def setUp(self) -> None:
        self.product_code = 0
        self.description = 1
        self.market_price = 2
        self.rental_price = 3
        self.material = 4
        self.size = 5

        self.furniture = furniture_class.Furniture(self.product_code, self.description,
                                                   self.market_price, self.rental_price,
                                                   self.material, self.size)

    def test_init(self):
        """Test that class was constructed properly."""

        self.assertEqual(self.product_code, self.furniture.product_code)
        self.assertEqual(self.description, self.furniture.description)
        self.assertEqual(self.market_price, self.furniture.market_price)
        self.assertEqual(self.rental_price, self.furniture.rental_price)
        self.assertEqual(self.material, self.furniture.material)
        self.assertEqual(self.size, self.furniture.size)

    def test_return_as_dict(self):

        output = self.furniture.return_as_dict()

        self.assertEqual(self.product_code, output['productCode'])
        self.assertEqual(self.description, output['description'])
        self.assertEqual(self.market_price, output['marketPrice'])
        self.assertEqual(self.rental_price, output['rentalPrice'])
        self.assertEqual(self.material, output['material'])
        self.assertEqual(self.size, output['size'])


class TestInventory(unittest.TestCase):
    """Test :py:class:`inventory_class.Inventory`"""

    def setUp(self) -> None:
        self.product_code = 0
        self.description = 1
        self.market_price = 2
        self.rental_price = 3

        self.inventory = inventory_class.Inventory(self.product_code, self.description,
                                                   self.market_price, self.rental_price)

    def test_init(self):
        """Test that class was constructed properly."""

        self.assertEqual(self.product_code, self.inventory.product_code)
        self.assertEqual(self.description, self.inventory.description)
        self.assertEqual(self.market_price, self.inventory.market_price)
        self.assertEqual(self.rental_price, self.inventory.rental_price)

    def test_return_as_dict(self):

        output = self.inventory.return_as_dict()

        self.assertEqual(self.product_code, output['productCode'])
        self.assertEqual(self.description, output['description'])
        self.assertEqual(self.market_price, output['marketPrice'])
        self.assertEqual(self.rental_price, output['rentalPrice'])


class TestMarketPrices(unittest.TestCase):
    """Test the ``market_prices`` module."""

    def test_get_latest_price(self):
        """Test :py:func:`market_prices.get_latest_price`"""

        # For any input, the result is 24
        for x in ('a', 1, None, True):
            self.assertEqual(24, market_prices.get_latest_price(x))


class TestMain(unittest.TestCase):
    """Test ``main`` module."""

    def test_main_menu(self):

        # Assert that valid options are accepted
        self.assertIs(main.add_new_item, main.main_menu("1"))
        self.assertIs(main.item_info, main.main_menu("2"))
        self.assertIs(main.exit_program, main.main_menu("q"))

    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_main_menu_prompts(self, print_mock, input_mock):

        # Assert that input is accepted
        input_mock.return_value = "1"
        self.assertIs(main.add_new_item, main.main_menu())

        input_mock.return_value = "2"
        self.assertIs(main.item_info, main.main_menu("not valid"))

        input_mock.return_value = "q"
        self.assertIs(main.exit_program, main.main_menu())

    @mock.patch("builtins.print")
    def test_get_price(self, print_mock):

        with mock.patch("market_prices.get_latest_price") as market_patch:
            market_patch.return_value = 1
            main.get_price('abc')
            market_patch.assert_called()
            print_mock.assert_called_with(1)

    @mock.patch("builtins.print")
    def test_add_new_item(self, print_mock):
        """Test :py:func:`main.add_new_item`"""

        # Set up Mocks
        furniture_class.Furniture.return_as_dict = mock.MagicMock(return_value="furniture")
        electric_appliances_class.ElectricAppliances.return_as_dict = \
            mock.MagicMock(return_value="electric")
        inventory_class.Inventory.return_as_dict = mock.MagicMock(return_value="inventory")

        # Add furniture
        main.FULLINVENTORY = {}
        with mock.patch("builtins.input") as mock_input:
            mock_input.side_effect = ['Code', 'Desc', '23', 'y', 'mat', 'S']
            main.add_new_item()
            self.assertEqual("furniture", main.FULLINVENTORY['Code'])

        # Add electric appliance
        with mock.patch("builtins.input") as mock_input:
            mock_input.side_effect = ["Code2", 'Desc', '23', 'n', 'y', 'brand', 'voltage']
            main.add_new_item()
            self.assertEqual("electric", main.FULLINVENTORY['Code2'])

        # Add generic inventory
        with mock.patch("builtins.input") as mock_input:
            mock_input.side_effect = ["Code3", 'Desc', '23', 'n', 'n']
            main.add_new_item()
            self.assertEqual("inventory", main.FULLINVENTORY['Code3'])

    def test_item_info(self):
        """Tests :py:func:`main.item_info`"""

        out1 = {1: 'a', 2: 'b'}
        out2 = {3: 'c', 4: 'd'}
        main.FULLINVENTORY = {'abc': out1, 'def': out2}

        with mock.patch("builtins.print") as print_mock, mock.patch("builtins.input") as input_mock:
            input_mock.return_value = "abc"

            main.item_info()
            for k, val in out1.items():
                print_mock.assert_any_call(f"{k}:{val}")

        with mock.patch("builtins.print") as print_mock, mock.patch("builtins.input") as input_mock:
            input_mock.return_value = "def"

            main.item_info()
            for k, val in out2.items():
                print_mock.assert_any_call(f"{k}:{val}")

        with mock.patch("builtins.print") as print_mock, mock.patch("builtins.input") as input_mock:
            input_mock.return_value = "ghi"
            main.item_info()
            print_mock.assert_called_with("Item not found in inventory")

    @mock.patch("sys.exit")
    def test_exit_program(self, sys_exit_mock):

        main.exit_program()
        self.assertTrue(sys_exit_mock.assert_called)
