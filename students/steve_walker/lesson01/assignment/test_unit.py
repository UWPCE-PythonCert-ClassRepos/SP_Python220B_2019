"""Unit tests for inventory_management files"""

from unittest import TestCase
from unittest.mock import patch
from IPython.utils.capture import capture_output

import inventory_management.market_prices as market_prices
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.main as main


class InventoryTests(TestCase):

    def test_inventory(self):
        
        inventory_sample = Inventory(11,
                                     "sample description",
                                     "sample market price",
                                     "sample rental price")

        self.assertEqual(inventory_sample.return_as_dictionary(),
                         {'product_code': 11,
                          'description': "sample description",
                          'market_price': "sample market price",
                          'rental_price': "sample rental price"})


class ElectricAppliancesTests(TestCase):

    def test_electric_appliances(self):
        
        electric_app_sample = ElectricAppliances(12,
                                                 "sample description",
                                                 "sample market price",
                                                 "sample rental price",
                                                 "sample brand",
                                                 "sample voltage")

        self.assertEqual(electric_app_sample.return_as_dictionary(),
                         {'product_code': 12,
                          'description': "sample description",
                          'market_price': "sample market price",
                          'rental_price': "sample rental price",
                          'brand': "sample brand",
                          'voltage': "sample voltage"})
    

class FurnitureTests(TestCase):

    def test_furniture(self):
        
        furniture_sample = Furniture(13, "sample description",
                                     "sample market price",
                                     "sample rental price",
                                     "sample material",
                                     "sample size")

        self.assertEqual(furniture_sample.return_as_dictionary(),
                         {'product_code': 13,
                          'description': "sample description",
                          'market_price': "sample market price",
                          'rental_price': "sample rental price",
                          'material': "sample material",
                          'size': "sample size"})


class MarketPriceTests(TestCase):

    def test_get_latest_price(self): # Update once returns real data

        self.assertEqual(market_prices.get_latest_price('101'), 24)


class MainTests(TestCase):

    def test_main_menu(self):
        """Test menu options call the correct methods"""

        # Use context managers (with + indentation) to define the patch scope
        # The builtins module is home to input().
        # Because main calls input from builtins, we need to patch builtins.
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)


    def test_add_new_furniture(self):
        furniture_inputs = (23, "sample description", "sample rental price",
                            "y", "sample material", "sample size")

        with patch('builtins.input', side_effect=furniture_inputs):
            with patch('inventory_management.market_prices.get_latest_price',
                       return_value=53):
                main.add_new_item()
        self.assertEqual(main.full_inventory[23],
                         {'product_code': 23,
                          'description': "sample description",
                          'market_price': 53,
                          'rental_price': "sample rental price",
                          'material': "sample material",
                          'size': "sample size"})


    def test_add_new_electronic_app(self):
        electronic_app_inputs = (22, "sample description",
                                 "sample rental price", "n", "y",
                                 "sample brand", "sample voltage")

        with patch('builtins.input', side_effect=electronic_app_inputs):
            with patch('inventory_management.market_prices.get_latest_price',
                       return_value=52):
                main.add_new_item()
        self.assertEqual(main.full_inventory[22],
                         {'product_code': 22,
                          'description': "sample description",
                          'market_price': 52,
                          'rental_price': "sample rental price",
                          'brand': "sample brand",
                          'voltage': "sample voltage"})


    def test_add_inventory(self):
        inventory_inputs = (21, "sample description", "sample rental price",
                            "n", "n")

        with patch('builtins.input', side_effect=inventory_inputs):
            with patch('inventory_management.market_prices.get_latest_price',
                       return_value=51):
                main.add_new_item()
        self.assertEqual(main.full_inventory[21],
                         {'product_code': 21,
                          'description': "sample description",
                          'market_price': 51,
                          'rental_price': "sample rental price"})


    def test_item_info(self):
        info_test_input = {'product_code': 21,
                           'description': "sample description",
                           'market_price': 24,
                           'rental_price': "sample rental price"}

        with patch('builtins.input', side_effect=[21]):
            main.full_inventory[21] = info_test_input
            with capture_output() as capture: # Necessary to get printed lines
                main.item_info()
            print(capture.stdout)
            self.assertEqual(capture.stdout,
                             "product_code:21\n"
                             "description:sample description\n"
                             "market_price:24\n"
                             "rental_price:sample rental price\n")

        with patch('builtins.input', side_effect='bad_key'):
            main.item_info()
            self.assertEqual(main.item_info(), None)


    def test_exit(self):
        with self.assertRaises(SystemExit):
            main.exit_program()
