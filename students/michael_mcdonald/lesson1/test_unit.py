"""test the inventory management module"""
# pylint: disable=E1111

import unittest
from unittest import TestCase
from unittest.mock import patch
from inventory_management import electric_appliances_class as eac  # pylint: disable=import-error
from inventory_management import inventory_class as ic  # pylint: disable=import-error
from inventory_management import furniture_class as fc  # pylint: disable=import-error
from inventory_management import market_prices as mp  # pylint: disable=import-error
from inventory_management import main as ma  # pylint: disable=import-error
# integration testing
# linting
# for each set of tests create a class
# cd C:\Users\mimcdona\Dropbox\UW\UW-Python220_Project
# python -m unittest test_unit.py
# python -m coverage run --source=inventory_management -m unittest test_unit.py
# python -m coverage report

SAMPLE_GENE_ITEM_DICT = {1: {'product_code': 1, 'description': 'Tape', 'market_price': 24,
                             'rental_price': 24}}

SAMPLE_ELEC_ITEM_DICT = {10: {'product_code': 10, 'description': 'Blender', 'market_price': 24,
                              'rental_price': 24, 'brand': 'Omega', 'voltage': '120'}}

SAMPLE_FURN_ITEM_DICT = {100: {'product_code': 100, 'description': 'Chair', 'market_price': 24,
                               'rental_price': 24, 'material': 'wood', 'size': 'L'}}

SAMPLE_FULL_INVENTORY = {}


class TestElectricAppliances(TestCase):
    """test ElectricAppliances class"""

    def test_return_as_dictionary(self):
        """test eac return as dictionary"""

        sample_dict = list(SAMPLE_ELEC_ITEM_DICT.values())[0]
        lst = list(sample_dict.values())
        new_eac_item = eac.ElectricAppliances(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5])
        test_dict = new_eac_item.return_as_dictionary()
        self.assertEqual(test_dict, sample_dict)
    print('- TestElectricAppliances.test_return_as_dictionary complete -')


class TestInventory(TestCase):
    """test Inventory class"""

    def test_return_as_dictionary(self):
        """test generic inventory return as dictionary"""

        sample_dict = list(SAMPLE_GENE_ITEM_DICT.values())[0]
        lst = list(sample_dict.values())
        new_generic_item = ic.Inventory(lst[0], lst[1], lst[2], lst[3])
        test_dict = new_generic_item.return_as_dictionary()
        self.assertEqual(test_dict, sample_dict)
    print('- TestInventory.test_return_as_dictionary complete -')


class TestFurniture(TestCase):
    """test Furniture class"""

    def test_return_as_dictionary(self):
        """test furniture return as dictionary"""

        sample_dict = list(SAMPLE_FURN_ITEM_DICT.values())[0]
        lst = list(sample_dict.values())
        new_furn_item = fc.Furniture(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5])
        test_dict = new_furn_item.return_as_dictionary()
        self.assertEqual(test_dict, sample_dict)
    print('- TestFurniture.test_return_as_dictionary complete -')


class TestMarketPrices(TestCase):
    """test MarketPrices"""

    def test_get_latest_price_equal(self):
        """test get latest price"""

        with patch("inventory_management.market_prices") as mock_market_prices:
            mock_market_prices.return_value = 24
            self.assertEqual(mp.get_latest_price() == 24)
    print('- TestMarketPricestest_get_latest_price_equal complete -')


class TestMain(TestCase):
    """test main (program execution"""
    sample_valid_prompts = ['1', '2', 'q']
    current_valid_prompt_cnt = 3

    def setUp(self):
        """pass for now"""

    def tearDown(self):
        """pass for now"""

    def test_main_menu(self):
        """Test main UI of main module."""

        counter = 0
        for i in TestMain.sample_valid_prompts:
            with patch('builtins.input', side_effect=i):
                if i == 1:
                    self.assertEqual(ma.main_menu(), ma.add_new_item)
                if i == 2:
                    self.assertEqual(ma.main_menu(), ma.item_info)
                if i == 'q':
                    self.assertEqual(ma.main_menu(), ma.exit_program)
            counter = counter + 1
        self.assertEqual(TestMain.current_valid_prompt_cnt, counter)
        print('- TestMain.test_main_menu complete -')

    def test_add_new_item_furn(self):
        """test new item furniture"""

        ma.FULL_INVENTORY = {}
        input_pachinko = [100, 'Chair', 24, 'y', 'wood', 'L']
        with patch('builtins.input', side_effect=input_pachinko):
            new_furn_item: object = ma.add_new_item()
            print(new_furn_item)
            self.assertEqual(SAMPLE_FURN_ITEM_DICT, ma.FULL_INVENTORY)
            ma.FULL_INVENTORY = {}

    def test_add_new_item_eac(self):
        """test new item elec"""

        ma.FULL_INVENTORY = {}
        input_pachinko = [10, 'Blender', 24, 'n', 'y', 'Omega', '120']
        with patch('builtins.input', side_effect=input_pachinko):
            new_eac_item = ma.add_new_item()
            print(new_eac_item)
            self.assertEqual(SAMPLE_ELEC_ITEM_DICT, ma.FULL_INVENTORY)
            ma.FULL_INVENTORY = {}

    def test_add_new_item_generic(self):
        """test new item generic"""

        ma.FULL_INVENTORY = {}
        input_pachinko = [1, 'Tape', 24, 'n', 'n']
        with patch('builtins.input', side_effect=input_pachinko):
            new_generic_item = ma.add_new_item()
            print(new_generic_item)
            self.assertEqual(SAMPLE_GENE_ITEM_DICT, ma.FULL_INVENTORY)
            ma.FULL_INVENTORY = {}

    def test_item_info_found(self):
        """test item info found"""

        ma.FULL_INVENTORY = {}
        input_pachinko_product = [1, 'Tape', 24, 'n', 'n']
        input_pachinko_item_info = [1]
        sample_print = 'product_code: 1\ndescription: Tape\nmarket_price: 24\nrental_price: 24\n'
        with patch('builtins.input', side_effect=input_pachinko_product):
            new_generic_item = ma.add_new_item()
            print(new_generic_item)
        with patch('builtins.input', side_effect=input_pachinko_item_info):
            new_generic_item_item_info = ma.item_info()
            self.assertEqual(print(sample_print), print(new_generic_item_item_info))
            ma.FULL_INVENTORY = {}

    def test_item_info_not_found(self):
        """test item info not found"""

        ma.FULL_INVENTORY = {}
        input_pachinko_product = [1, 'Tape', 24, 'n', 'n']
        input_pachinko_item_info = [2]
        sample_print = 'Item not found in inventory'
        with patch('builtins.input', side_effect=input_pachinko_product):
            new_generic_item = ma.add_new_item()
            print(new_generic_item)
        with patch('builtins.input', side_effect=input_pachinko_item_info):
            new_generic_item_item_info = ma.item_info()
            self.assertEqual(print(sample_print), print(new_generic_item_item_info))
            ma.FULL_INVENTORY = {}

    def test_exit_program(self):
        """test exit program"""

        with self.assertRaises(SystemExit) as sysex:
            ma.exit_program()
            self.assertEqual(sysex.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
