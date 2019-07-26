from unittest import TestCase
from unittest.mock import patch
from inventory_management.electric_appliances_class import *
from inventory_management.furniture_class import *
from inventory_management.inventory_class import *
from inventory_management.market_prices import *
from inventory_management.main import *


class IntegrationTests(TestCase):
    """Integration tests for inventory_management"""

    def test_main_add_inventory_integration(self):
        FULL_INVENTORY.clear()
        price = get_latest_price()

        # adding new item to inventory with main

        input_inventory = ['1', 'sushi', '1', 'n', 'n']
        item = Inventory('1', 'sushi', price, '1')
        with patch('builtins.input', side_effect=input_inventory):
            add_new_item()
            # Adding furniture item with main

        actual_inventory = FULL_INVENTORY
        expected_inventory = {
            '1': item.return_as_dictionary()}
        self.assertDictEqual(actual_inventory, expected_inventory)

    def test_main_add_furniture_integration(self):
        FULL_INVENTORY.clear()
        price = get_latest_price()

        input_furniture= ['2', 'table', '2', 'y', 'wood', 'S']
        item = Furniture('2', 'table', price, '2', 'wood', 'S')
        with patch('builtins.input', side_effect=input_furniture):
            add_new_item()

        actual_inventory = FULL_INVENTORY
        expected_inventory = {
            '2': item.return_as_dictionary()}
        self.assertDictEqual(actual_inventory, expected_inventory)

    # Adding electric appliance with main
    def test_main_add_electric_appliance_integration(self):
        FULL_INVENTORY.clear()
        price = get_latest_price()

        input_electric = ['3', 'phone', '3', 'n', 'y', 'Apple', '100']
        item = ElectricAppliances('3', 'phone', price, '3', 'Apple', '100')
        with patch('builtins.input', side_effect=input_electric):
            add_new_item()

        actual_inventory = FULL_INVENTORY
        expected_inventory = {
            '3': item.return_as_dictionary()}
        self.assertDictEqual(actual_inventory, expected_inventory)

    def test_mainmenu_q(self):
        '''test exiting programm'''
        with patch('builtins.input', side_effect=['q']):
            with self.assertRaises(SystemExit):
                exit_program()
