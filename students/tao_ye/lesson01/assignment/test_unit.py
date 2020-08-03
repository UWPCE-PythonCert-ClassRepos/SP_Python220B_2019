import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch
import io

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances

import inventory_management.main as m
import inventory_management.market_prices as mp


class InventoryClassTests(TestCase):

    def test_inventory_class(self):
        item = Inventory("1", "Bed", "500", "30")

        item_dict_created = item.return_as_dictionary()

        self.assertEqual(item_dict_created, {'product code': '1', 'description': 'Bed',
                                             'market price': '500', 'rental price': '30'})


class ElectricApplianceClassTests(TestCase):

    def test_electrical_appliance_class(self):
        item = ElectricAppliances("1", "Washer", "800", "20", "LG", "110")

        item_dict_created = item.return_as_dictionary()

        self.assertEqual(item_dict_created, {'product code': '1', 'description': 'Washer',
                                             'market price': '800', 'rental price': '20',
                                             'brand': 'LG', 'voltage': '110'})


class FurnitureClassTests(TestCase):

    def test_furniture_class(self):
        item = Furniture("1", "Sofa", "1000", "50", "Leather", "XL")

        item_dict_created = item.return_as_dictionary()

        self.assertEqual(item_dict_created, {'product code': '1', 'description': 'Sofa',
                                             'market price': '1000', 'rental price': '50',
                                             'material': 'Leather', 'size': 'XL'})


class MarketPriceModuleTests(TestCase):

    def test_market_price_module(self):
        self.assertEqual(24, mp.get_latest_price('1'))


class MainModuleTests(TestCase):

    @patch('builtins.input', side_effect='1')
    def test_main_menu(self, mock_input):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            funtion_object = m.main_menu()
            assert funtion_object == m.add_new_item

    def test_get_price(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            item_code = "1"
            m.get_latest_price = MagicMock()
            m.get_price(item_code)
        m.get_latest_price.assert_called_with(item_code)

    inventory_input_sequence = ["1", "Bed", "30", "n", "n"]
    appliance_input_sequence = ["2", "Washer", "20", "n", "y", "LG", "110"]
    furniture_input_sequence = ["3", "Sofa", "50", "y", "Leather", "XL"]

    @patch('builtins.input', side_effect=inventory_input_sequence)
    def test_add_new_item_inventory(self, mock_input):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            m.get_latest_price = MagicMock(return_value='500')
            m.add_new_item()
        assert m.FULL_INVENTORY['1'] == {'product code': '1', 'description': 'Bed',
                                         'market price': '500', 'rental price': '30'}

    @patch('builtins.input', side_effect=appliance_input_sequence)
    def test_add_new_item_appliance(self, mock_input):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            m.get_latest_price = MagicMock(return_value='800')
            m.add_new_item()
        assert m.FULL_INVENTORY['2'] == {'product code': '2', 'description': 'Washer',
                                         'market price': '800', 'rental price': '20',
                                         'brand': 'LG', 'voltage': '110'}

    @patch('builtins.input', side_effect=furniture_input_sequence)
    def test_add_new_item_furniture(self, mock_input):
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            m.get_latest_price = MagicMock(return_value='1000')
            m.add_new_item()
        assert m.FULL_INVENTORY['3'] == {'product code': '3', 'description': 'Sofa',
                                         'market price': '1000', 'rental price': '50',
                                         'material': 'Leather', 'size': 'XL'}

    @patch('builtins.input', return_value="3")
    def test_item_info(self, mock_input):
        printout = 'product code:3\ndescription:Sofa\nmarket price:1000\n' \
                   'rental price:50\nmaterial:Leather\nsize:XL'
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            m.item_info()

        assert fake_stdout.getvalue().strip() == printout

    @patch('builtins.input', return_value="random")
    def test_item_info_not_found(self, mock_input):
        printout = 'Item not found in inventory'
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            m.item_info()

        assert fake_stdout.getvalue().strip() == printout

    def test_exit(self):
        sys.exit = MagicMock()
        m.exit_program()
        sys.exit.assert_called()
