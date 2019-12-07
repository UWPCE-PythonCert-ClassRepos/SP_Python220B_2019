"""
Test Inventory Management system.
"""

import unittest
from unittest.mock import patch, MagicMock

import sys, os
_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_dir, "inventory_management"))

import main
import market_prices


class TestManagement(unittest.TestCase):
    """
    Test ``main`` module integrated with data classes.
    """

    def setUp(self) -> None:
        pass

    def test_program(self):

        # All market prices will be 1
        market_prices.get_latest_price = MagicMock(return_value=1)
        main.exit_program = MagicMock()

        with patch("builtins.input") as input_mock, patch("builtins.print") as print_mock:
            # Add a furniture item
            input_mock.side_effect = ['1', 'code1', 'desc1', '10', 'Y', 'wood', 'M']
            main.main_menu()()

            assert "code1" in main.FULLINVENTORY
            assert main.FULLINVENTORY['code1']['material'] == 'wood'

            # Get the furniture info
            input_mock.side_effect = ["2", "code1"]
            main.main_menu()()
            for k, val in {"description": "desc1", "rentalPrice": "10", "marketPrice": 1}.items():
                print_mock.assert_any_call(f"{k}:{val}")

            # Add an electric appliance
            input_mock.side_effect = ['1', 'code2', 'desc2', '5', 'N', 'y', 'brand', '9']
            main.main_menu()()

            assert "code2" in main.FULLINVENTORY
            assert main.FULLINVENTORY['code2']['brand'] == 'brand'
            assert main.FULLINVENTORY['code2']['voltage'] == '9'

            # Add a generic item
            input_mock.side_effect = ['1', 'code3', 'desc3', '5', 'N', 'n']
            main.main_menu()()

            assert "code3" in main.FULLINVENTORY
            assert main.FULLINVENTORY['code3']['description'] == 'desc3'
            assert main.FULLINVENTORY['code3']['marketPrice'] == 1

            # Get info
            input_mock.side_effect = ["2", "code3"]
            main.main_menu()()
            for k, val in {"description": "desc3", "rentalPrice": "5",
                           "marketPrice": 1, "productCode": 'code3'}.items():
                print_mock.assert_any_call(f"{k}:{val}")

            # Get info for a non-existent item
            input_mock.side_effect = ["2", "code4"]
            main.main_menu()()
            print_mock.assert_called_with("Item not found in inventory")

            # Exit
            input_mock.side_effect = ['q']
            main.main_menu()()

            main.exit_program.assert_called()
