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
from io import StringIO


class TestInventory(unittest.TestCase):
    """
    Testing
    """
    def testInventory(self):
        """Testing of Inventory initialization"""
        test_inventory = Inventory(1, "dining_table_description", 400, 50)
        assert test_inventory.product_code == 1
        assert test_inventory.description == "dining_table_description"
        assert test_inventory.market_price == 400
        assert test_inventory.rental_price == 50
        test_actualoutput = test_inventory.return_as_dictionary()
        test_expectedoutput = {'product_code': 1, 'description': "dining_table_description", 'market_price': 400,
                              'rental_price': 50}
        assert test_actualoutput == test_expectedoutput
        self.assertDictEqual(test_actualoutput, test_expectedoutput)


class TestElectricAppliances(unittest.TestCase):
    """
    Testing ElectricAppliances class
    """
    def testElectricAppliances(self):
        """Testing of electricalAppliance initialization"""
        test_electric_app = ElectricAppliances(1, "refregirator_description", 400, 50,
                                               "samsung", "110v")
        assert test_electric_app.product_code == 1
        assert test_electric_app.description == "refregirator_description"
        assert test_electric_app.market_price == 400
        assert test_electric_app.rental_price == 50
        assert test_electric_app.brand == "samsung"
        assert test_electric_app.voltage == "110v"
        test_actualoutput = test_electric_app.return_as_dictionary()
        test_expectedoutput = {'product_code': 1, 'description': "refregirator_description", 'market_price': 400,
                               'rental_price': 50, 'brand': "samsung", 'voltage': "110v"}
        assert test_actualoutput == test_expectedoutput
        self.assertDictEqual(test_actualoutput, test_expectedoutput)


class TestFurniture(unittest.TestCase):
    """
    Testing Furniture class
    """
    def testFurniture(self):
        """Testing of Furniture initialization"""
        test_furniture = Furniture(1, "dining_table_description", 400, 50, "glass", "L")
        assert test_furniture.product_code == 1
        assert test_furniture.description == "dining_table_description"
        assert test_furniture.market_price == 400
        assert test_furniture.rental_price == 50
        assert test_furniture.material == "glass"
        assert test_furniture.size == "L"
        test_actualoutput = test_furniture.return_as_dictionary()
        test_expectedoutput = {'product_code': 1, 'description': "dining_table_description", 'market_price': 400,
                               'rental_price': 50, 'material': "glass", 'size': "L"}
        assert test_actualoutput == test_expectedoutput
        self.assertDictEqual(test_actualoutput, test_expectedoutput)


class TestMarketPrices(unittest.TestCase):
    """
    Testing market_prices class
    """
    def test_get_latest_price(self):
        test_actual_item_code = market_prices.get_latest_price("item_code")
        test_expected_item_code = 24
        assert test_actual_item_code == test_expected_item_code


class TestMain(unittest.TestCase):
    """Testing of the main class"""
    def test_main_menu(self):
        """Testing of menu options"""
        prompt_1 = "1"
        prompt_2 = "2"
        prompt_3 = "q"
        with patch('builtins.input', side_effect=prompt_1):
            expected_option = 'add_new_item'
            actual_option = main.main_menu()
            self.assertEqual(actual_option.__name__, expected_option)
        with patch('builtins.input', side_effect=prompt_2):
            expected_option = 'item_info'
            actual_option = main.main_menu()
            self.assertEqual(actual_option.__name__, expected_option)
        with patch('builtins.input', side_effect=prompt_3):
            expected_option = 'exit_program'
            actual_option = main.main_menu()
            self.assertEqual(actual_option.__name__, expected_option)

    def test_get_price(self):
        """Testing of get price item"""
        expected_output = 24
        actual_output = main.get_price(100)
        self.assertEquals(expected_output, actual_output)

    def test_add_new_item(self):
        """Testing of add_new_item function"""
        test_furniture_data = [1, 'dining_table_description', 50, 'y', 'glass', 'L']
        test_electric_data = [1, 'refregirator_description', 400, 'n', 'y', 'samsung', '110v']
        test_inventory_data = [1, "dining_table_description", 400, 'n', 'n']
        with patch('builtins.input', side_effect=test_furniture_data):
            main.add_new_item()
            print(main.FULL_INVENTORY[test_furniture_data[0]])
            test_furniture_data_values = main.FULL_INVENTORY[test_furniture_data[0]]

        test_expected_furniture_data = {'product_code': 1, 'description': 'dining_table_description',
                                        'market_price': 24, 'rental_price': 50, 'material': 'glass', 'size': 'L'}
        self.assertDictEqual(test_furniture_data_values, test_expected_furniture_data)

        with patch('builtins.input', side_effect=test_electric_data):
            main.add_new_item()
            print(main.FULL_INVENTORY[test_electric_data[0]])
            test_electric_data_values = main.FULL_INVENTORY[test_electric_data[0]]

        test_expected_electric_data = {'product_code': 1, 'description': 'refregirator_description',
                                       'market_price': 24, 'rental_price': 400, 'brand': 'samsung', 'voltage': '110v'}
        self.assertDictEqual(test_expected_electric_data, test_electric_data_values)

        with patch('builtins.input', side_effect=test_inventory_data):
            main.add_new_item()
            print(main.FULL_INVENTORY[test_inventory_data[0]])
            test_inventory_data_values = main.FULL_INVENTORY[test_inventory_data[0]]

        test_expected_inventory_data = {'product_code': 1, 'description': 'dining_table_description',
                                       'market_price': 24, 'rental_price': 400}
        self.assertDictEqual(test_inventory_data_values, test_expected_inventory_data)

    def test_item_info(self):
        """Test item info """
        test_data = ['1', 'dining', '50', 'y', 'glass', 'L']
        with patch('builtins.input', side_effect=test_data):
            main.add_new_item()
            print(main.FULL_INVENTORY)
        test_item_code = 1
        with patch('builtins.input', side_effect='2'):
            actual_output = main.item_info()
            print("nub")
            print(actual_output)
        expected_output = '''product_code:1
description:dining
market_price:24
rental_price:50
material:glass
size:L'''
        self.assertNotEqual(actual_output, expected_output)


    # @patch('sys.stdout', new_callable=StringIO)
    # def test_item_info(self, mock_stdout):
    #     # test_FULL_INVENTORY = {1, {'product_code': 1, 'description': 'refregirator_description',
    #     #                            'market_price': 24, 'rental_price': 400, 'brand': 'samsung', 'voltage': '110v'}}
    #     test_non_item_code = 2
    #     with patch('builtins.input', side_effect=test_non_item_code):
    #         main.item_info()
    #         assert mock_stdout.__getattribute__() == 'Item not found in inventory\n'


if __name__ == '__main__':
    unittest.main()

