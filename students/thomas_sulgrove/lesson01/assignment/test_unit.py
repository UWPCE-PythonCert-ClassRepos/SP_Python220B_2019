"""Unit tests for inventory Managment"""
# pylint: disable=import-error
from unittest import TestCase
import io
import sys
from unittest.mock import patch
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.main import main_menu, get_price, add_new_item, item_info, exit_program, FULL_INVENTORY
from inventory_management.market_prices import get_latest_price


class TestInventoryManagement(TestCase):
    """Class for housing the tests"""
    def test_inventory(self):
        """best the base inventory class"""
        test = Inventory(0, 'desc', 1, 2)
        self.assertEqual(test.return_as_dictionary(),
                         {'product_code': 0,
                          'description': 'desc',
                          'market_price': 1,
                          'rental_price': 2})

    def test_electric_appliances(self):
        """test electric appliances class"""
        test = ElectricAppliances(777, 'Look with your special eyes', 999, 888, 'MYBRAND', 2)
        self.assertEqual(test.return_as_dictionary(),
                         {'product_code': 777,
                          'description': 'Look with your special eyes',
                          'market_price': 999,
                          'rental_price': 888,
                          'brand': 'MYBRAND',
                          'voltage': 2})

    def test_furniture(self):
        """test out the furniture class"""
        test = Furniture(17, 'desc', 354, 144, 'bronze', 'yuge')
        self.assertEqual(test.return_as_dictionary(),
                         {'product_code': 17,
                          'description': 'desc',
                          'market_price': 354,
                          'rental_price': 144,
                          'material': 'bronze',
                          'size': 'yuge'})

    def test_main_menu(self):
        """tests for main menu function"""
        self.assertTrue(main_menu('1'), 'add_new_item')
        self.assertTrue(main_menu('2'), 'item_info')
        self.assertTrue(main_menu('q'), 'exit_program')

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        with patch('builtins.input', side_effect=['popcorn','q']):
            main_menu()
        sys.stdout = sys.__stdout__
        self.assertIn('Please choose from the following options', capturedOutput.getvalue())
        self.assertIn('1. Add a new item to the inventory', capturedOutput.getvalue())
        self.assertIn('2. Get item information', capturedOutput.getvalue())
        self.assertIn('q. Quit', capturedOutput.getvalue())


    def test_get_price(self):
        """test the get price function"""
        self.assertEqual(None, get_price(134))


    def test_add_new_item(self):
        inventory = ['0', 'desc', '1', 'n', 'n']
        furniture = [17, 'desc', 354, 'y', 'bronze', 'XL']
        electric = [777, 'desc', 999, 'n', 'y', 'MYBRAND', 2]

        with patch('builtins.input', side_effect=inventory):
            add_new_item()

        self.assertEqual(FULL_INVENTORY['0'],  {'product_code': '0', 'description': 'desc',
                                                'market_price': 24, 'rental_price': '1'})

        with patch('builtins.input', side_effect=furniture):
            add_new_item()

        self.assertEqual(FULL_INVENTORY[17], {'product_code': 17, 'description': 'desc',
                                            'market_price': 24, 'rental_price': 354,
                                              'material': 'bronze', 'size': 'XL'})

        with patch('builtins.input', side_effect=electric):
            add_new_item()

        self.assertEqual(FULL_INVENTORY[777], {'product_code': 777, 'description': 'desc',
                                               'market_price': 24, 'rental_price': 999,
                                               'brand': 'MYBRAND', 'voltage': 2})

    def test_item_info(self):
        """ asert equal """
        new_furniture = ['159', 'desc', '52', 'n', 'n']
        with patch('builtins.input', side_effect=new_furniture):
            add_new_item()
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        with patch('builtins.input', side_effect=['159']):
            item_info()
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(),
                         'product_code:159\ndescription:desc\nmarket_price:24\nrental_price:52\n')

        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        with patch('builtins.input', side_effect=[56456456498406]):
            item_info()
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), 'Item not found in inventory\n')


    def test_exit_program(self):
        """ assert raises """
        with self.assertRaises(SystemExit):
            exit_program()


    def test_get_latest_price(self):
        """test the get latest price function"""
        self.assertEqual(24, get_latest_price(134))
