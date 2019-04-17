"""Integration Tests for Inventory Management"""
import unittest
from unittest.mock import patch
import io
import sys
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.main import MainMenu


class IntegrationTests(unittest.TestCase):
    """Integration Tests for Inventory Management"""
    MOCK_PRICE = 50

    @patch("inventory_management.market_prices.get_latest_price",
           lambda c: IntegrationTests.MOCK_PRICE)
    @patch("sys.stdin",
           io.StringIO("1\ncode1\ndesc1\nprice1\ny\nmat1\nXL\n\n" +
                       "1\ncode2\ndesc2\nprice2\nn\ny\nbrand2\nvolt2\n\n" +
                       "1\ncode3\ndesc3\nprice3\nn\nn\n\nq"))
    def test_integration(self):
        """Integration Test for Inventory Management"""
        # Redirect stdout just so menu isn't displayed while testing
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        inventory = dict()
        with self.assertRaises(SystemExit):
            MainMenu(inventory).do_menu()

        expected = {
            "code1": Furniture("code1", "desc1", self.MOCK_PRICE,
                               "price1", "mat1", "XL").return_as_dictionary(),
            "code2": ElectricAppliances("code2", "desc2", self.MOCK_PRICE,
                                        "price2", "brand2",
                                        "volt2").return_as_dictionary(),
            "code3": Inventory("code3", "desc3", self.MOCK_PRICE,
                               "price3").return_as_dictionary()}
        self.assertEqual(expected, inventory)
        sys.stdout = old_stdout
