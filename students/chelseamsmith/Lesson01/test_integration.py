"""Inventory management integration tests"""
from unittest import TestCase
from unittest.mock import patch
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.main as main
import inventory_management.market_prices as market_prices
import io


class IntegrationTest(TestCase):
    """integration test for inventory management modules"""

    def test_integration(self):
        """tests the various functions in main"""
        main.FULL_INVENTORY={} #make sure I have a clear inventory to work with
        #add an appliance
        input_appliance = ('1', 'tv', 25, 'n', 'y', 'Samsung', '60')
        with patch('builtins.input', side_effect = input_appliance):
            main.add_new_item()
        #add furniture
        input_furniture = ('2', 'table', 50, 'y', 'wood', 'L')
        with patch('builtins.input', side_effect = input_furniture):
            main.add_new_item()
        #add a miscellaneous item
        input_inventory = ('3', 'vase', 10, 'n', 'n')
        with patch('builtins.input', side_effect = input_inventory):
            main.add_new_item()

        #use item_info function to look for an object
        with patch('builtins.input', side_effect = '2'):
            with patch('sys.stdout', new=io.StringIO()) as actual_result:
                main.item_info()
        test_value = '''product_code:2
description:table
market_price:24
rental_price:50
material:wood
size:L
'''
        self.assertEqual(actual_result.getvalue(), test_value)
