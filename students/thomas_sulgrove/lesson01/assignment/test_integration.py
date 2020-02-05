"""Integration tests for inventory management"""
from unittest import TestCase
import io
import sys
from unittest.mock import patch
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.main import main_menu, get_price, add_new_item, item_info, exit_program, FULL_INVENTORY
from inventory_management.market_prices import get_latest_price


class ModuleTests(TestCase):
    """ module test """
    def test_module(self):
        """ initiate item's attributes and test """
        inventory = ['0', 'desc', '1', 'n', 'n']
        with patch('builtins.input', side_effect=inventory):
            add_new_item()

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        with patch('builtins.input', side_effect=['0']):
            item_info()
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(),
                         'product_code:0\ndescription:desc\nmarket_price:24\nrental_price:1\n')

