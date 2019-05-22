import sys
sys.path.append('/Users/guntur/PycharmProjects/uw/p220/SP_Python220B_2019/students/g_rama'
                '/lesson01/inventory_management')
from unittest import TestCase, mock
from unittest.mock import patch
import unittest
import pytest
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import market_prices
import main


class Integrationtest(unittest.TestCase):
    """Integration tests for all classes"""

    def test_integration(self):
        """Integration test function"""
        test_market_price = market_prices.get_latest_price('item_code')
        test_inventory_data = [1, "dining_table_description", 400, 'n', 'n']
        with patch('builtins.input', side_effect=test_inventory_data):
            main.add_new_item()

        test_inventory_object = Inventory(1, "dining_table_description", test_market_price, 400)
        print(test_inventory_object)

        # test_expected_inventory_data = {'product_code': 1, 'description': 'dining_table_description',
        #                                'market_price': 24, 'rental_price': 400}
        # self.assertDictEqual(test_inventory_data_values, test_expected_inventory_data)

        test_furniture_data = [2, "bed", "500", 'y', 'teak', 'L']
        with patch('builtins.input', side_effect=test_furniture_data):
            main.add_new_item()

        test_furniture_object = Furniture(2, "bed", test_market_price, "500", 'teak', 'L')




        # test_electric_data = [1, 'refregirator_description', 400, 'n', 'y', 'samsung', '110v']
        # with patch('builtins.input', side_effect=test_electric_data):
        #     main.add_new_item()
        #     print(main.FULL_INVENTORY[test_electric_data[0]])
        #     test_electric_data_values = main.FULL_INVENTORY[test_electric_data[0]]
        #
        # test_expected_electric_data = {'product_code': 1, 'description': 'refregirator_description',
        #                                'market_price': 24, 'rental_price': 400, 'brand': 'samsung', 'voltage': '110v'}
        # self.assertDictEqual(test_expected_electric_data, test_electric_data_values)

        full_data_main = main.FULL_INVENTORY
        expected_data_main = {
            1: test_inventory_object.return_as_dictionary(),
            2: test_furniture_object.return_as_dictionary()}
        self.assertEqual(full_data_main, expected_data_main)







