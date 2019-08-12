"""
Muhammad Khan
date: 07/01/2019


This module contains the integration test for the inventory management project

"""
import sys
import inventory_management.market_prices as mp
import inventory_management.inventory_class as ic
import inventory_management.furniture_class as fc
import inventory_management.electric_appliances_class as ec
import inventory_management.main as main
import unittest as ut
from unittest.mock import patch, MagicMock


class ModuleIntegrationTest(ut.TestCase):

    def test_module(self):
        """Test the module functionality"""
        # This piece tests for adding a new furniture
        user_input_1 =  ("1", "001", "table", "$3", 'y',"wood","L" )
        furniture_dict = {"001":{"product_code":"001","description":"table",
                                   "market_price":24,"rental_price":"$3",
                                    "material":"wood","size":"L"}}
        with patch("builtins.input", side_effect = user_input_1):
            main.main_menu()()
            self.assertEqual(main.FULL_INVENTORY, furniture_dict)
       # This piece test adding any other item.
        user_input_2 =  ( "\n","1","001", "table", "$3", "n","n")
        inventory_dict = {"001":{"product_code":"001","description":"table",
                                   "market_price":24,"rental_price":"$3"}}
        with patch("builtins.input", side_effect = user_input_2):
            main.main_menu()()
            self.assertEqual(main.FULL_INVENTORY, inventory_dict)
       # This piece test adding the electrical item.
        user_input_3 =  ("\n","1","003", "battery", "$5", "n", "y", "legend", "20V")
        all_item_dict = {"001":{"product_code":"001","description":"table",
                                "market_price":24,"rental_price":"$3"},
                         "003":{"product_code":"003","description":"battery",
                         "market_price":24,"rental_price":"$5","brand":"legend",
                         "voltage":"20V"}}
        with patch("builtins.input", side_effect = user_input_3):
            main.main_menu()()
            self.assertEqual(main.FULL_INVENTORY, all_item_dict)
        # This piece test item_info method.
        info_input = ("\n","2","001")
        with patch('builtins.input', side_effect = info_input):
             self.assertEqual(main.main_menu(), main.item_info)
        # This piece test the exit program.
        exit_input = ("\n","q")
        with patch('builtins.input', side_effect = exit_input):
            self.assertEqual(main.main_menu(), main.exit_program)

if __name__ == "__main__":
    ut.main()