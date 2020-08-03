from unittest import TestCase
from unittest.mock import MagicMock, patch
import io

import inventory_management.main as m


input_sequence_add_item = ['1',
                           '1', 'Bed', '30', 'n', 'n',
                           '1',
                           '2', 'Washer', '20', 'n', 'y', 'LG', '110',
                           '1',
                           '3', 'Sofa', '50', 'y', 'Leather', 'XL']

inventory_item = {'1': {'product code': '1', 'description': 'Bed',
                        'market price': '500', 'rental price': '30'}}

add_appliance_item = {'1': {'product code': '1', 'description': 'Bed',
                            'market price': '500', 'rental price': '30'},
                      '2': {'product code': '2', 'description': 'Washer',
                            'market price': '800', 'rental price': '20',
                            'brand': 'LG', 'voltage': '110'}}

add_furniture_item = {'1': {'product code': '1', 'description': 'Bed',
                            'market price': '500', 'rental price': '30'},
                      '2': {'product code': '2', 'description': 'Washer',
                            'market price': '800', 'rental price': '20',
                            'brand': 'LG', 'voltage': '110'},
                      '3': {'product code': '3', 'description': 'Sofa',
                            'market price': '1000', 'rental price': '50',
                            'material': 'Leather', 'size': 'XL'}}


class IntegrationTests(TestCase):

    @patch('builtins.input', side_effect=input_sequence_add_item)
    def test_main_menu_option_1(self, mock_input):
        """ Test main menu option 1: add_new item """
        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            # run option 1 three times to add three items
            m.get_latest_price = MagicMock(return_value='500')
            m.main_menu()()
            assert m.FULL_INVENTORY == inventory_item

            m.get_latest_price = MagicMock(return_value='800')
            m.main_menu()()
            assert m.FULL_INVENTORY == add_appliance_item

            m.get_latest_price = MagicMock(return_value='1000')
            m.main_menu()()
            assert m.FULL_INVENTORY == add_furniture_item

    @patch('builtins.input', side_effect=['2', '3'])
    def test_main_menu_option_2(self, mock_input):
        """ Test main menu option 2: item_info """
        printout = 'Please choose from the following options 1, 2, q:\n' \
                   '1. Add a new item to the inventory\n' \
                   '2. Get item information\n' \
                   'q. Quit\n' \
                   'product code:3\ndescription:Sofa\nmarket price:1000\n' \
                   'rental price:50\nmaterial:Leather\nsize:XL'

        with patch('sys.stdout', new=io.StringIO()) as fake_output:
            m.main_menu()()

        assert fake_output.getvalue().strip() == printout
